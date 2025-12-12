import sys
import os
import traceback
import pythoncom  # จำเป็นสำหรับ Windows COM Object ใน Thread
from docx2pdf import convert as convert_to_pdf
from pdf2docx import Converter
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                               QLineEdit, QProgressBar, QMessageBox, QTabWidget, QFrame)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QIcon, QFont

# ==========================================
# ส่วน Worker (ทำงานเบื้องหลัง)
# ==========================================

class WordToPdfWorker(QThread):
    finished_signal = Signal(bool, str)

    def __init__(self, input_path, output_path):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        try:
            # Initialize COM สำหรับ Thread นี้ (สำคัญมากบน Windows)
            pythoncom.CoInitialize()
            
            # แปลงไฟล์
            convert_to_pdf(self.input_path, self.output_path)
            
            self.finished_signal.emit(True, f"บันทึกไฟล์ PDF เรียบร้อยที่:\n{self.output_path}")
        except Exception as e:
            self.finished_signal.emit(False, str(e))
        finally:
            # คืนค่า COM
            pythoncom.CoUninitialize()

class PdfToWordWorker(QThread):
    finished_signal = Signal(bool, str)

    def __init__(self, input_path, output_path):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        try:
            cv = Converter(self.input_path)
            # start=0, end=None คือแปลงทุกหน้า
            cv.convert(self.output_path, start=0, end=None)
            cv.close()
            
            self.finished_signal.emit(True, f"บันทึกไฟล์ Word เรียบร้อยที่:\n{self.output_path}")
        except Exception as e:
            # จับ Error พร้อม Stack trace เพื่อให้แก้บั๊กง่าย
            err_msg = f"{str(e)}\n{traceback.format_exc()}"
            self.finished_signal.emit(False, err_msg)

# ==========================================
# ส่วน GUI (หน้าจอโปรแกรม)
# ==========================================

class ConverterTab(QWidget):
    """ Template สำหรับหน้าจอแปลงไฟล์ (ใช้ร่วมกันทั้ง 2 แท็บ) """
    def __init__(self, title, input_ext, btn_text, color_theme, parent=None):
        super().__init__(parent)
        self.input_ext = input_ext
        self.worker = None # เก็บ instance ของ Thread

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # 1. Header
        lbl_title = QLabel(title)
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color_theme};")
        layout.addWidget(lbl_title)

        # 2. Input Selection
        input_layout = QHBoxLayout()
        self.txt_path = QLineEdit()
        self.txt_path.setPlaceholderText(f"เลือกไฟล์ {input_ext} ...")
        self.txt_path.setReadOnly(True)
        self.txt_path.setFixedHeight(35)
        
        btn_browse = QPushButton("📂 เลือกไฟล์")
        btn_browse.setFixedHeight(35)
        btn_browse.clicked.connect(self.browse_file)
        
        input_layout.addWidget(self.txt_path)
        input_layout.addWidget(btn_browse)
        layout.addLayout(input_layout)

        # 3. Action Button
        self.btn_convert = QPushButton(btn_text)
        self.btn_convert.setFixedHeight(45)
        self.btn_convert.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_theme}; 
                color: white; 
                font-weight: bold; 
                font-size: 14px;
                border-radius: 8px;
            }}
            QPushButton:hover {{ filter: brightness(110%); }}
            QPushButton:disabled {{ background-color: #BDC3C7; }}
        """)
        self.btn_convert.clicked.connect(self.start_conversion)
        self.btn_convert.setEnabled(False)
        layout.addWidget(self.btn_convert)

        # 4. Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0) # Infinite loop animation
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # 5. Status
        self.lbl_status = QLabel("พร้อมทำงาน")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setStyleSheet("color: gray;")
        layout.addWidget(self.lbl_status)
        
        layout.addStretch() # ดันทุกอย่างขึ้นบน

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "เลือกไฟล์", "", f"Document Files (*{self.input_ext})"
        )
        if file_path:
            self.txt_path.setText(file_path)
            self.btn_convert.setEnabled(True)
            self.lbl_status.setText("ไฟล์พร้อมแปลง")
            self.lbl_status.setStyleSheet("color: green;")

    def start_conversion(self):
        input_path = self.txt_path.text()
        if not input_path: return

        # Lock UI
        self.btn_convert.setEnabled(False)
        self.progress_bar.show()
        self.lbl_status.setText("กำลังดำเนินการ... กรุณารอสักครู่")
        self.lbl_status.setStyleSheet("color: orange; font-weight: bold;")

        # สร้าง Output path (ชื่อเดิมแต่เปลี่ยนนามสกุล)
        input_folder = os.path.dirname(input_path)
        input_filename = os.path.splitext(os.path.basename(input_path))[0]
        
        # Override Logic ตามชนิดไฟล์
        if self.input_ext == ".docx":
            output_path = os.path.join(input_folder, input_filename + ".pdf")
            self.worker = WordToPdfWorker(input_path, output_path)
        else:
            output_path = os.path.join(input_folder, input_filename + ".docx")
            self.worker = PdfToWordWorker(input_path, output_path)

        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, success, message):
        self.progress_bar.hide()
        self.btn_convert.setEnabled(True)
        
        if success:
            self.lbl_status.setText("✅ เสร็จสมบูรณ์")
            self.lbl_status.setStyleSheet("color: green; font-weight: bold;")
            QMessageBox.information(self, "สำเร็จ", message)
        else:
            self.lbl_status.setText("❌ เกิดข้อผิดพลาด")
            self.lbl_status.setStyleSheet("color: red; font-weight: bold;")
            QMessageBox.critical(self, "Error", f"ไม่สามารถแปลงไฟล์ได้:\n{message}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab Report Converter Pro")
        self.resize(600, 400)

        # Setup Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #C0C0C0; }
            QTabBar::tab { height: 40px; width: 150px; font-size: 14px; }
            QTabBar::tab:selected { font-weight: bold; }
        """)
        self.setCentralWidget(self.tabs)

        # Tab 1: Word -> PDF
        self.tab_word_to_pdf = ConverterTab(
            title="แปลงไฟล์ Word (.docx) เป็น PDF",
            input_ext=".docx",
            btn_text="🚀 แปลงเป็น PDF",
            color_theme="#2980B9" # สีน้ำเงิน
        )
        
        # Tab 2: PDF -> Word
        self.tab_pdf_to_word = ConverterTab(
            title="แปลงไฟล์ PDF เป็น Word (.docx)",
            input_ext=".pdf",
            btn_text="📝 แปลงเป็น Word",
            color_theme="#C0392B" # สีแดง
        )

        self.tabs.addTab(self.tab_word_to_pdf, "Word ➔ PDF")
        self.tabs.addTab(self.tab_pdf_to_word, "PDF ➔ Word")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # ตั้ง Font ให้สวยงาม (Optional)
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())