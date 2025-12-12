from View.view_main_frame import MainWindow
from PySide6.QtCore import QObject, Signal, QTimer

class MainController(QObject):
    # Define signals
    show_add_work_page_signal = Signal()

    def __init__(self, login_controller=None):
        super(MainController, self).__init__()
        
        # Store logged-in user information
        self.logged_in_user_id = None
        self.logged_in_username = None
        self.logged_in_user_info = None
        
        # db_model = login_controller.model if login_controller else None
        self.main_window = MainWindow()
        
        # Set reference to this controller in main_window
        self.main_window.main_controller = self
        
        self.login_controller = login_controller
        
        
        self.main_window.ui.new_work_pushButton.clicked.connect(self.show_receive_work_page)
        self.main_window.ui.register_new_customer_pushButton.clicked.connect(self.show_report_work_page)
        
        self._setup_user_profile_connections()
        
    def show_receive_work_page(self):
        print("MainController: show_receive_work_page called")

    def show_report_work_page(self):
        print("MainController: show_report_work_page called")

    def _setup_user_profile_connections(self):
        user_widget = self.main_window.get_user_profile_widget()
        if user_widget and user_widget.popup:
            user_widget.popup.btn_logout.clicked.connect(self.logout_pushButton_clicked)
        if hasattr(self.main_window.ui, 'logout_pushButton'):
            self.main_window.ui.logout_pushButton.clicked.connect(self.logout_pushButton_clicked)
        

    def Show_main_page(self):
        self.main_window.Show_main_page()

    def hide_main_page(self):
        self.main_window.hide()
    
    def logout_pushButton_clicked(self):
        if hasattr(self.main_window, 'user_profile_widget') and self.main_window.user_profile_widget:
            self.main_window.user_profile_widget.hide_popup_immediately()
        
        self.main_window.hide()
        if self.login_controller:
            self.set_logged_in_user(user_id=None)
            QTimer.singleShot(100, self.show_login_after_logout)
    
    def show_login_after_logout(self):
        if self.login_controller:
            self.login_controller.clear_login_form()
            self.login_controller.Show_login_page()
    
    def set_logged_in_user(self, user_id):
        self.logged_in_user_id = user_id
    
    def set_user_info(self, user_id, username, user_info):
        self.logged_in_user_id = user_id
        self.logged_in_username = username
        self.logged_in_user_info = user_info
        
        if user_info:
            title = user_info.get('title', '')
            name = user_info.get('name', '')
            surname = user_info.get('surname', '')
            full_name = f"{title}{name} {surname}".strip()
            if not full_name:
                full_name = username or 'User'
            role = user_info.get('position', 'Staff')
            employee_id = str(user_id) if user_id else ''
            email = user_info.get('email', '')
            if hasattr(self.main_window, 'user_profile_widget') and self.main_window.user_profile_widget:
                self.main_window.user_profile_widget.update_user_info(full_name, role, employee_id)
                if self.main_window.user_profile_widget.popup:
                    self.main_window.user_profile_widget.popup.set_user_data(
                        full_name, role, employee_id, email
                    )
    
    
    def get_user_login_id(self):
        return self.logged_in_user_id
    
    def get_logged_in_user_id(self):
        return self.logged_in_user_id
