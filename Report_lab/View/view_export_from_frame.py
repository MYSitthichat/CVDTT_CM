from PySide6.QtWidgets import QWidget
from View.template_from_ui.Export_form_frame import Ui_MergForm

class ExportFormView(QWidget):
    def __init__(self, parent=None):
        super(ExportFormView, self).__init__(parent)
        self.ui = Ui_MergForm()
        self.ui.setupUi(self)
        self.ui.show_report_progressBar.setVisible(True)
        self.ui.show_report_progressBar.setValue(0)
        self.progress_value = 0
        # Signal connection moved to controller

