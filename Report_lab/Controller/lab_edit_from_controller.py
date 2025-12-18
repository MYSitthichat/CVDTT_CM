from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject
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
        QMessageBox.information(self.view, "Information", "Edit Form Button Clicked")

    def download_pushButton_clicked(self):
        QMessageBox.information(self.view, "Information", "Download Button Clicked")

    def delete_pushButton_clicked(self):
        QMessageBox.information(self.view, "Information", "Delete Button Clicked")

    def save_new_lab_pushButton_clicked(self):
        QMessageBox.information(self.view, "Information", "Save New Lab Button Clicked")

    def save_form_pushButton_clicked(self):
        QMessageBox.information(self.view, "Information", "Save Form Button Clicked")