import sys
import os
import traceback
import pythoncom  # จำเป็นสำหรับ Windows (Word Automation)
from docx2pdf import convert as convert_to_pdf
from pdf2docx import Converter
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                               QLineEdit, QProgressBar, QMessageBox, QTabWidget)
from PySide6.QtCore import QThread, Signal, Qt, QUrl
from PySide6.QtGui import QFont, QIcon, QAction
from PySide6.QtWebEngineWidgets import QWebEngineView  # สำหรับแสดง PDF

# ==========================================
# 1. ส่วนแสดงผล PDF (Preview Window)
# ==========================================
class PdfPreviewWindow(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()
        self.setWindowTitle(f"PDF Preview: {os.path.basename(pdf_path)}")
        self.resize(1000, 800)

        # Widget หลัก
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        # ตั้งค่าให้รองรับ PDF
        settings = self.web_view.settings()
        settings.setAttribute(settings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(settings.WebAttribute.PdfViewerEnabled, True)
        settings.setAttribute(settings.WebAttribute.LocalContentCanAccessFileUrls, True)

        # โหลดไฟล์
        self.load_pdf(pdf_path)

    def load_pdf(self, file_path):
        if os.path.exists(file_path):
            # ต้องใช้ Absolute Path เสมอ
            abs_path = os.path.abspath(file_path)
            # แปลง Path เป็น URL format (file:///C:/...)
            self.web_view.setUrl(QUrl.fromLocalFile(abs_path))
        else:
            QMessageBox.critical(self, "Error", "ไม่พบไฟล์ PDF")

# ==========================================
# 2. ส่วน Worker (ทำงานเบื้องหลัง)
# ==========================================
class WorkerThread(QThread):
    finished_signal = Signal(bool, str, str) # (Success, Message, OutputPath)

    def __init__(self, mode, input_path, output_path):
        super().__init__()
        self.mode = mode # 'word2pdf' or 'pdf2word'
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        try:
            if self.mode == 'word2pdf':
                pythoncom.CoInitialize() # Init COM สำหรับ Word
                convert_to_pdf(self.input_path, self.output_path)
            
            elif self.mode == 'pdf2word':
                cv = Converter(self.input_path)
                cv.convert(self.output_path, start=0, end=None)
                cv.close()

            self.finished_signal.emit(True, "แปลงไฟล์สำเร็จ!", self.output_path)
        
        except Exception as e:
            err_msg = f"{str(e)}\n{traceback.format_exc()}"
            self.finished_signal.emit(False, err_msg, "")
        finally:
            if self.mode == 'word2pdf':
                pythoncom.CoUninitialize()

# ==========================================
# 3. ส่วน GUI (Tab แปลงไฟล์)
# ==========================================
class ConverterTab(QWidget):
    def __init__(self, mode, parent=None):
        super().__init__(parent)
        self.mode = mode # 'word2pdf' or 'pdf2word'
        self.output_file_path = None # เก็บ path ล่าสุดที่แปลงเสร็จ
        self.preview_window = None   # เก็บหน้าต่าง Preview

        # Config ตามโหมด
        if mode == 'word2pdf':
            self.title = "แปลง Word (.docx) เป็น PDF"
            self.input_ext = "Word Files (*.docx *.doc)"
            self.btn_text = "แปลงเป็น PDF"
            self.theme_color = "#2980B9" # สีน้ำเงิน
        else:
            self.title = "แปลง PDF เป็น Word (.docx)"
            self.input_ext = "PDF Files (*.pdf)"
            self.btn_text = "แปลงเป็น Word"
            self.theme_color = "#C0392B" # สีแดง

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Header
        lbl_title = QLabel(self.title)
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {self.theme_color};")
        layout.addWidget(lbl_title)

        # Input Selection
        input_layout = QHBoxLayout()
        self.txt_path = QLineEdit()
        self.txt_path.setPlaceholderText("เลือกไฟล์...")
        self.txt_path.setReadOnly(True)
        self.txt_path.setFixedHeight(40)
        
        btn_browse = QPushButton("📂 เลือกไฟล์")
        btn_browse.setFixedHeight(40)
        btn_browse.clicked.connect(self.browse_file)
        
        input_layout.addWidget(self.txt_path)
        input_layout.addWidget(btn_browse)
        layout.addLayout(input_layout)

        # Convert Button
        self.btn_convert = QPushButton(self.btn_text)
        self.btn_convert.setFixedHeight(50)
        self.btn_convert.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme_color}; 
                color: white; font-size: 16px; font-weight: bold; border-radius: 8px;
            }}
            QPushButton:hover {{ filter: brightness(110%); }}
            QPushButton:disabled {{ background-color: #BDC3C7; }}
        """)
        self.btn_convert.clicked.connect(self.start_conversion)
        self.btn_convert.setEnabled(False)
        layout.addWidget(self.btn_convert)

        # Preview Button (ซ่อนไว้ก่อน)
        self.btn_preview = QPushButton("👁️ ดูตัวอย่าง PDF")
        self.btn_preview.setFixedHeight(45)
        self.btn_preview.setStyleSheet("""
            QPushButton {
                background-color: #27AE60; color: white; font-size: 14px; border-radius: 8px;
            }
            QPushButton:hover { background-color: #2ECC71; }
        """)
        self.btn_preview.clicked.connect(self.open_preview)
        self.btn_preview.hide() # ซ่อนจนกว่าจะแปลงเสร็จ
        layout.addWidget(self.btn_preview)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Status
        self.lbl_status = QLabel("-")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_status)
        layout.addStretch()

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "เลือกไฟล์", "", self.input_ext)
        if file_path:
            self.txt_path.setText(file_path)
            self.btn_convert.setEnabled(True)
            self.lbl_status.setText("พร้อมเริ่มงาน")
            self.lbl_status.setStyleSheet("color: black;")
            
            # ถ้าเป็นโหมด PDF -> Word ปุ่ม Preview อาจจะเปิดได้เลยถ้า User เลือกไฟล์ PDF
            if self.mode == 'pdf2word':
                self.output_file_path = file_path # มองไฟล์ input เป็นไฟล์ที่จะพรีวิว
                self.btn_preview.setText("👁️ ดูตัวอย่างไฟล์ PDF ต้นฉบับ")
                self.btn_preview.show()
            else:
                self.btn_preview.hide()

    def start_conversion(self):
        input_path = self.txt_path.text()
        if not input_path: return

        # UI Lock
        self.btn_convert.setEnabled(False)
        self.btn_preview.hide()
        self.progress_bar.show()
        self.lbl_status.setText("กำลังประมวลผล... กรุณารอสักครู่")
        self.lbl_status.setStyleSheet("color: orange; font-weight: bold;")

        # Prepare Output Path
        folder = os.path.dirname(input_path)
        filename = os.path.splitext(os.path.basename(input_path))[0]
        
        if self.mode == 'word2pdf':
            output_path = os.path.join(folder, filename + ".pdf")
        else:
            output_path = os.path.join(folder, filename + ".docx")

        # Start Thread
        self.worker = WorkerThread(self.mode, input_path, output_path)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, success, message, output_path):
        self.progress_bar.hide()
        self.btn_convert.setEnabled(True)

        if success:
            self.lbl_status.setText(f"✅ {message}")
            self.lbl_status.setStyleSheet("color: green; font-weight: bold;")
            
            # เก็บ Path ไว้ใช้งาน
            self.output_file_path = output_path

            # ถ้าแปลงเป็น PDF ให้โชว์ปุ่ม Preview
            if self.mode == 'word2pdf':
                self.btn_preview.setText("👁️ ดูตัวอย่าง PDF ที่ได้")
                self.btn_preview.show()
            else:
                QMessageBox.information(self, "สำเร็จ", f"ไฟล์ Word ถูกบันทึกที่:\n{output_path}")
        else:
            self.lbl_status.setText("❌ เกิดข้อผิดพลาด")
            self.lbl_status.setStyleSheet("color: red;")
            QMessageBox.critical(self, "Error", message)

    def open_preview(self):
        if self.output_file_path and os.path.exists(self.output_file_path):
            # เปิดหน้าต่าง Preview
            self.preview_window = PdfPreviewWindow(self.output_file_path)
            self.preview_window.show()
        else:
            QMessageBox.warning(self, "เตือน", "ไม่พบไฟล์ PDF สำหรับแสดงผล")

# ==========================================
# 4. Main Window (ตัวรวม Tabs)
# ==========================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab Report Manager Pro")
        self.resize(600, 500)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab { height: 45px; width: 200px; font-size: 14px; }
            QTabWidget::pane { border: 1px solid #CCC; }
        """)
        self.setCentralWidget(self.tabs)

        # เพิ่ม Tab
        self.tab1 = ConverterTab('word2pdf')
        self.tab2 = ConverterTab('pdf2word')

        self.tabs.addTab(self.tab1, "Word ➔ PDF")
        self.tabs.addTab(self.tab2, "PDF ➔ Word")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())