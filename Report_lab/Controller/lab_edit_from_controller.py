from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QFileDialog
from PySide6.QtCore import QObject, Qt
from View.view_lab_edite_form_frame import LabEditFormView

class LabEditFormController(QObject):
    """ Controller for the Lab Edit Form Page """

    def __init__(self, view: LabEditFormView):
        super().__init__()
        self.view: LabEditFormView = view
        self._setup_connections()
    
    def _setup_connections(self):
        self.view.ui.Edte_form_pushButton.clicked.connect(self.edit_form_pushButton_clicked)
        self.view.ui.Download_form_pushButton.clicked.connect(self.download_pushButton_clicked)
        self.view.ui.Delete_form_pushButton.clicked.connect(self.delete_pushButton_clicked)
        self.view.ui.save_form_pushButton.clicked.connect(self.save_form_pushButton_clicked)
        self.view.ui.save_new_lab_pushButton.clicked.connect(self.save_new_lab_pushButton_clicked)


    def edit_form_pushButton_clicked(self):
        print("EDIT FORM BUTTON CLICKED - LabEditFormController")

    def download_pushButton_clicked(self):
        print("DOWNLOAD BUTTON CLICKED - LabEditFormController")

    def delete_pushButton_clicked(self):
        print("DELETE BUTTON CLICKED - LabEditFormController")

    def save_new_lab_pushButton_clicked(self):
        print("SAVE NEW LAB BUTTON CLICKED - LabEditFormController")

    def save_form_pushButton_clicked(self):
        print("SAVE FORM BUTTON CLICKED - LabEditFormController")