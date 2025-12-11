from PySide6.QtWidgets import QWidget
from View.template_from_ui.bacteria_frame import Ui_bacteria_MainWindow

class bacterieFrameView(QWidget, Ui_bacteria_MainWindow):
    def __init__(self, parent=None):
        super(bacterieFrameView, self).__init__(parent)
        self.ui = Ui_bacteria_MainWindow()
        from PySide6.QtWidgets import QMainWindow
        dummy_main_window = QMainWindow()
        self.ui.setupUi(dummy_main_window)
        
        from PySide6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.centralwidget)
        self.setLayout(layout)