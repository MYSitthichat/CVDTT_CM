from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject
from View.view_report_from_frame import ReportFormView

class SendLabController(QObject):
    """ Controller for the Send Lab Page """

    def __init__(self, view: ReportFormView):
        super().__init__()
        self.view: ReportFormView = view
        self._setup_connections()
    
    def _setup_connections(self):
        self.view.ui.search_location_file_pushButton.clicked.connect(self.browse_file_clicked)
        self.view.ui.clear_location_file_pushButton.clicked.connect(self.clear_pushButton_clicked)
        self.view.ui.send_report_file_pushButton.clicked.connect(self.send_pushButton_clicked)
        self.view.ui.convert_word_to_pdf_pushButton.clicked.connect(self.convert_to_pdf_clicked)
        self.view.ui.select_barcode_pushButton.clicked.connect(self.select_barcode_clicked)
        

    def select_barcode_clicked(self):
        QMessageBox.information(self.view, "Information", "Select Barcode Button Clicked")
        
    def clear_pushButton_clicked(self):
        QMessageBox.information(self.view, "Information", "Clear Button Clicked")
        
    def send_pushButton_clicked(self):
        QMessageBox.information(self.view, "Information", "Send Button Clicked")
        
    def browse_file_clicked(self):
        QMessageBox.information(self.view, "Information", "Browse File Button Clicked")

    def convert_to_pdf_clicked(self):
        QMessageBox.information(self.view, "Information", "Convert To PDF Button Clicked")