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
        
        # Create main window
        self.main_window = MainWindow()
        
        # Set reference to this controller in main_window
        self.main_window.main_controller = self
        
        self.login_controller = login_controller
        
        # Connect User Profile Widget buttons (แทนที่ปุ่ม logout เดิม)
        self._setup_user_profile_connections()

    def _setup_user_profile_connections(self):
        # Connect user profile widget if available
        if hasattr(self.main_window, 'get_user_profile_widget'):
            user_widget = self.main_window.get_user_profile_widget()
            if user_widget and hasattr(user_widget, 'popup') and user_widget.popup:
                user_widget.popup.btn_logout.clicked.connect(self.logout_pushButton_clicked)
        
        # Connect logout button if available
        if hasattr(self.main_window, 'ui') and hasattr(self.main_window.ui, 'logout_pushButton'):
            self.main_window.ui.logout_pushButton.clicked.connect(self.logout_pushButton_clicked)
        
        # Connect register button if available
        if hasattr(self.main_window, 'ui') and hasattr(self.main_window.ui, 'register_new_customer_pushButton'):
            self.main_window.ui.register_new_customer_pushButton.clicked.connect(self.show_register_page)
        
        # Connect new work button if available
        if hasattr(self.main_window, 'ui') and hasattr(self.main_window.ui, 'new_work_pushButton'):
            self.main_window.ui.new_work_pushButton.clicked.connect(self.show_add_work_page)

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
    
    def show_register_page(self):
        if hasattr(self.main_window, 'show_register_page'):
            self.main_window.show_register_page()
    
    def show_add_work_page(self):
        if hasattr(self.main_window, 'show_add_work_page'):
            self.main_window.show_add_work_page()
            self.show_add_work_page_signal.emit()
    
    def set_logged_in_user(self, user_id):
        self.logged_in_user_id = user_id
        if hasattr(self, 'edit_employee_controller') and self.edit_employee_controller and user_id is not None:
            self.edit_employee_controller.set_current_user(user_id)
    
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
            group_id = user_info.get('group_id')
            self._update_edit_employee_button_visibility(group_id)
            if hasattr(self.main_window, 'user_profile_widget') and self.main_window.user_profile_widget:
                self.main_window.user_profile_widget.update_user_info(full_name, role, employee_id)
                if self.main_window.user_profile_widget.popup:
                    self.main_window.user_profile_widget.popup.set_user_data(
                        full_name, role, employee_id, email
                    )
        if hasattr(self, 'edit_employee_controller') and self.edit_employee_controller and user_id is not None:
            self.edit_employee_controller.set_current_user(user_id)
    
    def _update_edit_employee_button_visibility(self, group_id):
        if hasattr(self.main_window, 'ui') and hasattr(self.main_window.ui, 'edit_employee_pushButton'):
            if group_id is not None and group_id <= 2:
                self.main_window.ui.edit_employee_pushButton.show()
            else:
                self.main_window.ui.edit_employee_pushButton.hide()
    
    def get_user_login_id(self):
        return self.logged_in_user_id
    
    def get_logged_in_user_id(self):
        return self.logged_in_user_id
