from View.view_forgot_password_frame import ForgotPasswordWidget
from PySide6.QtCore import QObject
from SERVICES_REPORT_LAB.auth_service import AuthService
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMessageBox


class ForgotPasswordController(QObject):
    return_to_login = Signal()
    def __init__(self):
        super(ForgotPasswordController, self).__init__()
        self.forgot_password_widget = ForgotPasswordWidget()
        self.api_app = AuthService()
        self.confirm_password_is_like = False
        self.forgot_password_widget.ui.FP_save_pushButton.clicked.connect(self.save_forgot_password)
        self.forgot_password_widget.ui.FP_cancel_pushButton.clicked.connect(self.cancel_forgot_password)
        self.forgot_password_widget.ui.FP_check_email_pushButton.clicked.connect(self.check_email)
        self.forgot_password_widget.ui.FP_new_password_check_lineEdit.textChanged.connect(self.compare_passwords)

    def save_forgot_password(self):
        email = self.forgot_password_widget.ui.FP_email_lineEdit.text()
        password = self.forgot_password_widget.ui.FP_new_password_lineEdit.text()
        confirm_password = self.forgot_password_widget.ui.FP_new_password_check_lineEdit.text()
        if password == confirm_password:
            if self.api_app.update_password(email,password):
                QMessageBox.information(
                self.forgot_password_widget,
                "Update Success",
                "รหัสผ่านของคุณถูกอัปเดตเรียบร้อยแล้ว")
                self.forgot_password_widget.unlock_and_clear()
                self.forgot_password_widget.hide()
                self.return_to_login.emit()
            else:
                QMessageBox.warning(
                self.forgot_password_widget,
                "Update Failed",
                "ไม่พบอีเมลนี้ในระบบ")
        else:
            QMessageBox.warning(
            self.forgot_password_widget,
            "Password is correct",
            "กรุณาเช็ค Password ว่าเหมือนกันหรือไม่")


    def compare_passwords(self):
        password = self.forgot_password_widget.ui.FP_new_password_lineEdit.text()
        confirm_password = self.forgot_password_widget.ui.FP_new_password_check_lineEdit.text()

        if confirm_password == "":
            self.forgot_password_widget.comfirm_is_none()
            self.confirm_password_is_like = False
            return

        if password == "":
            self.forgot_password_widget.passwords_do_not_match()
            self.confirm_password_is_like = False
            return

        if password == confirm_password:
            self.forgot_password_widget.passwords_match()
            self.confirm_password_is_like = True

        else:
            self.forgot_password_widget.passwords_do_not_match()
            self.confirm_password_is_like = False


    def cancel_forgot_password(self):
        self.forgot_password_widget.unlock_and_clear()
        self.forgot_password_widget.hide()
        self.return_to_login.emit()

    def check_email(self):
        email = self.forgot_password_widget.ui.FP_email_lineEdit.text()
        if email == "":
            QMessageBox.warning(
            self.forgot_password_widget,
            "Email Not Found",
            "ไม่สามารถปล่อยว่างได้ กรุณาใส่อีเมลล์")
            return
        else:
            if self.api_app.check_email(email):
                QMessageBox.information(
                self.forgot_password_widget,
                "Email Found",
                "✅ พบอีเมลนี้ในระบบ\n\nคุณสามารถรีเซ็ตรหัสผ่านได้")
                self.forgot_password_widget.lock_email_field()
                self.forgot_password_widget.check_email_success()
            else:
                QMessageBox.warning(
                    self.forgot_password_widget,
                    "Email Not Found",
                    "ไม่พบอีเมลนี้ในระบบ" )
                self.forgot_password_widget.ui.FP_email_lineEdit.clear()


    def hide(self):
        self.forgot_password_widget.hide()
    
    def Show(self):
        self.forgot_password_widget.Show()
        self.forgot_password_widget.unlock_and_clear()