from PySide6.QtWidgets import QWidget
from View.template_from_ui.error_page_frame import Ui_error_Form

class ErrorPageView(QWidget):
    def __init__(self, parent=None):
        super(ErrorPageView, self).__init__(parent)
        self.ui = Ui_error_Form()
        self.ui.setupUi(self)
        
        # Force larger font size (override qt_material theme)
        self.ui.label.setStyleSheet("""
            QLabel {
                font-family: 'TH Niramit AS';
                font-size: 75pt;
                font-weight: bold;
                color: #ffffff;
            }
        """)
        # Signal connection moved to controller