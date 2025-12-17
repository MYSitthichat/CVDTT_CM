from View.view_main_frame import MainWindow
from PySide6.QtCore import QObject, Signal, QTimer
from Controller.send_lab_controller import SendLabController
from Controller.receive_lab_controller import ReceiveLabController
from Controller.lab_edit_from_controller import LabEditFormController
from View.view_receive_lab_frame import ReceiveLabFormView
from View.view_report_from_frame import ReportFormView
from View.view_lab_edite_form_frame import LabEditFormView
from SERVICES_REPORT_LAB.search_room import SearchRoomService

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
        self.main_window: MainWindow = MainWindow()
        
        # Use the widgets that MainWindow already created
        self.report_widget: ReportFormView = self.main_window.report_form_view
        self.receive_widget: ReceiveLabFormView = self.main_window.receive_lab_form_view
        self.edite_lab_widget: LabEditFormView = self.main_window.lab_edit_form_view

        # Create controllers
        self.send_lab_controller: SendLabController = SendLabController(self.report_widget)
        self.receive_lab_controller: ReceiveLabController = ReceiveLabController(self.receive_widget, main_controller=self)
        self.lab_edit_form_controller: LabEditFormController = LabEditFormController(self.edite_lab_widget)

        # Set reference to this controller in main_window
        self.main_window.main_controller = self
        self.login_controller = login_controller

        self.search_room_service = SearchRoomService()
        
        
        self.main_window.ui.receive_lab_order_pushButton.clicked.connect(self.show_receive_work_page)
        self.main_window.ui.send_lab_report_pushButton.clicked.connect(self.show_report_work_page)
        self.main_window.ui.Edit_Form_pushButton.clicked.connect(self.show_lab_edit_form)
        
        self._setup_user_profile_connections()
        
    def show_receive_work_page(self):
        self.main_window.show_receive_work_page()
        self.main_window.receive_lab_form_view.clear_all_table()

    def show_report_work_page(self):
        self.main_window.show_report_work_page()

    def show_lab_edit_form(self):
        self.main_window.show_lab_edit_form()

    def _setup_user_profile_connections(self):
        user_widget = self.main_window.get_user_profile_widget()
        if user_widget and user_widget.popup:
            user_widget.popup.btn_logout.clicked.connect(self.logout_pushButton_clicked)
        if hasattr(self.main_window.ui, 'logout_pushButton'):
            self.main_window.ui.logout_pushButton.clicked.connect(self.logout_pushButton_clicked)
        

    def Show_main_page(self,group_id):
        if group_id and group_id >=18:
            self.main_window.show_error_page()
        else:
            self.main_window.Show_main_page()

    def hide_main_page(self):
        self.main_window.hide()
    
    def logout_pushButton_clicked(self):
        if hasattr(self.main_window, 'user_profile_widget') and self.main_window.user_profile_widget:
            self.main_window.user_profile_widget.hide_popup_immediately()
        self.main_window.reset_to_default_page()
        self.main_window.hide()
        
        if self.login_controller:
            self.set_logged_in_user(user_id=None)
            self.receive_widget.clear_all_table()
            QTimer.singleShot(300, self.show_login_after_logout)
    
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
        room = "ห้องปฏิบัติการส่วนกลาง"
        full_name = username or 'User'
        role = 'Staff'
        employee_id = str(user_id) if user_id else ''
        email = ''
        if user_info:
            title = user_info.get('title', '')
            name = user_info.get('name', '')
            surname = user_info.get('surname', '')
            full_name = f"{title}{name} {surname}".strip()
            if not full_name:
                full_name = username or 'User'
            role = user_info.get('position', 'Staff')
            email = user_info.get('email', '')

            if "ศาสตร์" in role:
                room = role.split("ศาสตร์")[-1].strip()
            else:
                room = "ห้องปฏิบัติการส่วนกลาง"
        self.get_room_id_from_user(room)
        
        
        if hasattr(self.main_window, 'user_profile_widget') and self.main_window.user_profile_widget:
            self.main_window.user_profile_widget.update_user_info(full_name, role, employee_id)
            if self.main_window.user_profile_widget.popup:
                self.main_window.user_profile_widget.popup.set_user_data(
                    full_name, role, employee_id, email, room
                )


    def get_room_id_from_user(self, room):
        stop_words = [
                "นักวิทยาศาสตร์", 
                "เจ้าหน้าที่",
                "ปฏิบัติการ", 
                "วิเคราะห์", 
                "ตรวจสอบ",
                "ตรวจ", 
                "ห้อง", 
                "ทาง", 
                "และ",
                "ประจำศูนย์",
                "ชันสูตรโรคสัตว์",
                "น้ำ",
                "วิทยา"]
        cleaned_name = room
        room_id = None
        if cleaned_name != "ห้องปฏิบัติการส่วนกลาง":
            for word in stop_words:
                cleaned_name = cleaned_name.replace(word, "").strip()
            room = cleaned_name
            room_id = self.search_room_service.search_room(cleaned_name)
            self.set_room_id_from_user(cleaned_name, room_id)
            self.status_lab_edit_button(False)
        else:
            room_id = 999
            self.set_room_id_from_user(cleaned_name, room_id)
            self.status_lab_edit_button(True)


    def status_lab_edit_button(self, show: bool):
        self.main_window.ui.Edit_Form_pushButton.setVisible(show)

    def set_room_id_from_user(self, room, room_id):
        # เคลียร์ข้อมูลเก่าก่อนตั้งค่า room ใหม่
        self.receive_lab_controller.clear_all_data()
        self.receive_lab_controller._set_room_for_user(room, room_id)

    def get_user_login_id(self):
        return self.logged_in_user_id
    
    def get_logged_in_user_id(self):
        return self.logged_in_user_id
