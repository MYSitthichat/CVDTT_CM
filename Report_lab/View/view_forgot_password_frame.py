from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from View.template_from_ui.forgot_password_frame import Ui_forgot_password_Form
from PySide6.QtGui import QAction, QIcon
import os

class ForgotPasswordWidget(QWidget):
    def __init__(self, parent=None):
        super(ForgotPasswordWidget, self).__init__(parent)
        self.ui = Ui_forgot_password_Form()
        self.ui.setupUi(self)

        self.ui.FP_new_password_lineEdit.setEchoMode(self.ui.FP_new_password_lineEdit.EchoMode.Password)
        self.ui.FP_new_password_check_lineEdit.setEchoMode(self.ui.FP_new_password_check_lineEdit.EchoMode.Password)
        self.password_visible = False
        
        icon_path = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "ICON", 
            "LOGIN"
        )
        self.eye_hide_icon = QIcon(os.path.join(icon_path, "hidden.png"))
        self.eye_show_icon = QIcon(os.path.join(icon_path, "eye.png"))
        self.toggle_action = QAction(self.ui.FP_new_password_lineEdit)
        self.toggle_action.setIcon(self.eye_hide_icon)
        self.toggle_action.setToolTip("แสดงรหัสผ่าน")
        self.toggle_action.triggered.connect(self.toggle_password_visibility)
        self.ui.FP_new_password_lineEdit.addAction(
            self.toggle_action, 
            self.ui.FP_new_password_lineEdit.ActionPosition.TrailingPosition
        )
        self.ui.FP_new_password_check_lineEdit.addAction(
            self.toggle_action, 
            self.ui.FP_new_password_check_lineEdit.ActionPosition.TrailingPosition
        )
        
    def toggle_password_visibility(self):
        if self.password_visible:
            self.ui.FP_new_password_lineEdit.setEchoMode(self.ui.FP_new_password_lineEdit.EchoMode.Password)
            self.ui.FP_new_password_check_lineEdit.setEchoMode(self.ui.FP_new_password_check_lineEdit.EchoMode.Password)
            self.toggle_action.setIcon(self.eye_hide_icon)
            self.toggle_action.setToolTip("แสดงรหัสผ่าน")
            self.password_visible = False
        else:
            self.ui.FP_new_password_lineEdit.setEchoMode(self.ui.FP_new_password_lineEdit.EchoMode.Normal)
            self.ui.FP_new_password_check_lineEdit.setEchoMode(self.ui.FP_new_password_check_lineEdit.EchoMode.Normal)
            self.toggle_action.setIcon(self.eye_show_icon)
            self.toggle_action.setToolTip("ซ่อนรหัสผ่าน")
            self.password_visible = True


    def unlock_email_field(self):
        self.ui.FP_email_lineEdit.setEnabled(True)
        self.ui.FP_check_email_pushButton.setEnabled(True)
        self.ui.FP_check_email_pushButton.setStyleSheet("")
        
    def lock_email_field(self):
        self.ui.FP_email_lineEdit.setEnabled(False)
        self.ui.FP_check_email_pushButton.setEnabled(False)
        self.ui.FP_check_email_pushButton.setStyleSheet("background-color: lightgray;")

    def check_email_success(self):
        self.ui.FP_new_password_lineEdit.setEnabled(True)
        self.ui.FP_new_password_check_lineEdit.setEnabled(True)
        # self.ui.FP_save_pushButton.setEnabled(True)

    def check_email_failure(self):
        self.ui.FP_new_password_lineEdit.setEnabled(False)
        self.ui.FP_new_password_check_lineEdit.setEnabled(False)
        self.ui.FP_save_pushButton.setEnabled(False)
        
    def unlock_and_clear(self):
        self.ui.FP_email_lineEdit.setEnabled(True)
        self.ui.FP_check_email_pushButton.setEnabled(True)
        self.ui.FP_new_password_lineEdit.setEnabled(True)
        self.ui.FP_new_password_check_lineEdit.setEnabled(True)
        self.ui.FP_save_pushButton.setEnabled(True)
        self.ui.FP_email_lineEdit.clear()
        self.ui.FP_new_password_lineEdit.clear()
        self.ui.FP_new_password_check_lineEdit.clear()
        self.ui.FP_Password_like_label.clear()
        self.check_email_failure()
    
    def passwords_match(self):
        self.ui.FP_Password_like_label.setText("✅")
        self.ui.FP_save_pushButton.setEnabled(True)
    
    def passwords_do_not_match(self):
        self.ui.FP_Password_like_label.setText("❌")
        self.ui.FP_save_pushButton.setEnabled(False)

    def comfirm_is_none(self):
        self.ui.FP_Password_like_label.clear()
        self.ui.FP_save_pushButton.setEnabled(False)

    def Show(self):
        self.ui.FP_new_password_lineEdit.setEchoMode(self.ui.FP_new_password_lineEdit.EchoMode.Password)
        self.ui.FP_new_password_check_lineEdit.setEchoMode(self.ui.FP_new_password_check_lineEdit.EchoMode.Password)
        self.toggle_action.setIcon(self.eye_hide_icon)
        self.password_visible = False
        self.show()
    
    def hide(self):
        return super().hide()