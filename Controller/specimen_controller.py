from View.view_specimen_frame import SpecimenWidget
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox
import pyodbc
from datetime import datetime


class SpecimenController(QObject):
    """Controller for Specimen Page - copied from lab_manager"""
    
    def __init__(self, view: SpecimenWidget, parent=None):
        super().__init__(parent)
        self.view = view
        self.main_window = parent  # Store reference to main window
        self.case_registration_id = None  # Store the case registration ID
        self.bind_specimen_events()
        # print("SpecimenController initialized")
    
    def bind_specimen_events(self):
        # Save and cancel buttons
        self.view.ui.specimen_save_pushButton.clicked.connect(self.save_specimen_information)
        self.view.ui.specimen_cancel_pushButton.clicked.connect(self.cancel_specimen)
        
        # Lab navigation buttons
        self.view.ui.specimen_molecular_biology_pushButton.clicked.connect(self.goto_molecular_biology)
        self.view.ui.specimen_microbiology_pushButton.clicked.connect(self.goto_microbiology)
        self.view.ui.specimen_parasitology_pushButton.clicked.connect(self.goto_parasitology)
        self.view.ui.specimen_service_after_death_pushButton.clicked.connect(self.goto_after_death)
    
    def save_specimen_information(self):
        self.view.save_button_clicked()
        print(f"save_specimen_information called - Case ID: {self.case_registration_id}")
    
    def get_specimen_data(self):
        # """Get all data from specimen form"""
        # # Determine animal type from radio buttons
        # animal_type = ""
        # if self.view.ui.specimen_swine_radioButton.isChecked():
        #     animal_type = "สุกร (Swine)"
        # elif self.view.ui.specimen_avian_radioButton.isChecked():
        #     animal_type = "สัตว์ปีก (Avian)"
        # elif self.view.ui.specimen_bovine_radioButton.isChecked():
        #     animal_type = "โค (Bovine)"
        # elif self.view.ui.specimen_equine_radioButton.isChecked():
        #     animal_type = "ม้า (Equine)"
        # elif self.view.ui.specimen_conine_radioButton.isChecked():
        #     animal_type = "สุนัข (Conine)"
        # elif self.view.ui.specimen_elephant_radioButton.isChecked():
        #     animal_type = "ช้าง (Elephant)"
        # elif self.view.ui.specimen_felin_radioButton.isChecked():
        #     animal_type = "แมว (Felin)"
        # elif self.view.ui.specimen_unknown_radioButton.isChecked():
        #     animal_type = "Unknow"
        # elif self.view.ui.specimen_animal_other_radioButton.isChecked():
        #     animal_type = f"อื่นๆ: {self.view.ui.specimen_animal_other_lineEdit.text()}"
        
        # # Determine status
        # status = "ปกติ" if self.view.ui.specimen_normal_radioButton.isChecked() else "ด่วนที่สุด"
        
        # # Determine keeping method
        # keeping = ""
        # if self.view.ui.specimen_chill_radioButton.isChecked():
        #     keeping = "แช่เย็น (Chill)"
        # elif self.view.ui.specimen_freeze_radioButton.isChecked():
        #     keeping = "แช่แข็ง (Freeze)"
        # elif self.view.ui.specimen_room_temperature_radioButton.isChecked():
        #     keeping = "ไม่แช่ (Room Temperature)"
        
        # # Get sample type
        # sample = self.view.ui.specimen_sample_comboBox.currentText()
        # if self.view.ui.specimen_sample_other_radioButton.isChecked():
        #     sample = f"อื่นๆ: {self.view.ui.specimen_sample_other_lineEdit.text()}"
        
        # return {
        #     'name': self.view.ui.specimen_name_lineEdit.text(),
        #     'specimen_id': self.view.ui.specimen_ID_lineEdit.text(),
        #     'sex': self.view.ui.specimen_sex_comboBox.currentText(),
        #     'age_year': self.view.ui.specimen_ageYear_lineEdit.text(),
        #     'age_month': self.view.ui.specimen_ageMonth_lineEdit.text(),
        #     'age_day': self.view.ui.specimen_ageDay_lineEdit.text(),
        #     'age_unknown': self.view.ui.specimen_ageUnknown_checkBox.isChecked(),
        #     'animal_type': animal_type,
        #     'breed': self.view.ui.specimen_breed_lineEdit.text(),
        #     'weight': self.view.ui.specimen_weight_lineEdit.text(),
        #     'death_cause': self.view.ui.specimen_death_comboBox.currentText(),
        #     'death_date': self.view.ui.specimen_day_of_death_dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
        #     'sample_date': self.view.ui.specimen_day_keep_sample_dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
        #     'sample_type': sample,
        #     'keeping_method': keeping,
        #     'status': status,
        #     'treatment_history': self.view.ui.specimen_record_heal_textEdit.toPlainText(),
        #     'antibiotics_history': self.view.ui.specimen_record_antibiotics_textEdit.toPlainText()
        # }
        pass
    
    
    def clear_specimen_information(self):
        print("Clearing specimen information")
    
    def cancel_specimen(self):
        self.view.cancel_button_clicked()
        if self.main_window and hasattr(self.main_window, 'add_work_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.add_work_widget)
        else:
            print("Warning: Cannot navigate back to new work page")
    
    def goto_molecular_biology(self):
        print("Navigate to Molecular Biology page")
        if self.main_window and hasattr(self.main_window, 'molecular_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.molecular_widget)
            if hasattr(self.main_window.molecular_widget, 'clear_page'):
                self.main_window.molecular_widget.clear_page()
        else:
            print("Warning: Cannot navigate to molecular biology page")

    def goto_microbiology(self):
        print("Navigate to Microbiology page")
        if self.main_window and hasattr(self.main_window, 'bacteria_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.bacteria_widget)
        else:
            print("Warning: Cannot navigate to microbiology page")
    
    def goto_parasitology(self):
        print("Navigate to Parasitology page")
        if self.main_window and hasattr(self.main_window, 'parasite_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.parasite_widget)
        else:
            print("Warning: Cannot navigate to parasitology page")
    
    def goto_after_death(self):
        print("Navigate to After Death Service page")
        if self.main_window and hasattr(self.main_window, 'after_death_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.after_death_widget)
            if hasattr(self.main_window.after_death_widget, 'clear_page'):
                self.main_window.after_death_widget.clear_page()
        else:
            print("Warning: Cannot navigate to after death page")
    
    def set_case_registration_id(self, case_id):
        """Set the case registration ID from new work page"""
        self.case_registration_id = case_id
        print(f"case_registration_id: {case_id}")
    
    def get_case_registration_id(self):
        """Get the current case registration ID"""
        return self.case_registration_id

