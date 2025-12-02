from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QPen, QPixmap, QColor
from View.template_from_ui.edit_employee_frame import Ui_edit_employee_MainWindow

class EditEmployeeWindow(QMainWindow, Ui_edit_employee_MainWindow):
    class SignatureCanvas(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setMinimumSize(470, 410)
            self.drawing = False
            self.last_point = QPoint()
            self.image = QPixmap(470, 410)
            self.image.fill(Qt.white)

        def mousePressEvent(self, event):
            if event.button() == Qt.LeftButton:
                self.drawing = True
                self.last_point = event.pos()

        def mouseMoveEvent(self, event):
            if self.drawing and (event.buttons() & Qt.LeftButton):
                painter = QPainter(self.image)
                pen = QPen(QColor(0, 0, 0), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                painter.setPen(pen)
                painter.drawLine(self.last_point, event.pos())
                self.last_point = event.pos()
                self.update()

        def mouseReleaseEvent(self, event):
            if event.button() == Qt.LeftButton:
                self.drawing = False

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), self.image)

        def clear(self):
            self.image.fill(Qt.white)
            self.update()

        def get_signature(self):
            return self.image

        def set_signature(self, pixmap):
            self.image = pixmap.scaled(470, 410, Qt.KeepAspectRatio)
            self.update()

    def __init__(self, parent=None):
        super(EditEmployeeWindow, self).__init__(parent)
        self.setupUi(self)

        # Add signature canvas over the signature frame
        self.signature_canvas = EditEmployeeWindow.SignatureCanvas(self.employee_signature_frame)
        self.signature_canvas.setGeometry(0, 0, 470, 410)

        # Connect clear/edit button
        self.employee_edit_signature_pushButton.clicked.connect(self.clear_signature)

    def clear_signature(self):
        self.signature_canvas.clear()

    def get_signature_image(self):
        return self.signature_canvas.get_signature()

    def set_signature_image(self, pixmap):
        self.signature_canvas.set_signature(pixmap)

    def Show(self):
        self.show()

    def hide(self):
        return super().hide()
