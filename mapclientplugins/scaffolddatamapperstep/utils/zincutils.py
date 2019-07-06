from opencmiss.zinc.node import Node
from opencmiss.zinc.field import Field
from opencmiss.zinc.status import OK as ZINC_OK
from opencmiss.utils.maths.vectorops import add, dot


def matrixvectormult(m, v):
    return [dot(row_m, v) for row_m in m]


def transform_coordinates(field, rotation):
    number_of_components = field.getNumberOfComponents()
    if (number_of_components != 2) and (number_of_components != 3):
        print('zincutils.transformCoordinates: field has invalid number of components')
        return False
    if len(rotation) != number_of_components:
        print('zincutils.transformCoordinates: invalid matrix number of columns or offset size')
        return False
    if field.getCoordinateSystemType() != Field.COORDINATE_SYSTEM_TYPE_RECTANGULAR_CARTESIAN:
        print('zincutils.transformCoordinates: field is not rectangular cartesian')
        return False
    fe_field = field.castFiniteElement()
    if not fe_field.isValid():
        print('zincutils.transformCoordinates: field is not finite element field type')
        return False
    success = True
    fm = field.getFieldmodule()
    fm.beginChange()
    cache = fm.createFieldcache()
    nodes = fm.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
    node_template = nodes.createNodetemplate()
    node_iter = nodes.createNodeiterator()
    node = node_iter.next()
    while node.isValid():
        node_template.defineFieldFromNode(fe_field, node)
        cache.setNode(node)
        for derivative in [Node.VALUE_LABEL_VALUE, Node.VALUE_LABEL_D_DS1, Node.VALUE_LABEL_D_DS2,
                           Node.VALUE_LABEL_D2_DS1DS2, Node.VALUE_LABEL_D_DS3, Node.VALUE_LABEL_D2_DS1DS3,
                           Node.VALUE_LABEL_D2_DS2DS3, Node.VALUE_LABEL_D3_DS1DS2DS3]:
            versions = node_template.getValueNumberOfVersions(fe_field, -1, derivative)
            for v in range(1, versions + 1):
                result, values = fe_field.getNodeParameters(cache, -1, derivative, v, number_of_components)
                if result != ZINC_OK:
                    success = False
                else:
                    new_values = matrixvectormult(rotation, values)
                    result = fe_field.setNodeParameters(cache, -1, derivative, v, new_values)
                    if result != ZINC_OK:
                        success = False
        node = node_iter.next()
    fm.endChange()
    if not success:
        print('zincutils.transformCoordinates: failed to get/set some values')
    return success


def offset_scaffold(field, offset):
    number_of_components = field.getNumberOfComponents()
    if (number_of_components != 2) and (number_of_components != 3):
        print('zincutils.offset_scaffold: field has invalid number of components')
        return False
    if len(offset) != number_of_components:
        print('zincutils.offset_scaffold: invalid matrix number of columns or offset size')
        return False
    if field.getCoordinateSystemType() != Field.COORDINATE_SYSTEM_TYPE_RECTANGULAR_CARTESIAN:
        print('zincutils.offset_scaffold: field is not rectangular cartesian')
        return False
    fe_field = field.castFiniteElement()
    if not fe_field.isValid():
        print('zincutils.transformCoordinates: field is not finite element field type')
        return False
    success = True
    fm = field.getFieldmodule()
    fm.beginChange()
    cache = fm.createFieldcache()
    nodes = fm.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
    node_template = nodes.createNodetemplate()
    node_iter = nodes.createNodeiterator()
    node = node_iter.next()
    while node.isValid():
        node_template.defineFieldFromNode(fe_field, node)
        cache.setNode(node)
        for derivative in [Node.VALUE_LABEL_VALUE, Node.VALUE_LABEL_D_DS1, Node.VALUE_LABEL_D_DS2,
                           Node.VALUE_LABEL_D2_DS1DS2, Node.VALUE_LABEL_D_DS3, Node.VALUE_LABEL_D2_DS1DS3,
                           Node.VALUE_LABEL_D2_DS2DS3, Node.VALUE_LABEL_D3_DS1DS2DS3]:
            versions = node_template.getValueNumberOfVersions(fe_field, -1, derivative)
            for v in range(1, versions + 1):
                result, values = fe_field.getNodeParameters(cache, -1, derivative, v, number_of_components)
                if result != ZINC_OK:
                    success = False
                else:
                    if derivative == Node.VALUE_LABEL_VALUE:
                        new_values = add(values, offset)
                    else:
                        new_values = values
                    result = fe_field.setNodeParameters(cache, -1, derivative, v, new_values)
                    if result != ZINC_OK:
                        success = False
        node = node_iter.next()
    fm.endChange()
    if not success:
        print('zincutils.offset_scaffold: failed to get/set some values')
    return success
