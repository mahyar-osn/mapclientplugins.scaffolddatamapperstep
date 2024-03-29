from opencmiss.zinc.field import Field
from opencmiss.zinc.glyph import Glyph
from opencmiss.zinc.material import Material
from opencmiss.zinc.status import OK as ZINC_OK
from opencmiss.utils.maths import vectorops as maths


class DataModel(object):

    def __init__(self, region, material_module, ex_file_path, ephys_file_path=None):
        self._region = region
        self._material_module = material_module
        self._ex_file_path = ex_file_path
        self._ephys_file_path = ephys_file_path if ephys_file_path is not None else None
        self._data_coordinate_field = None

        self._initialise_point_material()
        self._initialise_scene()
        self._initialise_ex_data()

    def _identify_data_type(self):
        pass

    def _initialise_scene(self):
        self._scene = self._region.getScene()

    def _initialise_point_material(self):
        self._material_module.beginChange()
        cell_purple = self._material_module.createMaterial()
        cell_purple.setName('cell_purple')
        cell_purple.setManaged(True)
        cell_purple.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.7, 0.0, 1.0])
        cell_purple.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.7, 0.0, 1.0])
        cell_purple.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
        cell_purple.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
        cell_purple.setAttributeReal(Material.ATTRIBUTE_ALPHA, 1.0)
        cell_purple.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)
        self._material_module.endChange()

    def get_scene(self):
        if self._scene is not None:
            return self._scene
        else:
            raise ValueError('Scaffold scene is not initialised.')

    def _create_data_point_graphics(self):
        points = self._scene.createGraphicsPoints()
        points.setFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
        points.setCoordinateField(self._data_coordinate_field)
        point_attr = points.getGraphicspointattributes()
        point_attr.setGlyphShapeType(Glyph.SHAPE_TYPE_SPHERE)
        point_size = self._get_auto_point_size()
        point_attr.setBaseSize(point_size)
        points.setMaterial(self._material_module.findMaterialByName('cell_purple'))
        points.setName('display_points')

    def create_data_graphics(self):
        self._create_data_point_graphics()

    def _get_auto_point_size(self):
        minimums, maximums = self._get_data_range()
        data_size = maths.magnitude(maths.sub(maximums, minimums))
        return 0.25 * data_size

    def _get_data_range(self):
        fm = self._region.getFieldmodule()
        data_points = fm.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
        minimums, maximums = self._get_nodeset_minimum_maximum(data_points, self._data_coordinate_field)
        return minimums, maximums

    @staticmethod
    def _get_nodeset_minimum_maximum(nodeset, field):
        fm = field.getFieldmodule()
        count = field.getNumberOfComponents()
        minimums_field = fm.createFieldNodesetMinimum(field, nodeset)
        maximums_field = fm.createFieldNodesetMaximum(field, nodeset)
        cache = fm.createFieldcache()
        result, minimums = minimums_field.evaluateReal(cache, count)
        if result != ZINC_OK:
            minimums = None
        result, maximums = maximums_field.evaluateReal(cache, count)
        if result != ZINC_OK:
            maximums = None
        del minimums_field
        del maximums_field
        return minimums, maximums

    def _initialise_ex_data(self):
        sir = self._region.createStreaminformationRegion()
        point_cloud_resource = sir.createStreamresourceFile(self._ex_file_path)
        sir.setResourceDomainTypes(point_cloud_resource, Field.DOMAIN_TYPE_DATAPOINTS)
        result = self._region.read(sir)
        if result != ZINC_OK:
            raise ValueError('Failed to initiate EX data.')
        self._data_coordinate_field = self._get_data_coordinate_field()

    def _get_data_coordinate_field(self):
        fm = self._region.getFieldmodule()
        data_point_set = fm.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
        data_point = data_point_set.createNodeiterator().next()
        if not data_point.isValid():
            raise ValueError('Data cloud is empty')
        cache = fm.createFieldcache()
        cache.setNode(data_point)
        field_iter = fm.createFielditerator()
        field = field_iter.next()
        while field.isValid():
            if field.isTypeCoordinate() and (field.getNumberOfComponents() <= 3):
                if field.isDefinedAtLocation(cache):
                    return field
            field = field_iter.next()
        raise ValueError('Could not determine data coordinate field')

    @staticmethod
    def get_data_location(field):
        locations_list = list()
        fm = field.getFieldmodule()
        fm.beginChange()
        cache = fm.createFieldcache()
        datapoints = fm.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
        node_iter = datapoints.createNodeiterator()
        node = node_iter.next()
        while node.isValid():
            cache.setNode(node)
            _, coordinates = field.evaluateReal(cache, 3)
            locations_list.append(coordinates)
            node = node_iter.next()
        fm.endChange()
        return locations_list

    def get_data_id(self, field):
        return
