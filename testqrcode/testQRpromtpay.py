import sys
import io
import qrcode
from promptpay import qrcode as pp
from pyzbar.pyzbar import decode
from PIL import Image
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QTabWidget,
    QFileDialog,
    QTextEdit,
    QGroupBox,
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt


class PromptPayQRApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PromptPay QR Generator & Slip Verifier")
        self.setGeometry(100, 100, 600, 700)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Create Tab Widget
        self.tabs = QTabWidget()
        
        # Create tabs
        self.tab_generate = QWidget()
        self.tab_verify = QWidget()
        
        self.tabs.addTab(self.tab_generate, "สร้าง QR Code")
        self.tabs.addTab(self.tab_verify, "ตรวจสอบสลิป")
        
        # Setup each tab
        self.setup_generate_tab()
        self.setup_verify_tab()
        
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def setup_generate_tab(self):
        layout = QVBoxLayout()

        # Input for PromptPay ID
        self.label_id = QLabel("PromptPay ID (Phone / Thai ID):")
        layout.addWidget(self.label_id)

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("08xxxxxxxx or 1-xxxx-xxxxx-xx-x")
        layout.addWidget(self.input_id)

        # Input for Amount
        self.label_amount = QLabel("Amount (THB) - Optional:")
        layout.addWidget(self.label_amount)

        self.input_amount = QLineEdit()
        self.input_amount.setPlaceholderText("e.g. 100.00")
        layout.addWidget(self.input_amount)

        # Generate Button
        self.btn_generate = QPushButton("Generate QR Code")
        self.btn_generate.setFixedHeight(40)
        self.btn_generate.clicked.connect(self.generate_qr)
        layout.addWidget(self.btn_generate)

        # Image Display
        self.label_qr_image = QLabel("QR Code will appear here")
        self.label_qr_image.setAlignment(Qt.AlignCenter)
        self.label_qr_image.setMinimumSize(300, 300)
        self.label_qr_image.setStyleSheet(
            "border: 1px solid #ccc; background-color: #f9f9f9;"
        )
        layout.addWidget(self.label_qr_image)

        self.tab_generate.setLayout(layout)

    def setup_verify_tab(self):
        layout = QVBoxLayout()
        
        # Upload section
        upload_group = QGroupBox("อัพโหลดภาพสลิป")
        upload_layout = QVBoxLayout()
        
        btn_layout = QHBoxLayout()
        self.btn_upload = QPushButton("เลือกไฟล์ภาพสลิป")
        self.btn_upload.setFixedHeight(40)
        self.btn_upload.clicked.connect(self.upload_slip)
        btn_layout.addWidget(self.btn_upload)
        
        self.btn_decode = QPushButton("Decode QR Code")
        self.btn_decode.setFixedHeight(40)
        self.btn_decode.setEnabled(False)
        self.btn_decode.clicked.connect(self.decode_slip)
        btn_layout.addWidget(self.btn_decode)
        
        upload_layout.addLayout(btn_layout)
        
        # Slip Image Display
        self.label_slip_image = QLabel("ภาพสลิปจะแสดงที่นี่")
        self.label_slip_image.setAlignment(Qt.AlignCenter)
        self.label_slip_image.setMinimumSize(300, 300)
        self.label_slip_image.setStyleSheet(
            "border: 1px solid #ccc; background-color: #f9f9f9;"
        )
        upload_layout.addWidget(self.label_slip_image)
        
        upload_group.setLayout(upload_layout)
        layout.addWidget(upload_group)
        
        # Result section
        result_group = QGroupBox("ข้อมูลจากสลิป")
        result_layout = QVBoxLayout()
        
        self.text_slip_data = QTextEdit()
        self.text_slip_data.setReadOnly(True)
        self.text_slip_data.setPlaceholderText("ข้อมูลที่ decode จาก QR code จะแสดงที่นี่")
        self.text_slip_data.setMinimumHeight(200)
        result_layout.addWidget(self.text_slip_data)
        
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        self.tab_verify.setLayout(layout)
        
        # Store slip image path
        self.slip_image_path = None

    def generate_qr(self):
        account_id = self.input_id.text().strip()
        amount_str = self.input_amount.text().strip()

        if not account_id:
            QMessageBox.warning(self, "Input Error", "Please enter a PromptPay ID.")
            return

        amount = None
        if amount_str:
            try:
                amount = float(amount_str)
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Invalid amount format.")
                return

        try:
            # Generate Payload
            payload = pp.generate_payload(account_id, amount)
            # print(f"Payload: {payload}")

            # Generate QR Image using 'qrcode' library
            # box_size controls the size of each box in pixels
            img = qrcode.make(payload, box_size=10, border=2)

            # Convert PIL image to QPixmap via BytesIO
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            qimage = QImage.fromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(qimage)

            # Display
            self.label_qr_image.setPixmap(
                pixmap.scaled(
                    self.label_qr_image.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )
            self.label_qr_image.setText("")  # Clear text if any

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate QR Code: {str(e)}")

    def upload_slip(self):
        """Upload slip image and display it"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "เลือกภาพสลิป",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            self.slip_image_path = file_path
            
            # Display image
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(
                self.label_slip_image.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label_slip_image.setPixmap(scaled_pixmap)
            self.label_slip_image.setText("")
            
            # Enable decode button
            self.btn_decode.setEnabled(True)
            self.text_slip_data.clear()

    def decode_slip(self):
        """Decode QR code from slip image"""
        if not self.slip_image_path:
            QMessageBox.warning(self, "Error", "กรุณาเลือกภาพสลิปก่อน")
            return
        
        try:
            # Open image with PIL
            img = Image.open(self.slip_image_path)
            
            # Decode QR codes
            decoded_objects = decode(img)
            
            if not decoded_objects:
                QMessageBox.warning(
                    self,
                    "ไม่พบ QR Code",
                    "ไม่พบ QR Code ในภาพที่เลือก\nกรุณาตรวจสอบว่าภาพชัดเจนและมี QR Code"
                )
                return
            
            # Display all QR codes found
            result_text = f"พบ QR Code จำนวน: {len(decoded_objects)}\n\n"
            
            for i, obj in enumerate(decoded_objects, 1):
                result_text += f"=== QR Code #{i} ===\n"
                result_text += f"Type: {obj.type}\n"
                
                # Decode data
                data = obj.data.decode('utf-8')
                result_text += f"Raw Data:\n{data}\n\n"
                
                # Try to parse PromptPay data
                if data.startswith("00020101"):
                    parsed_data = self.parse_promptpay_qr(data)
                    result_text += "ข้อมูล PromptPay:\n"
                    for key, value in parsed_data.items():
                        result_text += f"  {key}: {value}\n"
                else:
                    result_text += "  (ไม่ใช่ QR Code ของ PromptPay)\n"
                
                result_text += "\n" + "="*40 + "\n\n"
            
            self.text_slip_data.setPlainText(result_text)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"เกิดข้อผิดพลาดในการ decode QR Code:\n{str(e)}"
            )

    def parse_promptpay_qr(self, data):
        """Parse PromptPay QR code data"""
        result = {}
        
        try:
            # Parse EMV QR code format
            i = 0
            while i < len(data):
                if i + 4 > len(data):
                    break
                
                tag = data[i:i+2]
                length = int(data[i+2:i+4])
                
                if i + 4 + length > len(data):
                    break
                
                value = data[i+4:i+4+length]
                
                # Map common tags
                if tag == "00":
                    result["Payload Format"] = value
                elif tag == "01":
                    result["Point of Initiation"] = value
                elif tag == "29":
                    # PromptPay specific
                    result["PromptPay"] = self.parse_sub_tags(value)
                elif tag == "30":
                    result["Merchant Information"] = value
                elif tag == "52":
                    result["Merchant Category Code"] = value
                elif tag == "53":
                    result["Currency"] = "THB" if value == "764" else value
                elif tag == "54":
                    result["Amount"] = f"{value} THB"
                elif tag == "58":
                    result["Country Code"] = value
                elif tag == "62":
                    # Additional data
                    result["Additional Data"] = self.parse_sub_tags(value)
                elif tag == "63":
                    result["CRC"] = value
                
                i += 4 + length
            
        except Exception as e:
            result["Parse Error"] = str(e)
        
        return result

    def parse_sub_tags(self, data):
        """Parse sub-tags in PromptPay format"""
        result = {}
        i = 0
        
        try:
            while i < len(data):
                if i + 4 > len(data):
                    break
                
                tag = data[i:i+2]
                length = int(data[i+2:i+4])
                
                if i + 4 + length > len(data):
                    break
                
                value = data[i+4:i+4+length]
                
                # Map sub-tags
                if tag == "00":
                    result["AID"] = value
                elif tag == "01":
                    result["Mobile/ID"] = value
                elif tag == "02":
                    result["Ref 1"] = value
                elif tag == "03":
                    result["Ref 2"] = value
                elif tag == "05":
                    result["Terminal ID"] = value
                elif tag == "07":
                    result["Bill Number"] = value
                else:
                    result[f"Tag {tag}"] = value
                
                i += 4 + length
                
        except Exception:
            pass
        
        return result if result else data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptPayQRApp()
    window.show()
    sys.exit(app.exec())
