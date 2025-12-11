from PySide6.QtWidgets import QMainWindow
from View.template_from_ui.main_frame import Ui_MainWindow
from View.user_profile_widget import UserProfileWidget


class MainWindow(QMainWindow):
    
    def __init__(self, parent=None, model=None, add_work_widget=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Store reference to main controller (will be set by MainController)
        self.main_controller = None

        self.barcode_controller = None  # Created in MainController
        self.check_job_controller = None  # Created in MainController
        self.lab_received_controller = None  # Created in MainController
        self.molecular_controller = None
        self.after_death_controller = None
        self.lab_report_controller = None
        
        # --- User Profile Widget (แทนที่ปุ่ม Logout) ---
        self.user_profile_widget = None
        self._setup_user_profile_widget()

        self.setup_stacked_widget()



    def setup_stacked_widget(self):
        while self.ui.stackedWidget.count() > 0:
            old_widget = self.ui.stackedWidget.widget(0)
            self.ui.stackedWidget.removeWidget(old_widget)

    def Show_main_page(self):
        self.show()

    def hide(self):
        super().hide()
    
    def get_logged_in_user_id(self):
        """Get the logged-in user ID from main controller"""
        if self.main_controller:
            return self.main_controller.get_logged_in_user_id()
        return None
    
    def get_user_login_id(self):
        """Alias for get_logged_in_user_id for backward compatibility"""
        return self.get_logged_in_user_id()
    
    def _setup_user_profile_widget(self):
        """สร้างและแทนที่ปุ่ม Logout ด้วย User Profile Widget"""
        # ซ่อนปุ่ม Logout เดิม
        if hasattr(self.ui, 'logout_pushButton'):
            self.ui.logout_pushButton.hide()
            
            # สร้าง User Profile Widget
            self.user_profile_widget = UserProfileWidget(
                parent=self.ui.frame,
                name="User",
                role="Staff",
                employee_id=""
            )
            
            # ตั้งตำแหน่งให้ห่างจากปุ่ม EDIT EMPLOYEE 5px
            # EDIT EMPLOYEE: y=750, height=51 → สิ้นสุดที่ 801
            # Profile Card: 801 + 5 = 806
            self.user_profile_widget.setGeometry(7, 823, 251, 60)
            self.user_profile_widget.show()
    
    def update_user_profile(self, name, role, employee_id):
        """อัพเดทข้อมูลผู้ใช้ใน Profile Widget"""
        if self.user_profile_widget:
            self.user_profile_widget.update_user_info(name, role, employee_id)
    
    def get_user_profile_widget(self):
        """ดึง User Profile Widget เพื่อเชื่อมต่อ signals"""
        return self.user_profile_widget