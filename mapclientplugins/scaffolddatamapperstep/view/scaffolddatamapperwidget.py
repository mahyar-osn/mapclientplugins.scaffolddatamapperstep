from PySide import QtGui

from .ui_scaffolddatamapperwidget import Ui_ScaffoldDataMapper


class ScaffoldDataMapperWidget(QtGui.QWidget):

    def __init__(self, master_model, shareable_widget=None, parent=None):
        super(ScaffoldDataMapperWidget, self).__init__(parent)

        self._model = master_model
        self._ui = Ui_ScaffoldDataMapper()
        self._ui.setupUi(self)
        self._ui.sceneviewerWidget.setContext(self._model.get_context())

        self._done_callback = None
        self._settings = {'view-parameters': {}}

        self._make_connections()

    def _make_connection(self):
        self._ui.sceneviewerWidget.graphics_initialized.connect(self._graphics_initialized)
        self._ui.doneButton.clicked.connect(self._done_clicked)
        self._ui.viewAllButton.clicked.connect(self._view_all)
        self._ui.yaw_doubleSpinBox.valueChanged.connect(self._yaw_clicked)
        self._ui.pitch_doubleSpinBox.valueChanged.connect(self._pitch_clicked)
        self._ui.roll_doubleSpinBox.valueChanged.connect(self._roll_clicked)
        self._ui.positionX_doubleSpinBox.valueChanged.connect(self._x_clicked)
        self._ui.positionY_doubleSpinBox.valueChanged.connect(self._y_clicked)
        self._ui.positionZ_doubleSpinBox.valueChanged.connect(self._z_clicked)

    def _graphics_initialized(self):
        scene_viewer = self._ui.sceneviewerWidget.get_zinc_sceneviewer()

        if scene_viewer is not None:
            scene = self._model.get_scaffold_scene()
            self._ui.sceneviewerWidget.set_scene(scene)

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
