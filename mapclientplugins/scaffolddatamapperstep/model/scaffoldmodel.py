from opencmiss.zinc.field import Field
from opencmiss.zinc.graphics import Graphics
from opencmiss.zinc.material import Material
from opencmiss.zinc.status import OK as ZINC_OK


class ScaffoldModel(object):

    def __init__(self, region, material_module, file_path):
        self._region = region
        self._material_module = material_module
        self._file_path = file_path
        self._scaffold_coordinate_field = None

        self._initialise_scene()
        self._initialise_surface_material()

        self._initialise_scaffold()

    def _create_surface_graphics(self):
        surface = self._scene.createGraphicsSurfaces()
        surface.setCoordinateField(self._scaffold_coordinate_field)
        surface.setRenderPolygonMode(Graphics.RENDER_POLYGON_MODE_SHADED)
        surface_material = self._material_module.findMaterialByName('trans_blue')
        surface.setMaterial(surface_material)
        surface.setName('display_surfaces')
        return surface

    def _create_line_graphics(self):
        lines = self._scene.createGraphicsLines()
        lines.setCoordinateField(self._scaffold_coordinate_field)
        lines.setName('display_lines')
        black = self._material_module.findMaterialByName('white')
        lines.setMaterial(black)
        return lines

    def create_scaffold_graphics(self):
        self._create_line_graphics()
        self._create_surface_graphics()

    def _initialise_scene(self):
        if self._region.getScene():
            self._region.getScene().removeAllGraphics()
        self._scene = self._region.getScene()

    def get_scene(self):
        if self._scene is not None:
            return self._scene
        else:
            raise ValueError('Scaffold scene is not initialised.')

    def _initialise_surface_material(self):
        self._material_module.beginChange()
        trans_blue = self._material_module.createMaterial()
        trans_blue.setName('trans_blue')
        trans_blue.setManaged(True)
        trans_blue.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.0, 0.2, 0.6])
        trans_blue.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.0, 0.7, 1.0])
        trans_blue.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
        trans_blue.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
        trans_blue.setAttributeReal(Material.ATTRIBUTE_ALPHA, 0.3)
        trans_blue.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)
        self._material_module.endChange()

    def _initialise_scaffold(self):
        result = self._region.read(self._file_path)
        if result != ZINC_OK:
            raise ValueError('Failed to initiate scaffold')
        self._scaffold_coordinate_field = self._get_model_coordinate_field()

    def _get_mesh(self):
        fm = self._region.getFieldmodule()
        for dimension in range(3, 0, -1):
            mesh = fm.findMeshByDimension(dimension)
            if mesh.getSize() > 0:
                return mesh
        raise ValueError('Model contains no mesh')

    def _get_model_coordinate_field(self):
        mesh = self._get_mesh()
        element = mesh.createElementiterator().next()
        if not element.isValid():
            raise ValueError('Model contains no elements')
        fm = self._region.getFieldmodule()
        cache = fm.createFieldcache()
        cache.setElement(element)
        field_iter = fm.createFielditerator()
        field = field_iter.next()
        while field.isValid():
            if field.isTypeCoordinate() and (field.getNumberOfComponents() <= 3):
                if field.isDefinedAtLocation(cache):
                    return field
            field = field_iter.next()
        raise ValueError('Could not determine model coordinate field')
