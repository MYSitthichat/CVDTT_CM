from View.view_login_frame import LoginWindow
from Controller.main_controller import MainController
from Controller.forgot_password_controller import ForgotPasswordController
from PySide6.QtCore import QObject, QTimer
import sys
from SERVICES_REPORT_LAB.auth_service import AuthService
from SERVICES_REPORT_LAB.employee_service import EmployeeService
from PySide6.QtWidgets import QMessageBox

debug = False

class Login_Controller(QObject):
    
    def __init__(self):
        super(Login_Controller, self).__init__()
        self.login_window = LoginWindow()
        self.main_window = MainController(login_controller=self)
        self.login_api_app = AuthService()
        self.employee_service = EmployeeService()
        self.forgot_password_widget = ForgotPasswordController()
        self.main_window.hide_main_page()
        
        # Store logged-in user information
        self.logged_in_user_id = None
        
        self.login_window.login_pushButton.clicked.connect(self.check_login)
        self.login_window.cancel_pushButton.clicked.connect(self.cancel_login)
        self.login_window.forgot_password_commandLinkButton.clicked.connect(self.show_forgot_password)
        self.forgot_password_widget.return_to_login.connect(self.show_login_from_forgot)
        
        # Connect Enter key press to login
        self.login_window.user_lineEdit.returnPressed.connect(self.check_login)
        self.login_window.password_lineEdit.returnPressed.connect(self.check_login)

    def check_login(self):
        username = self.login_window.user_lineEdit.text()
        password = self.login_window.password_lineEdit.text()
        if debug:
            self.logged_in_user_id = 222
            self.load_and_set_user_info(self.logged_in_user_id, username)
            self.switch_to_main()
        else:
            if username == "" and password == "":
                return False
            user_info = self.login_api_app.login(username, password)
            if user_info:
                self.logged_in_user_id = user_info.get('id') or user_info.get('user_id')
                self.load_and_set_user_info(self.logged_in_user_id, username)
                self.switch_to_main()
                return True
            
            else:
                QMessageBox.warning(
                    self.login_window, 
                    "Login Failed", 
                    "Invalid username or password"
                )
                return False
    
    def load_and_set_user_info(self, user_id, username):
        try:
            employee_data = self.employee_service.get_employee_by_id(user_id)
            
            if employee_data:
                user_info = {
                    'id': employee_data.get('id'),
                    'title': employee_data.get('title', ''),
                    'name': employee_data.get('name', ''),
                    'surname': employee_data.get('surname', ''),
                    'email': employee_data.get('email', ''),
                    'group_id': employee_data.get('group_id'),
                    'position': employee_data.get('position', 'Staff')
                }
                self.get_user_group_id = employee_data.get('group_id', 0)
                self.main_window.set_user_info(user_id, username, user_info)
            else:
                self.main_window.set_logged_in_user(user_id)
        except Exception as e:
            print(f"Error loading user info: {e}")
            self.main_window.set_logged_in_user(user_id)

    def cancel_login(self):
        sys.exit()

    def switch_to_main(self):
        self.login_window.hide()
        QTimer.singleShot(300, self.show_main_after_login_page)

    def show_main_after_login_page(self):
        group_id = getattr(self, 'get_user_group_id', 0)
        self.main_window.Show_main_page(group_id=group_id)

    def show_forgot_password(self):
        self.login_window.hide()
        self.forgot_password_widget.Show()

    def show_login_from_forgot(self):
        self.forgot_password_widget.hide()
        self.clear_login_form()
        self.login_window.Show()

    def Show_login_page(self):
        self.login_window.Show()

    def clear_login_form(self):
        # Clear user info when logging out
        self.logged_in_user_id = None
        self.logged_in_username = None
        self.logged_in_user_info = None
        
        if hasattr(self.login_window, 'user_lineEdit'):
            self.login_window.user_lineEdit.clear()

        if hasattr(self.login_window, 'pass_lineEdit'):
            self.login_window.password_lineEdit.clear()
        elif hasattr(self.login_window, 'password_lineEdit'):
            self.login_window.password_lineEdit.clear()