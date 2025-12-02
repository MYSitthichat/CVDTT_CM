from PySide6.QtWidgets import QMainWindow
from View.template_from_ui.main_frame import Ui_MainWindow
from View.view_register_new_customer_frame import RegisterNewCustomerWidget
from View.view_new_work_frame import AddNewWorkWidget
from View.view_barcode_page import BarcodePageWidget
from View.view_check_jop_progress import CheckJobProgressWidget
from View.view_lab_received_sample import LabReceivedSampleWidget
from Controller.new_work_controller import NewWorkController
from Controller.barcode_page_controller import BarcodePageController
from Controller.check_job_progress_controller import CheckJobProgressController
from Controller.lab_received_sample_controller import LabReceivedSampleController
from View.view_bacteria_frame import bacterieFrameView
from Controller.bacteria_controller import BacteriaController
from View.view_parasite_frame import parasiteFrameView
from Controller.parasite_controller import ParasiteController
from View.view_specimen_frame import SpecimenWidget
from Controller.specimen_controller import SpecimenController
from View.view_edit_employee_frame import EditEmployeeWindow
from View.view_molecular_biology import MolecularBiologyPageWidget
from Controller.molecular_biology_controller import MolecularBiologyController
from View.view_after_death import AfterDeathPageWidget
from Controller.after_death_controller import AfterDeathPageController
from View.view_lab_report import LabReportPageWidget
from Controller.lab_report_controller import LabReportPageController
class MainWindow(QMainWindow):
    
    def __init__(self, parent=None, model=None, add_work_widget=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # --- Setup Pages (Widgets Only) ---
        # Controllers will be created by MainController
        self.register_widget = RegisterNewCustomerWidget()
        # add_work_widget is passed from MainController to prevent duplicate creation
        self.add_work_widget = add_work_widget if add_work_widget is not None else AddNewWorkWidget()
        self.barcode_widget = BarcodePageWidget()
        self.check_job_widget = CheckJobProgressWidget()
        self.lab_received_widget = LabReceivedSampleWidget() 
        self.bacteria_widget = bacterieFrameView()
        self.parasite_widget = parasiteFrameView()
        self.specimen_widget = SpecimenWidget()
        self.edit_employee_widget = EditEmployeeWindow()
        self.molecular_widget = MolecularBiologyPageWidget()
        self.after_death_widget = AfterDeathPageWidget()
        self.lab_report_widget = LabReportPageWidget()

        # --- Setup Controllers ---
        # NewWorkController is now created in MainController
        self.barcode_controller = BarcodePageController(self.barcode_widget)
        self.check_job_controller = CheckJobProgressController(model, self.check_job_widget)
        self.lab_received_controller = LabReceivedSampleController(model, self.lab_received_widget)
        self.bacteria_controller = BacteriaController(self.bacteria_widget, self)
        self.parasite_controller = ParasiteController(self.parasite_widget, self)
        self.specimen_controller = SpecimenController(self.specimen_widget, self)
        self.molecular_controller = MolecularBiologyController(model, self.molecular_widget, self)
        self.after_death_controller = AfterDeathPageController(model, self.after_death_widget, self)
        self.lab_report_controller = LabReportPageController(model, self.lab_report_widget, self)

        self.setup_stacked_widget()
        
        # --- Link Buttons ---
        self.ui.register_new_customer_pushButton.clicked.connect(self.show_register_page)
        # self.ui.new_work_pushButton.clicked.connect(self.show_add_work_page)
        
        if hasattr(self.ui, 'barcode_print_pushButton'):
            self.ui.barcode_print_pushButton.clicked.connect(self.show_barcode_page)
            
        if hasattr(self.ui, 'check_job_pushButton'):
            self.ui.check_job_pushButton.clicked.connect(self.show_check_job_page)

        if hasattr(self.ui, 'lab_received_pushButton'):
            self.ui.lab_received_pushButton.clicked.connect(self.show_lab_received_page)
        else:
            print("Error: Could not find 'lab_received_pushButton' in Ui_MainWindow")

        if hasattr(self.ui, 'specimen_pushButton'):
            self.ui.specimen_pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.specimen_widget))

        if hasattr(self.ui, 'edit_employee_pushButton'):
            self.ui.edit_employee_pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.edit_employee_widget))

        
        if hasattr(self.ui, 'lab_report_pushButton'):
            self.ui.lab_report_pushButton.clicked.connect(self.show_lab_report_page)
        else:
            print("Warning: 'lab_report_pushButton' not found")

        self.show_register_page()


    def setup_stacked_widget(self):
        while self.ui.stackedWidget.count() > 0:
            old_widget = self.ui.stackedWidget.widget(0)
            self.ui.stackedWidget.removeWidget(old_widget)
        
        self.ui.stackedWidget.addWidget(self.register_widget)
        self.ui.stackedWidget.addWidget(self.add_work_widget)
        self.ui.stackedWidget.addWidget(self.barcode_widget)
        self.ui.stackedWidget.addWidget(self.check_job_widget)
        self.ui.stackedWidget.addWidget(self.lab_received_widget)
        self.ui.stackedWidget.addWidget(self.bacteria_widget)
        self.ui.stackedWidget.addWidget(self.parasite_widget)
        self.ui.stackedWidget.addWidget(self.specimen_widget)
        self.ui.stackedWidget.addWidget(self.edit_employee_widget)
        self.ui.stackedWidget.addWidget(self.molecular_widget)
        self.ui.stackedWidget.addWidget(self.after_death_widget)
        self.ui.stackedWidget.addWidget(self.lab_report_widget)


    def show_register_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.register_widget)
        self.register_widget.ui.Add_new_costumer_private_radioButton.setChecked(True)
        # self.register_widget.set_middle_name_status(False)
        # self.register_widget.ui.mid_name_checkBox.setChecked(False)

    def show_add_work_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.add_work_widget)
        
    def show_barcode_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.barcode_widget)

    def show_check_job_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.check_job_widget)

    def show_lab_received_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.lab_received_widget)

    def show_molecular_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.molecular_widget)
        # self.molecular_widget.clear_molecular_biology_page()

    def show_after_death_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.after_death_widget)
        self.after_death_widget.clear_page()

    def show_lab_report_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.lab_report_widget)
        self.lab_report_widget.clear_page()

    def Show_main_page(self):
        self.show()

    def hide(self):
        super().hide()