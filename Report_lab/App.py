import sys
import os
from PySide6.QtWidgets import QApplication
from Controller.login_controller import Login_Controller 


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

register_dir = os.path.join(parent_dir, 'Report_lab')
if register_dir not in sys.path:
    sys.path.insert(0, register_dir)

try:
    from qt_material import apply_stylesheet
except ImportError:
    print("\n[Error] not found qt-material")
    print("error please run: pip install qt-material\n")
    sys.exit()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # apply_stylesheet(app, theme='dark_red.xml')
    apply_stylesheet(app, theme='dark_teal.xml')
    login_app = Login_Controller()
    login_app.Show_login_page()
    app.exec()

# Available themes
# Light Themes:
    # 'light_blue.xml'
    # 'light_blue_500.xml'
    # 'light_cyan.xml'
    # 'light_orange.xml'
    # 'light_pink.xml'
    # 'light_purple.xml'
    # 'light_red.xml'
    # 'light_teal.xml'
    # 'light_yellow.xml'

# Dark Themes:
    # 'dark_blue.xml'
    # 'dark_cyan.xml'
    # 'dark_pink.xml'
    # 'dark_purple.xml'
    # 'dark_red.xml'
    # 'dark_teal.xml'
    # 'dark_yellow.xml'
    
    # ผมต้้องการคำสั่ง sql โดยใช้ id และ room ในตาราง lab_order เพื่อหา sample_id และเอาเลข room ที่ส่งมาตอนแรกเขียนเป็น condition คือ ถ้า room = 2 ให้เอา sample_id ที่ได้ไปหาในตาราง lab_bacteria_biology ถ้า room = 5 ให้เอาไปหาในตาราง lab_parasite_biology ถ้า room = 8 ให้เอาไปหาในตาราง lab_molecular_biology และเลือกเอาเฉพาะรายการตรวจ