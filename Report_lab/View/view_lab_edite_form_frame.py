from PySide6.QtWidgets import QWidget
from View.template_from_ui.lab_edit_form_frame import Ui_lab_Edite_form_Form

class LabEditFormView(QWidget):
    def __init__(self, parent=None):
        super(LabEditFormView, self).__init__(parent)
        self.ui = Ui_lab_Edite_form_Form()
        self.ui.setupUi(self)
        # Signal connection moved to controller

