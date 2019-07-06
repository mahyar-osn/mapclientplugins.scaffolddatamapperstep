from math import radians
from opencmiss.zinc.graphics import Graphics
from opencmiss.zinc.material import Material
from opencmiss.zinc.status import OK as ZINC_OK
from opencmiss.utils.maths import vectorops as maths

from ..utils import zincutils


class ScaffoldModel(object):

    def __init__(self, region, material_module, file_path):
        self._region = region
        self._material_module = material_module
        self._file_path = file_path
        self._scaffold_coordinate_field = None

        self._initialise_scene()
        self._initialise_surface_material()
        self._initialise_scaffold()

        self._settings = dict(yaw=0.0, pitch=0.0, roll=0.0, X=0.0, Y=0.0, Z=0.0)
        self._settings_change_callback = None
        self._current_angle_value = [0., 0., 0.]
        self._current_axis_value = [0., 0., 0.]

    def reset_settings(self):
        self._settings = dict(yaw=0.0, pitch=0.0, roll=0.0, X=0.0, Y=0.0, Z=0.0)
        self._apply_callback()

    def set_settings_change_callback(self, settings_change_callback):
        self._settings_change_callback = settings_change_callback

    def _apply_callback(self):
        self._settings_change_callback()

    def get_yaw_value(self):
        return self._settings['yaw']

    def get_pitch_value(self):
        return self._settings['pitch']

    def get_roll_value(self):
        return self._settings['roll']

    def get_X_value(self):
        return self._settings['X']

    def get_Y_value(self):
        return self._settings['Y']

    def get_Z_value(self):
        return self._settings['Z']

    def _create_surface_graphics(self):
        fm = self._region.getFieldmodule()
        fm.beginChange()

        surface_right_atrium = self._scene.createGraphicsSurfaces()
        surface_right_atrium.setCoordinateField(self._scaffold_coordinate_field)
        surface_right_atrium.setSubgroupField(fm.findFieldByName('right atrium'))
        surface_right_atrium.setRenderPolygonMode(Graphics.RENDER_POLYGON_MODE_SHADED)
        surface_material = self._material_module.findMaterialByName('right atrium')
        surface_right_atrium.setMaterial(surface_material)
        surface_right_atrium.setName('display_right_atrium_surfaces')

        surface_left_atrium = self._scene.createGraphicsSurfaces()
        surface_left_atrium.setCoordinateField(self._scaffold_coordinate_field)
        surface_left_atrium.setSubgroupField(fm.findFieldByName('left atrium'))
        surface_left_atrium.setRenderPolygonMode(Graphics.RENDER_POLYGON_MODE_SHADED)
        surface_material = self._material_module.findMaterialByName('left atrium')
        surface_left_atrium.setMaterial(surface_material)
        surface_left_atrium.setName('display_left_atrium_surfaces')

        surface_right_ventricle = self._scene.createGraphicsSurfaces()
        surface_right_ventricle.setCoordinateField(self._scaffold_coordinate_field)
        surface_right_ventricle.setSubgroupField(fm.findFieldByName('right ventricle'))
        surface_right_ventricle.setRenderPolygonMode(Graphics.RENDER_POLYGON_MODE_SHADED)
        surface_material = self._material_module.findMaterialByName('right ventricle')
        surface_right_ventricle.setMaterial(surface_material)
        surface_right_ventricle.setName('display_right_ventricle_surfaces')

        surface_left_ventricle = self._scene.createGraphicsSurfaces()
        surface_left_ventricle.setCoordinateField(self._scaffold_coordinate_field)
        surface_left_ventricle.setSubgroupField(fm.findFieldByName('left ventricle'))
        surface_left_ventricle.setRenderPolygonMode(Graphics.RENDER_POLYGON_MODE_SHADED)
        surface_material = self._material_module.findMaterialByName('left ventricle')
        surface_left_ventricle.setMaterial(surface_material)
        surface_left_ventricle.setName('display_left_ventricle_surfaces')

        fm.endChange()
        return

    def _create_line_graphics(self):
        lines = self._scene.createGraphicsLines()
        lines.setCoordinateField(self._scaffold_coordinate_field)
        lines.setName('display_lines')
        black = self._material_module.findMaterialByName('white')
        lines.setMaterial(black)
        return lines

    def create_scaffold_graphics(self):
        # self._create_line_graphics()
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

        right_atrium = self._material_module.createMaterial()
        right_atrium.setName('right atrium')
        right_atrium.setManaged(True)
        right_atrium.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.82, 0.45, 0.35])
        right_atrium.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.82, 0.45, 0.35])
        right_atrium.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
        right_atrium.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
        right_atrium.setAttributeReal(Material.ATTRIBUTE_ALPHA, 0.7)
        right_atrium.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)

        left_atrium = self._material_module.createMaterial()
        left_atrium.setName('left atrium')
        left_atrium.setManaged(True)
        left_atrium.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.79, 0.42, 0.32])
        left_atrium.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.79, 0.42, 0.32])
        left_atrium.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
        left_atrium.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
        left_atrium.setAttributeReal(Material.ATTRIBUTE_ALPHA, 0.7)
        left_atrium.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)

        right_ventricle = self._material_module.createMaterial()
        right_ventricle.setName('right ventricle')
        right_ventricle.setManaged(True)
        right_ventricle.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.71, 0.33, 0.22])
        right_ventricle.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.71, 0.33, 0.22])
        right_ventricle.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
        right_ventricle.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
        right_ventricle.setAttributeReal(Material.ATTRIBUTE_ALPHA, 0.7)
        right_ventricle.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)

        left_ventricle = self._material_module.createMaterial()
        left_ventricle.setName('left ventricle')
        left_ventricle.setManaged(True)
        left_ventricle.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.59, 0.22, 0.05])
        left_ventricle.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.59, 0.22, 0.05])
        left_ventricle.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
        left_ventricle.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
        left_ventricle.setAttributeReal(Material.ATTRIBUTE_ALPHA, 0.7)
        left_ventricle.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)

        self._material_module.endChange()
        return

    def _initialise_scaffold(self):
        result = self._region.readFile(self._file_path)
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

    def rotate_scaffold(self, angle, value):
        next_angle_value = value
        if angle == 'yaw':
            if next_angle_value > self._current_angle_value[0]:
                angle_value = next_angle_value - self._current_angle_value[0]
            else:
                angle_value = -(self._current_angle_value[0] - next_angle_value)
            euler_angles = [angle_value, 0., 0.]
            self._current_angle_value[0] = next_angle_value
            self._settings['yaw'] = next_angle_value
        elif angle == 'pitch':
            if next_angle_value > self._current_angle_value[1]:
                angle_value = next_angle_value - self._current_angle_value[1]
            else:
                angle_value = -(self._current_angle_value[1] - next_angle_value)
            euler_angles = [0., angle_value, 0.]
            self._current_angle_value[1] = next_angle_value
            self._settings['pitch'] = next_angle_value
        else:
            if next_angle_value > self._current_angle_value[2]:
                angle_value = next_angle_value - self._current_angle_value[2]
            else:
                angle_value = -(self._current_angle_value[2] - next_angle_value)
            euler_angles = [0., 0., angle_value]
            self._current_angle_value[2] = next_angle_value
            self._settings['roll'] = next_angle_value
        angles = euler_angles
        angles = [radians(x) for x in angles]
        rotation = maths.eulerToRotationMatrix3(angles)
        zincutils.transform_coordinates(self._scaffold_coordinate_field, rotation)
        self._apply_callback()

    def translate_scaffold(self, axis, value, rate):
        next_axis_value = value * rate

        if axis == 'X':
            if next_axis_value > self._current_axis_value[0]:
                axis_value = next_axis_value - self._current_axis_value[0]
            else:
                axis_value = -(self._current_axis_value[0] - next_axis_value)
            new_coordinates = [axis_value, 0., 0.]
            self._current_axis_value[0] = next_axis_value
            self._settings['X'] = next_axis_value
        elif axis == 'Y':
            if next_axis_value > self._current_axis_value[1]:
                axis_value = next_axis_value - self._current_axis_value[1]
            else:
                axis_value = -(self._current_axis_value[1] - next_axis_value)
            new_coordinates = [0., axis_value, 0.]
            self._current_axis_value[1] = next_axis_value
            self._settings['Y'] = next_axis_value
        else:
            if next_axis_value > self._current_axis_value[2]:
                axis_value = next_axis_value - self._current_axis_value[2]
            else:
                axis_value = -(self._current_axis_value[2] - next_axis_value)
            new_coordinates = [0., 0., axis_value]
            self._current_axis_value[2] = next_axis_value
            self._settings['Z'] = next_axis_value
        offset = new_coordinates
        zincutils.offset_scaffold(self._scaffold_coordinate_field, offset)
        self._apply_callback()
