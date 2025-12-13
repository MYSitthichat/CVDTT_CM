from PySide6.QtWidgets import QWidget
from View.template_from_ui.receive_lab_frame import Ui_receive_lab_Form

class ReceiveLabFormView(QWidget):
    def __init__(self, parent=None):
        super(ReceiveLabFormView, self).__init__(parent)
        self.ui = Ui_receive_lab_Form()
        self.ui.setupUi(self)
        # Signal connection moved to controller