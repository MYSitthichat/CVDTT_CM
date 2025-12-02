from PySide6.QtWidgets import QMainWindow
from View.template_from_ui.login_frame import Ui_login_MainWindow
from PySide6.QtGui import QAction, QIcon
import os

class LoginWindow(QMainWindow,Ui_login_MainWindow):
    
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)   
        
        self.password_lineEdit.setEchoMode(self.password_lineEdit.EchoMode.Password)
        self.password_visible = False
        
        icon_path = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "ICON", 
            "LOGIN"
        )
        self.eye_hide_icon = QIcon(os.path.join(icon_path, "hidden.png"))
        self.eye_show_icon = QIcon(os.path.join(icon_path, "eye.png"))
        self.toggle_action = QAction(self.password_lineEdit)
        self.toggle_action.setIcon(self.eye_hide_icon)
        self.toggle_action.setToolTip("แสดงรหัสผ่าน")  # tooltip เมื่อ hover
        self.toggle_action.triggered.connect(self.toggle_password_visibility)
        self.password_lineEdit.addAction(
            self.toggle_action, 
            self.password_lineEdit.ActionPosition.TrailingPosition
        )
        
        
    def toggle_password_visibility(self):
        if self.password_visible:
            self.password_lineEdit.setEchoMode(self.password_lineEdit.EchoMode.Password)
            self.toggle_action.setIcon(self.eye_hide_icon)
            self.toggle_action.setToolTip("แสดงรหัสผ่าน")
            self.password_visible = False
        else:
            self.password_lineEdit.setEchoMode(self.password_lineEdit.EchoMode.Normal)
            self.toggle_action.setIcon(self.eye_show_icon)
            self.toggle_action.setToolTip("ซ่อนรหัสผ่าน")
            self.password_visible = True

    def Show(self):
        self.password_lineEdit.setEchoMode(self.password_lineEdit.EchoMode.Password)
        self.toggle_action.setIcon(self.eye_hide_icon)
        self.password_visible = False
        self.show()
    
    def hide(self):
        return super().hide()