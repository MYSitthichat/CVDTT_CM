from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QFrame, QGraphicsDropShadowEffect)


class UserDetailPopup(QWidget):
    def __init__(self, parent_widget):
        super().__init__(None)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setAttribute(Qt.WA_Hover)
        self.mouse_inside = False
        self.parent_widget = parent_widget
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.container = QFrame()
        self.container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 4)
        self.container.setGraphicsEffect(shadow)
        
        content_layout = QVBoxLayout(self.container)
        content_layout.setSpacing(5)
        
        lbl_title = QLabel("ข้อมูลผู้ใช้งาน")
        lbl_title.setStyleSheet("font-weight: bold; color: #555; font-size: 14px; border: none;")
        content_layout.addWidget(lbl_title)
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #e0e0e0; border: none;")
        content_layout.addWidget(separator)
        self.lbl_name = QLabel("ชื่อ: -")
        self.lbl_role = QLabel("ตำแหน่ง: -")
        self.lbl_employee_id = QLabel("รหัสพนักงาน: -")
        self.lbl_email = QLabel("อีเมล: -")
        self.lbl_room = QLabel("ห้อง: -")
        
        label_style = "color: #333; font-size: 12px; border: none; padding: 2px;"
        for lbl in [self.lbl_name, self.lbl_role, self.lbl_employee_id, self.lbl_email, self.lbl_room]:
            lbl.setStyleSheet(label_style)
            content_layout.addWidget(lbl)
        
        content_layout.addSpacing(5)
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setStyleSheet("background-color: #e0e0e0; border: none;")
        content_layout.addWidget(separator2)
        self.btn_logout = QPushButton("ออกจากระบบ")
        logout_btn_style = """
            QPushButton {
                background-color: #f0f0f0;
                border: none;
                border-radius: 5px;
                padding: 0px 0px;
                color: #333;
                font-size: 13px;
                font-weight: bold;
                min-width: 240px;
            }
            QPushButton:hover {
                background-color: #ffcccc;
                color: #dc3545;
            }
        """
        self.btn_logout.setStyleSheet(logout_btn_style)
        
        content_layout.addWidget(self.btn_logout)
        layout.addWidget(self.container)
        
        self.setFixedSize(310, 250)
        
        self.btn_logout.clicked.connect(self.hide_immediately)

    def set_user_data(self, name, role, employee_id, email="", room=""):
        self.lbl_name.setText(f"ชื่อ: {name}")
        self.lbl_role.setText(f"ตำแหน่ง: {role}")
        self.lbl_employee_id.setText(f"รหัสพนักงาน: {employee_id}")
        self.lbl_email.setText(f"อีเมล: {email if email else '-'}")
        self.lbl_room.setText(f"ห้อง: {room if room else '-'}")

    def enterEvent(self, event):
        """เมื่อเมาส์เข้า popup"""
        self.mouse_inside = True
        if self.parent_widget and self.parent_widget.hide_timer.isActive():
            self.parent_widget.hide_timer.stop()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """เมื่อเมาส์ออกจาก popup"""
        self.mouse_inside = False
        if self.parent_widget:
            self.parent_widget.hide_timer.start(self.parent_widget.hide_delay)
        super().leaveEvent(event)
    
    def hide_immediately(self):
        """ซ่อน popup ทันที (เมื่อกดปุ่ม)"""
        self.mouse_inside = False
        self.hide()


class UserProfileWidget(QFrame):
    def __init__(self, parent=None, name="User", role="Staff", employee_id=""):
        super().__init__(parent)
        self.popup = None
        self.name = name
        self.role = role
        self.employee_id = employee_id
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self._hide_popup_delayed)
        self.hide_delay = 200  # milliseconds
        
        self.setFixedHeight(60)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            UserProfileWidget {
                background-color: #f8f9fa;
                border: 2px solid #dcdcdc;
                border-radius: 8px;
            }
            UserProfileWidget:hover {
                background-color: #e9ecef;
                border: 2px solid #007bff;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        avatar_char = self._get_avatar_char(name)
        self.avatar = QLabel(avatar_char)
        self.avatar.setFixedSize(45, 45)
        self.avatar.setAlignment(Qt.AlignCenter)
        self.avatar.setStyleSheet("""
            background-color: #007bff;
            color: white;
            font-weight: bold;
            font-size: 20px;
            border-radius: 22px;
            border: 2px solid white;
        """)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(1)
        
        self.lbl_name = QLabel(name)
        self.lbl_name.setStyleSheet(
            "font-weight: bold; font-size: 13px; border: none; "
            "background: transparent; color: #333;"
        )
        
        self.lbl_role = QLabel(role)
        self.lbl_role.setStyleSheet(
            "color: #6c757d; font-size: 10px; border: none; "
            "background: transparent;"
        )
        
        info_layout.addStretch()
        info_layout.addWidget(self.lbl_name)
        info_layout.addWidget(self.lbl_role)
        info_layout.addStretch()
        icon = QLabel("⋮")
        icon.setStyleSheet(
            "color: #6c757d; font-weight: bold; font-size: 18px; "
            "border: none; background: transparent;"
        )
        
        layout.addWidget(self.avatar)
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(icon)
        self.popup = UserDetailPopup(self)
        self.popup.set_user_data(name, role, employee_id)

    def update_user_info(self, name, role, employee_id):
        self.name = name
        self.role = role
        self.employee_id = employee_id
        avatar_char = self._get_avatar_char(name)
        self.avatar.setText(avatar_char)
        self.lbl_name.setText(name)
        self.lbl_role.setText(role)
        
        if self.popup:
            self.popup.set_user_data(name, role, employee_id)
    
    def _get_avatar_char(self, full_name):
        if not full_name:
            return "U"
        
        parts = full_name.strip().split()
        
        titles = ['นาย', 'นาง', 'นางสาว', 'น.ส.', 'นายแพทย์', 'แพทย์หญิง', 
                  'ทพ.', 'ทพญ.', 'ดร.', 'ศ.', 'รศ.', 'ผศ.', 'Mr.', 'Mrs.', 
                  'Miss', 'Ms.', 'Dr.', 'Prof.']
        for part in parts:
            if part and part not in titles:
                return part[0].upper()
        return full_name[0].upper() if full_name else "U"

    def enterEvent(self, event):
        if self.hide_timer.isActive():
            self.hide_timer.stop()
        
        if self.popup:
            global_pos = self.mapToGlobal(QPoint(0, 0))
            x = global_pos.x() + self.width()
            
            if self.parent():
                parent_global_pos = self.parent().mapToGlobal(QPoint(0, 0))
                parent_bottom = parent_global_pos.y() + self.parent().height()
                
                y = parent_bottom - self.popup.height() + 5
            else:
                y = global_pos.y() + self.height() - self.popup.height()
            
            self.popup.move(x, y)
            self.popup.show()
            
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hide_timer.start(self.hide_delay)
        super().leaveEvent(event)
    
    def _hide_popup_delayed(self):
        if self.popup and not self.popup.mouse_inside:
            self.popup.hide()
    
    def hide_popup_immediately(self):
        if self.hide_timer.isActive():
            self.hide_timer.stop()
        if self.popup:
            self.popup.mouse_inside = False
            self.popup.hide()
