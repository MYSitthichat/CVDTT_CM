from PySide6.QtWidgets import QMainWindow
from View.template_from_ui.main_frame import Ui_MainWindow
from View.user_profile_widget import UserProfileWidget
from View.view_report_from_frame import ReportFormView
class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create instances of the report form view
        self.report_form_view = ReportFormView()


        # Store reference to main controller (will be set by MainController)
        self.main_controller = None
        
        self.user_profile_widget = None
        self._setup_user_profile_widget()

        self.setup_stacked_widget()


    def setup_stacked_widget(self):
        while self.ui.stackedWidget.count() > 0:
            old_widget = self.ui.stackedWidget.widget(0)
            self.ui.stackedWidget.removeWidget(old_widget)
        self.ui.stackedWidget.addWidget(self.report_form_view)
        # self.ui.stackedWidget.setCurrentWidget(self.report_form_view)

    def Show_main_page(self):
        self.show()
        self.ui.stackedWidget.setCurrentWidget(self.report_form_view)

    def hide(self):
        super().hide()
    
    def get_logged_in_user_id(self):
        if self.main_controller:
            return self.main_controller.get_logged_in_user_id()
        return None
    
    def get_user_login_id(self):
        return self.get_logged_in_user_id()
    
    def _setup_user_profile_widget(self):
        if hasattr(self.ui, 'logout_pushButton'):
            self.ui.logout_pushButton.hide()
            
            self.user_profile_widget = UserProfileWidget(
                parent=self.ui.frame,
                name="User",
                role="Staff",
                employee_id=""
            )
            self.user_profile_widget.setGeometry(7, 823, 251, 60)
            self.user_profile_widget.show()
    
    def update_user_profile(self, name, role, employee_id):
        if self.user_profile_widget:
            self.user_profile_widget.update_user_info(name, role, employee_id)
    
    def get_user_profile_widget(self):
        return self.user_profile_widget