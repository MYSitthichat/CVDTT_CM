from PySide6.QtWidgets import QWidget
from View.template_from_ui.Doctor_report_frame import Ui_Doctor_Form

class DoctorReportView(QWidget):
    def __init__(self, parent=None):
        super(DoctorReportView, self).__init__(parent)
        self.ui = Ui_Doctor_Form()
        self.ui.setupUi(self)
        self.progress_value = 0
        # Signal connection moved to controller
        self.setup_ui()
        
    def setup_ui(self):
        self.ui.stuck_order_lineEdit.setReadOnly(True)
        self.ui.number_report_lineEdit.setReadOnly(True)