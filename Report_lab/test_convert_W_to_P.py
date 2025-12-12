import sys
import os
import time
import pythoncom  # จำเป็นสำหรับการทำงานกับ Word ใน Thread แยก
from docx2pdf import convert
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                               QLineEdit, QProgressBar, QMessageBox)
from PySide6.QtCore import QThread, Signal, Qt

# --- 1. Worker Thread (คนงานเบื้องหลัง) ---
class ConversionWorker(QThread):
    # สร้างสัญญาณเพื่อส่งผลลัพธ์กลับไปที่หน้าจอหลัก
    finished_signal = Signal(bool, str) # (Success?, Message)

    def __init__(self, input_path, output_path):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        try:
            # สำคัญ: การใช้ COM Object (Word) ใน Thread ใหม่ ต้อง Initialize ก่อนเสมอ
            pythoncom.CoInitialize()
            
            # สั่งแปลงไฟล์
            convert(self.input_path, self.output_path)
            
            # ส่งสัญญาณว่าเสร็จแล้ว
            self.finished_signal.emit(True, f"แปลงไฟล์สำเร็จเรียบร้อย!\nบันทึกที่: {self.output_path}")
            
        except Exception as e:
            # ถ้าพัง ส่ง Error กลับไป
            self.finished_signal.emit(False, str(e))
        finally:
            # คืนค่า resource
            pythoncom.CoUninitialize()

# --- 2. GUI (หน้าจอหลัก) ---
class WordToPDFApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab Report Converter (Word -> PDF)")
        self.resize(500, 250)

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("แปลงไฟล์ Lab Report เป็น PDF")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title)

        # File Selection Area
        file_layout = QHBoxLayout()
        self.txt_path = QLineEdit()
        self.txt_path.setPlaceholderText("เลือกไฟล์ Word (.docx)...")
        self.txt_path.setReadOnly(True)
        file_layout.addWidget(self.txt_path)

        btn_browse = QPushButton("📂 เลือกไฟล์")
        btn_browse.clicked.connect(self.browse_file)
        file_layout.addWidget(btn_browse)
        layout.addLayout(file_layout)

        # Convert Button
        self.btn_convert = QPushButton("🚀 เริ่มแปลงเป็น PDF")
        self.btn_convert.setFixedHeight(40)
        self.btn_convert.setStyleSheet("""
            QPushButton {
                background-color: #0078D7; 
                color: white; 
                font-weight: bold; 
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #005A9E; }
            QPushButton:disabled { background-color: #CCCCCC; }
        """)
        self.btn_convert.clicked.connect(self.start_conversion)
        self.btn_convert.setEnabled(False) # ปิดปุ่มไว้ก่อนจนกว่าจะเลือกไฟล์
        layout.addWidget(self.btn_convert)

        # Progress Bar (ซ่อนไว้ก่อน)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0) # แบบ Indeterminate (วิ่งไปมา)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Status Label
        self.lbl_status = QLabel("กรุณาเลือกไฟล์เพื่อเริ่มต้น")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setStyleSheet("color: gray;")
        layout.addWidget(self.lbl_status)

        # ตัวแปรเก็บ Worker
        self.worker = None

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "เลือกไฟล์ Word", "", "Word Documents (*.docx *.doc)"
        )
        if file_path:
            self.txt_path.setText(file_path)
            self.btn_convert.setEnabled(True)
            self.lbl_status.setText("พร้อมแปลงไฟล์")
            self.lbl_status.setStyleSheet("color: green;")

    def start_conversion(self):
        input_path = self.txt_path.text()
        if not input_path:
            return

        # กำหนดชื่อไฟล์ output (เปลี่ยนนามสกุลเป็น .pdf)
        output_path = os.path.splitext(input_path)[0] + ".pdf"

        # UI Updates: ล็อกปุ่ม, โชว์ progress
        self.btn_convert.setEnabled(False)
        self.txt_path.setEnabled(False)
        self.progress_bar.show()
        self.lbl_status.setText("กำลังแปลงไฟล์... กรุณารอสักครู่ (อาจใช้เวลา 5-10 วินาที)")
        self.lbl_status.setStyleSheet("color: orange;")

        # เริ่ม Thread ทำงาน
        self.worker = ConversionWorker(input_path, output_path)
        self.worker.finished_signal.connect(self.on_conversion_finished)
        self.worker.start()

    def on_conversion_finished(self, success, message):
        # UI Updates: คืนค่าเดิม
        self.progress_bar.hide()
        self.btn_convert.setEnabled(True)
        self.txt_path.setEnabled(True)

        if success:
            self.lbl_status.setText("✅ เสร็จสมบูรณ์")
            self.lbl_status.setStyleSheet("color: green;")
            QMessageBox.information(self, "สำเร็จ", message)
            
            # Option: เปิด Folder ปลายทางให้เลยไหม?
            # os.startfile(os.path.dirname(self.txt_path.text())) 
        else:
            self.lbl_status.setText("❌ เกิดข้อผิดพลาด")
            self.lbl_status.setStyleSheet("color: red;")
            QMessageBox.critical(self, "ล้มเหลว", f"เกิดข้อผิดพลาดในการแปลงไฟล์:\n{message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WordToPDFApp()
    window.show()
    sys.exit(app.exec())