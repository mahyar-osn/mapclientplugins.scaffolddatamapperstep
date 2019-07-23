from PySide import QtCore, QtGui

from .ui_scaffolddatamapperwidget import Ui_ScaffoldDataMapper
from .datamappersceneviewerwidget import DataMapperSceneviewerWidget


class ScaffoldDataMapperWidget(QtGui.QWidget):

    def __init__(self, master_model, shareable_widget=None, parent=None):
        super(ScaffoldDataMapperWidget, self).__init__(parent)

        self._model = master_model
        self._ui = Ui_ScaffoldDataMapper()
        self._ui.setupUi(self)
        self._ui.sceneviewerWidget.setContext(self._model.get_context())

        self._done_callback = None
        self._settings = {'view-parameters': {}}
        self._model.set_model_settings_change_callback(self._setting_display)
        self._make_connections()

    def _make_connections(self):
        self._ui.sceneviewerWidget.graphicsInitialized.connect(self._graphics_initialized)
        self._ui.doneButton.clicked.connect(self._done_clicked)
        self._ui.viewAllButton.clicked.connect(self._view_all)
        self._ui.yaw_doubleSpinBox.valueChanged.connect(self._yaw_clicked)
        self._ui.pitch_doubleSpinBox.valueChanged.connect(self._pitch_clicked)
        self._ui.roll_doubleSpinBox.valueChanged.connect(self._roll_clicked)
        self._ui.positionX_doubleSpinBox.valueChanged.connect(self._x_clicked)
        self._ui.positionY_doubleSpinBox.valueChanged.connect(self._y_clicked)
        self._ui.positionZ_doubleSpinBox.valueChanged.connect(self._z_clicked)
        self._ui.manualMapping_radioButton.clicked.connect(self._manual_mapping_selected)
        self._ui.automaticMapping_radioButton.clicked.connect(self._auto_mapping_selected)
        self._ui.createNode_checkBox.clicked.connect(self._create_node_selected)
        self._ui.checkBox.clicked.connect(self._select_node_selected)

    def _graphics_initialized(self):
        scene_viewer = self._ui.sceneviewerWidget.getSceneviewer()

        if scene_viewer is not None:
            scene = self._model.get_scene()
            self._ui.sceneviewerWidget.setScene(scene)

            if len(self._settings['view-parameters']) == 0:
                self._view_all()
            else:
                eye = self._settings['view-parameters']['eye']
                look_at = self._settings['view-parameters']['look_at']
                up = self._settings['view-parameters']['up']
                angle = self._settings['view-parameters']['angle']
                self._ui.sceneviewerWidget.setViewParameters(eye, look_at, up, angle)
                self._view_all()

    def _view_all(self):
        if self._ui.sceneviewerWidget.getSceneviewer() is not None:
            self._ui.sceneviewerWidget.viewAll()

    def _done_clicked(self):
        self._done_callback()

    def register_done_execution(self, done_callback):
        self._done_callback = done_callback

    def _yaw_clicked(self):
        value = self._ui.yaw_doubleSpinBox.value()
        self._model.rotate_scaffold('yaw', value)

    def _pitch_clicked(self):
        value = self._ui.pitch_doubleSpinBox.value()
        self._model.rotate_scaffold('pitch', value)

    def _roll_clicked(self):
        value = self._ui.roll_doubleSpinBox.value()
        self._model.rotate_scaffold('roll', value)

    def _x_clicked(self):
        value = self._ui.positionX_doubleSpinBox.value()
        rate = self._ui.rateOfChange_horizontalSlider.value()
        self._model.translate_scaffold('X', value, rate)

    def _y_clicked(self):
        value = self._ui.positionY_doubleSpinBox.value()
        rate = self._ui.rateOfChange_horizontalSlider.value()
        self._model.translate_scaffold('Y', value, rate)

    def _z_clicked(self):
        value = self._ui.positionZ_doubleSpinBox.value()
        rate = self._ui.rateOfChange_horizontalSlider.value()
        self._model.translate_scaffold('Z', value, rate)

    def _setting_display(self):
        self._display_real(self._ui.yaw_doubleSpinBox, self._model.get_model_yaw_value())
        self._display_real(self._ui.pitch_doubleSpinBox, self._model.get_model_pitch_value())
        self._display_real(self._ui.roll_doubleSpinBox, self._model.get_model_roll_value())
        self._display_real(self._ui.positionX_doubleSpinBox, self._model.get_model_X_value())
        self._display_real(self._ui.positionY_doubleSpinBox, self._model.get_model_Y_value())
        self._display_real(self._ui.positionZ_doubleSpinBox, self._model.get_model_Z_value())

    @staticmethod
    def _display_real(widget, value):
        new_text = '{:.4g}'.format(value)
        if isinstance(widget, QtGui.QDoubleSpinBox):
            widget.setValue(value)
        else:
            widget.setText(new_text)

    def _manual_mapping_selected(self):
        self._ui.createNode_checkBox.setEnabled(True)

    def _create_node_selected(self):
        self._ui.checkBox.setEnabled(False) if self._ui.createNode_checkBox.isChecked() else\
            self._ui.checkBox.setEnabled(True)

    def _select_node_selected(self):
        if self._ui.checkBox.isChecked():
            self._ui.createNode_checkBox.setEnabled(False)
        else:
            self._ui.createNode_checkBox.setEnabled(True)
        self._model.get_selection_data_location(self._ui.sceneviewerWidget.getOrCreateSelectionGroup())

    def _auto_mapping_selected(self):
        if self._ui.automaticMapping_radioButton.isChecked():
            self._ui.createNode_checkBox.setEnabled(False)
