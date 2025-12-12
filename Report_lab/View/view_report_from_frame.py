from PySide6.QtWidgets import QWidget
from View.template_from_ui.send_report_pdf_frame import Ui_Report_Form

class ReportFormView(QWidget):
    def __init__(self, parent=None):
        super(ReportFormView, self).__init__(parent)
        self.ui = Ui_Report_Form()
        self.ui.setupUi(self)
        # Signal connection moved to controller

