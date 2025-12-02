from View.view_main_frame import MainWindow
from PySide6.QtCore import QObject, Signal, QTimer
from Controller.new_register_controller import NewRegisterController
from Controller.new_work_controller import NewWorkController
from Controller.barcode_page_controller import BarcodePageController
from Controller.check_job_progress_controller import CheckJobProgressController
from Controller.lab_received_sample_controller import LabReceivedSampleController
from View.view_new_work_frame import AddNewWorkWidget

class MainController(QObject):
    # Define signals
    show_add_work_page_signal = Signal()

    def __init__(self, login_controller=None):
        super(MainController, self).__init__()
        
        # Store logged-in user information
        self.logged_in_user_id = None
        self.logged_in_username = None
        self.logged_in_user_info = None
        
        # Create widgets here to prevent duplicate creation
        self.add_work_widget = AddNewWorkWidget()
        
        # db_model = login_controller.model if login_controller else None
        self.main_window = MainWindow(add_work_widget=self.add_work_widget)
        
        # Set reference to this controller in main_window
        self.main_window.main_controller = self
        
        # Create ALL controllers here to prevent duplicate creation
        self.new_register_controller = NewRegisterController(self.main_window.register_widget)
        self.new_work_controller = NewWorkController(self.add_work_widget, self.main_window, self)
        self.barcode_controller = BarcodePageController(None, self.main_window.barcode_widget)
        self.check_job_controller = CheckJobProgressController(None, self.main_window.check_job_widget)
        self.lab_received_controller = LabReceivedSampleController(None, self.main_window.lab_received_widget)
        
        # Connect Signal to NewWorkController
        self.show_add_work_page_signal.connect(self.new_work_controller.setup_ui)
        
        self.login_controller = login_controller
        
        # Connect buttons
        self.main_window.ui.logout_pushButton.clicked.connect(self.logout_pushButton_clicked)
        self.main_window.ui.register_new_customer_pushButton.clicked.connect(self.show_register_page)
        
        if hasattr(self.main_window.ui, 'new_work_pushButton'):
            self.main_window.ui.new_work_pushButton.clicked.connect(self.show_add_work_page)

    def Show_main_page(self):
        self.main_window.Show_main_page()

    def hide_main_page(self):
        self.main_window.hide()
    
    def logout_pushButton_clicked(self):
        self.main_window.hide()  # Hide the main window
        if self.login_controller:
            # Delay 500ms before showing login page
            self.set_logged_in_user(user_id=None)
            QTimer.singleShot(100, self.show_login_after_logout)
    
    def show_login_after_logout(self):
        if self.login_controller:
            self.login_controller.clear_login_form()
            self.login_controller.Show_login_page()
    
    def show_register_page(self):
        self.main_window.show_register_page()
    
    def show_add_work_page(self):
        self.main_window.show_add_work_page()
        
        self.show_add_work_page_signal.emit()
    
    def set_logged_in_user(self, user_id):
        self.logged_in_user_id = user_id
        # print(f"User logged in: ID={user_id}")
    
    def get_user_login_id(self):
        """Get the logged-in user ID"""
        return self.logged_in_user_id
    
    def get_logged_in_user_id(self):
        """Get the logged-in user ID"""
        return self.logged_in_user_id
    
    def get_logged_in_username(self):
        """Get the logged-in username"""
        return self.logged_in_username
    
    def get_logged_in_user_info(self):
        """Get the full logged-in user information"""
        return self.logged_in_user_info