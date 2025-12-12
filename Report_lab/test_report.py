import sys
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QGraphicsScene, 
                               QGraphicsPixmapItem, QGraphicsTextItem, QGraphicsLineItem, 
                               QToolBar, QFileDialog, QMessageBox, QGraphicsItem, QGraphicsRectItem)
from PySide6.QtCore import Qt, QRectF, QPointF, QSizeF
from PySide6.QtGui import QPixmap, QAction, QPainter, QPen, QFont, QPageSize, QPdfWriter, QBrush, QColor, QCursor

# --- Class สำหรับรูปภาพที่ย่อขยายได้ (แก้ไข Artifacts แล้ว) ---
class ResizableImageItem(QGraphicsRectItem):
    handle_size = 10.0

    handle_cursors = {
        1: Qt.SizeFDiagCursor, 2: Qt.SizeVerCursor, 3: Qt.SizeBDiagCursor,
        4: Qt.SizeHorCursor, 5: Qt.SizeHorCursor,
        6: Qt.SizeBDiagCursor, 7: Qt.SizeVerCursor, 8: Qt.SizeFDiagCursor,
    }

    def __init__(self, pixmap):
        super().__init__()
        self.pixmap = pixmap
        self.setRect(0, 0, pixmap.width(), pixmap.height())
        
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        # สำคัญ: ต้องตั้งค่านี้เพื่อให้ boundingRect ทำงานถูกต้องเมื่อมีการหมุนหรือย่อขยาย
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges) 
        self.setAcceptHoverEvents(True)
        
        self.current_handle = None
        self.mouse_press_pos = None
        self.mouse_press_rect = None

    # --- [จุดที่แก้ไข] เพิ่มฟังก์ชันนี้เพื่อบอกขอบเขตที่แท้จริง ---
    def boundingRect(self):
        # เอาขอบเขตสี่เหลี่ยมเดิมมา
        rect = super().boundingRect()
        # เผื่อพื้นที่รอบๆ ออกไปอีกหน่อยให้ครอบคลุมจุดจับ (Handles)
        # ใช้ handle_size เป็นระยะเผื่อ (margin) เพื่อความปลอดภัย
        margin = self.handle_size
        return rect.adjusted(-margin, -margin, margin, margin)

    def paint(self, painter, option, widget=None):
        rect = self.rect()
        painter.drawPixmap(rect.toRect(), self.pixmap)

        if self.isSelected():
            self.draw_handles(painter)
            pen = QPen(Qt.gray, 1, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(rect)

    def draw_handles(self, painter):
        painter.setPen(Qt.black)
        painter.setBrush(Qt.white)
        handles = self.get_handle_rects()
        for _, rect in handles.items():
            painter.drawRect(rect)

    def get_handle_rects(self):
        rect = self.rect()
        s = self.handle_size
        # จุดจับจะอยู่กึ่งกลางมุมหรือขอบพอดี
        return {
            1: QRectF(rect.left() - s/2, rect.top() - s/2, s, s),
            2: QRectF(rect.center().x() - s/2, rect.top() - s/2, s, s),
            3: QRectF(rect.right() - s/2, rect.top() - s/2, s, s),
            4: QRectF(rect.left() - s/2, rect.center().y() - s/2, s, s),
            5: QRectF(rect.right() - s/2, rect.center().y() - s/2, s, s),
            6: QRectF(rect.left() - s/2, rect.bottom() - s/2, s, s),
            7: QRectF(rect.center().x() - s/2, rect.bottom() - s/2, s, s),
            8: QRectF(rect.right() - s/2, rect.bottom() - s/2, s, s),
        }

    def hoverMoveEvent(self, event):
        if self.isSelected():
            handle = self.get_handle_at(event.pos())
            if handle:
                self.setCursor(QCursor(self.handle_cursors[handle]))
            else:
                self.setCursor(Qt.SizeAllCursor)
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        if self.isSelected():
            self.current_handle = self.get_handle_at(event.pos())
            if self.current_handle:
                self.mouse_press_pos = event.pos()
                self.mouse_press_rect = self.rect()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.current_handle:
            self.interactive_resize(event.pos())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.current_handle = None
        self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)

    def get_handle_at(self, pos):
        handles = self.get_handle_rects()
        for handle_id, rect in handles.items():
            if rect.contains(pos):
                return handle_id
        return None

    def interactive_resize(self, mouse_pos):
        rect = self.mouse_press_rect
        diff = mouse_pos - self.mouse_press_pos
        
        new_x, new_y, new_w, new_h = rect.x(), rect.y(), rect.width(), rect.height()

        # [เพิ่มเติม] ทำให้ครบทุกจุดจับเพื่อความสมบูรณ์
        if self.current_handle == 1: # Top-Left
            new_x = rect.x() + diff.x()
            new_y = rect.y() + diff.y()
            new_w = rect.width() - diff.x()
            new_h = rect.height() - diff.y()
        elif self.current_handle == 2: # Top
            new_y = rect.y() + diff.y()
            new_h = rect.height() - diff.y()
        elif self.current_handle == 3: # Top-Right
            new_y = rect.y() + diff.y()
            new_w = rect.width() + diff.x()
            new_h = rect.height() - diff.y()
        elif self.current_handle == 4: # Left
            new_x = rect.x() + diff.x()
            new_w = rect.width() - diff.x()
        elif self.current_handle == 5: # Right
            new_w = rect.width() + diff.x()
        elif self.current_handle == 6: # Bottom-Left
            new_x = rect.x() + diff.x()
            new_w = rect.width() - diff.x()
            new_h = rect.height() + diff.y()
        elif self.current_handle == 7: # Bottom
            new_h = rect.height() + diff.y()
        elif self.current_handle == 8: # Bottom-Right
            new_w = rect.width() + diff.x()
            new_h = rect.height() + diff.y()
        
        if new_w < 20: new_w = 20
        if new_h < 20: new_h = 20

        # [จุดที่แก้ไข] แจ้งเตือนการเปลี่ยนแปลง Geometry ก่อนตั้งค่าใหม่
        self.prepareGeometryChange()
        self.setRect(new_x, new_y, new_w, new_h)


# --- (ส่วนอื่นๆ ของโค้ด ReportView, LabReportScene, LabReportEditor เหมือนเดิมทุกประการ) ---
# เพื่อความกระชับ ผมขอละส่วนที่ซ้ำเดิมไว้นะครับ ให้ใช้ส่วนล่างของโค้ดที่แล้วมารวมกับ Class ข้างบนนี้
# ถ้าต้องการโค้ดเต็มๆ บอกได้เลยครับ

# ... [วาง Class ResizableImageItem ตัวใหม่ทับตัวเดิม] ...

class ReportView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setAcceptDrops(True)
        self.setMouseTracking(True) 

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls(): event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls(): event.acceptProposedAction()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                self.add_image(f, event.position())

    def add_image(self, path, pos):
        pixmap = QPixmap(path)
        if pixmap.isNull(): return

        if pixmap.width() > 400:
            pixmap = pixmap.scaledToWidth(400, Qt.SmoothTransformation)
            
        item = ResizableImageItem(pixmap) # ใช้ Class ที่แก้แล้ว
        
        scene_pos = self.mapToScene(pos.toPoint())
        item.setPos(scene_pos)
        self.scene().addItem(item)

class LabReportScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mode = "select"
        self.current_item = None
        self.start_point = None
        self.setSceneRect(0, 0, 595, 842) # A4

    def mousePressEvent(self, event):
        # สำคัญ: คลิกที่ว่างเพื่อยกเลิกการเลือก และสั่ง redraw scene
        if not self.itemAt(event.scenePos(), QGraphicsView().transform()):
            self.clearSelection()
            self.update() # บังคับอัปเดตหน้าจอเพื่อลบ artifacts ที่อาจค้างอยู่

        if event.button() == Qt.LeftButton:
            pos = event.scenePos()
            if self.mode == "text":
                text = QGraphicsTextItem("Double click to edit")
                text.setFont(QFont("Arial", 12))
                text.setPos(pos)
                text.setFlag(QGraphicsItem.ItemIsMovable)
                text.setFlag(QGraphicsItem.ItemIsSelectable)
                text.setTextInteractionFlags(Qt.TextEditorInteraction)
                self.addItem(text)
                self.mode = "select"
                return
            elif self.mode == "arrow":
                self.start_point = pos
                self.current_item = QGraphicsLineItem(pos.x(), pos.y(), pos.x(), pos.y())
                pen = QPen(Qt.red, 3)
                self.current_item.setPen(pen)
                self.addItem(self.current_item)
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode == "arrow" and self.current_item:
            line = self.current_item.line()
            line.setP2(event.scenePos())
            self.current_item.setLine(line)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.mode == "arrow" and self.current_item:
            end_pos = event.scenePos()
            self.create_arrow_head(self.start_point, end_pos)
            self.current_item = None
            self.start_point = None
            self.mode = "select"
        super().mouseReleaseEvent(event)

    def create_arrow_head(self, start, end):
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        angle = math.atan2(dy, dx)
        arrow_len = 15
        arrow_angle = math.pi / 6 
        p1_x = end.x() - arrow_len * math.cos(angle - arrow_angle)
        p1_y = end.y() - arrow_len * math.sin(angle - arrow_angle)
        p2_x = end.x() - arrow_len * math.cos(angle + arrow_angle)
        p2_y = end.y() - arrow_len * math.sin(angle + arrow_angle)
        head1 = QGraphicsLineItem(end.x(), end.y(), p1_x, p1_y)
        head2 = QGraphicsLineItem(end.x(), end.y(), p2_x, p2_y)
        pen = QPen(Qt.red, 3)
        head1.setPen(pen)
        head2.setPen(pen)
        line = self.current_item
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)
        head1.setParentItem(line)
        head2.setParentItem(line)

class LabReportEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab Report Editor (Fixed Artifacts)")
        self.resize(1000, 800)
        self.scene = LabReportScene()
        self.view = ReportView(self.scene)
        self.setCentralWidget(self.view)
        
        toolbar = QToolBar("Tools")
        self.addToolBar(toolbar)
        
        btn_select = QAction("✋ Select", self)
        btn_select.triggered.connect(lambda: self.set_mode("select"))
        toolbar.addAction(btn_select)
        btn_text = QAction("📝 Add Text", self)
        btn_text.triggered.connect(lambda: self.set_mode("text"))
        toolbar.addAction(btn_text)
        btn_arrow = QAction("↗️ Draw Arrow", self)
        btn_arrow.triggered.connect(lambda: self.set_mode("arrow"))
        toolbar.addAction(btn_arrow)
        toolbar.addSeparator()
        btn_pdf = QAction("💾 Export PDF", self)
        btn_pdf.triggered.connect(self.export_pdf)
        toolbar.addAction(btn_pdf)

    def set_mode(self, mode):
        self.scene.mode = mode
        if mode == "select":
            self.view.setDragMode(QGraphicsView.RubberBandDrag)
            self.view.setCursor(Qt.ArrowCursor)
        else:
            self.view.setDragMode(QGraphicsView.NoDrag)
            self.view.setCursor(Qt.CrossCursor)

    def export_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save PDF", "report.pdf", "PDF Files (*.pdf)")
        if not filename: return
        writer = QPdfWriter(filename)
        writer.setPageSize(QPageSize(QPageSize.A4))
        writer.setResolution(300)
        painter = QPainter(writer)
        self.scene.render(painter)
        painter.end()
        QMessageBox.information(self, "Success", "Exported!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LabReportEditor()
    window.show()
    sys.exit(app.exec())