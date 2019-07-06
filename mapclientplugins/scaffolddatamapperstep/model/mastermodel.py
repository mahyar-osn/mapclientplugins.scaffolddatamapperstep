from opencmiss.zinc.context import Context

from .scaffoldmodel import ScaffoldModel
from .datamodel import DataModel


class MasterModel(object):

    def __init__(self, scaffold_path, ex_data_path, ephys_data_path=None):
        self._context = Context('ScaffoldDataMapper')
        self._material_module = self._context.getMaterialmodule()
        self._region = self._context.createRegion()
        self._region.setName('DataMapperRegion')

        self._scaffold_path = scaffold_path
        self._ex_data_path = ex_data_path
        self._ephys_data_path = ephys_data_path if ephys_data_path is not None else None

        self._scaffold_model = ScaffoldModel(self._region, self._material_module, self._scaffold_path)
        self._data_model = DataModel(self._region, self._material_module, self._ex_data_path, self._ephys_data_path)

        self._initialise_glyph_material()
        self._initialise_tessellation(12)

    def get_context(self):
        return self._context

    def get_region(self):
        return self._region

    def initialise_graphics(self):
        self._scaffold_model.create_scaffold_graphics()
        self._data_model.create_data_graphics()

    def _initialise_glyph_material(self):
        self._glyph_module = self._context.getGlyphmodule()
        self._glyph_module.defineStandardGlyphs()

    def _initialise_tessellation(self, res):
        self._tessellationmodule = self._context.getTessellationmodule()
        self._tessellationmodule = self._tessellationmodule.getDefaultTessellation()
        self._tessellationmodule.setRefinementFactors([res])

    def rotate_scaffold(self, angle, value):
        self._scaffold_model.rotate_scaffold(angle, value)

    def translate_scaffold(self, axis, value, rate):
        self._scaffold_model.translate_scaffold(axis, value, rate)
