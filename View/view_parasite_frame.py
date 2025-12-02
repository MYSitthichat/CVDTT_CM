from PySide6.QtWidgets import QWidget
from View.template_from_ui.parasite_frame import Ui_parasite_MainWindow

class parasiteFrameView(QWidget, Ui_parasite_MainWindow):
    def __init__(self, parent=None):
        super(parasiteFrameView, self).__init__(parent)
        self.ui = Ui_parasite_MainWindow()
        from PySide6.QtWidgets import QMainWindow
        dummy_main_window = QMainWindow()
        self.ui.setupUi(dummy_main_window)
        
        from PySide6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.centralwidget)
        self.setLayout(layout)

