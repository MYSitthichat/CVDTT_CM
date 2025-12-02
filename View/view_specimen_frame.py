from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QDateTime, QTimer
from View.template_from_ui.specimen_frame import Ui_specimen_MainWindow


class SpecimenWidget(QWidget,Ui_specimen_MainWindow):
    def __init__(self, parent=None):
        super(SpecimenWidget, self).__init__(parent)
        self.ui = Ui_specimen_MainWindow()
        from PySide6.QtWidgets import QMainWindow
        dummy_main_window = QMainWindow()
        self.ui.setupUi(dummy_main_window)
        
        from PySide6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.centralwidget)
        self.setLayout(layout)
        self.setup_ui_specimen()
        self.set_current_datetime()  # Set current date/time on init
        
        # Setup timer to update datetime every second
        self.set_current_datetime()

    def setup_ui_specimen(self):
        # print("Setting up Specimen UI")
        self.ui.specimen_fungal_pushButton.setDisabled(True)
        self.ui.specimen_cytology_pushButton.setDisabled(True)
        self.ui.specimen_necropsy_pushButton.setDisabled(True)
        self.ui.specimen_serology_pushButton.setDisabled(True)
        self.ui.specimen_virology_pushButton.setDisabled(True)
        self.ui.specimen_hematology_pushButton.setDisabled(True)
        self.ui.specimen_food_safety_pushButton.setDisabled(True)
        self.ui.specimen_feed_analysis_pushButton.setDisabled(True)
        self.ui.specimen_water_quality_pushButton.setDisabled(True)
        self.ui.specimen_surgical_biopsy_pushButton.setDisabled(True)
        self.ui.specimen_immunohistochemistry_pushButton.setDisabled(True)
        self.ui.specimen_histopathology_research_pushButton.setDisabled(True)
        self.ui.specimen_histopathology_research_recut_pushButton.setDisabled(True)
        self.ui.specimen_histopathology_pushButton.setDisabled(True)
        self.ui.specimen_parasitology_pushButton.setDisabled(True)
        self.ui.specimen_microbiology_pushButton.setDisabled(True)
        self.ui.specimen_molecular_biology_pushButton.setDisabled(True)
        self.ui.specimen_service_after_death_pushButton.setDisabled(True)
    
    def save_button_clicked(self):
        self.ui.specimen_parasitology_pushButton.setDisabled(False)
        self.ui.specimen_microbiology_pushButton.setDisabled(False)
        self.ui.specimen_molecular_biology_pushButton.setDisabled(False)
        self.ui.specimen_service_after_death_pushButton.setDisabled(False)
    
    def cancel_button_clicked(self):
        self.ui.specimen_parasitology_pushButton.setDisabled(True)
        self.ui.specimen_microbiology_pushButton.setDisabled(True)
        self.ui.specimen_molecular_biology_pushButton.setDisabled(True)
        self.ui.specimen_service_after_death_pushButton.setDisabled(True)
    
    def set_current_datetime(self):
        current_datetime = QDateTime.currentDateTime()
        if hasattr(self.ui, 'specimen_day_of_death_dateTimeEdit'):
            self.ui.specimen_day_of_death_dateTimeEdit.setDateTime(current_datetime)
        if hasattr(self.ui, 'specimen_day_keep_sample_dateTimeEdit'):
            self.ui.specimen_day_keep_sample_dateTimeEdit.setDateTime(current_datetime)
            
    def update_datetime_to_now(self):
        self.set_current_datetime()


