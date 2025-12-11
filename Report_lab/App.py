import sys
import os

# เพิ่ม parent directory (CVDTT_CM) เข้า Python path เพื่อให้สามารถ import SERVICES_REGISTER และ BACKEND ได้
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # CVDTT_CM folder
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# เพิ่ม Register/Order_Lab_Pdf เข้า Python path เพื่อใช้ PDF generators จาก Register folder
local_order_lab_pdf = os.path.join(current_dir, 'Order_Lab_Pdf')
if local_order_lab_pdf not in sys.path:
    sys.path.insert(0, local_order_lab_pdf)

from PySide6.QtWidgets import QApplication
from Controller.main_controller import MainController
from Controller.login_controller import Login_Controller 

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