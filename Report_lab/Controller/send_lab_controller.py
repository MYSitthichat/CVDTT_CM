from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QFileDialog
from PySide6.QtCore import QObject, Qt
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
        
        
        
    def clear_pushButton_clicked(self):
        print("CLEAR BUTTON CLICKED - SendLabController")
        
    def send_pushButton_clicked(self):
        print("SEND BUTTON CLICKED - SendLabController")
        
    def browse_file_clicked(self):
        print("BROWSE FILE BUTTON CLICKED - SendLabController")

    def convert_to_pdf_clicked(self):
        print("CONVERT TO PDF BUTTON CLICKED - SendLabController")