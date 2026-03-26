from PySide6.QtWidgets import QWidget
from View.template_from_ui.monocular_form import Ui_Report_Form

class MonocularFormView(QWidget):
    def __init__(self, parent=None):
        super(MonocularFormView, self).__init__(parent)
        self.ui = Ui_Report_Form()
        self.ui.setupUi(self)
        # Signal connection moved to controller
