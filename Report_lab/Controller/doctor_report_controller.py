from PySide6.QtWidgets import QMessageBox, QTreeWidgetItem, QFileDialog, QProgressDialog
from PySide6.QtCore import QObject, Qt, QUrl, QThread, Signal
from PySide6.QtWebEngineCore import QWebEngineSettings
from View.view_doctor_frame import DoctorReportView
from SERVICES_REPORT_LAB.doctor_report_service import DoctorReportService
from datetime import datetime
import os
import subprocess
import sys
import base64
from docx2pdf import convert


class PDFConverterThread(QThread):
    """Thread สำหรับแปลง Word เป็น PDF แบบ background"""
    finished = Signal(str)  # ส่ง path ของ PDF ที่แปลงเสร็จ
    error = Signal(str)     # ส่งข้อความ error
    
    def __init__(self, word_file, pdf_file):
        super().__init__()
        self.word_file = word_file
        self.pdf_file = pdf_file
    
    def run(self):
        try:
            # print(f"✓ [Thread] กำลังแปลงเป็น PDF...")
            convert(self.word_file, self.pdf_file)
            # print(f"✓ [Thread] แปลงเป็น PDF เรียบร้อย: {self.pdf_file}")
            self.finished.emit(self.pdf_file)
        except Exception as e:
            print(f"✗ [Thread] Error converting to PDF: {e}")
            self.error.emit(str(e))


class DoctorReportController(QObject):
    # Define signals

    def __init__(self, view: DoctorReportView, main_controller=None):
        super().__init__()
        self.view: DoctorReportView = view
        self.main_controller = main_controller
        self.doctor_report_service = DoctorReportService()
        
        # Thread สำหรับแปลง PDF
        self.pdf_converter_thread = None
        
        # Progress Dialog สำหรับแสดงสถานะการแปลงไฟล์
        self.progress_dialog = None
        
        # Mapping ชื่อห้องแล็บกับ room_id
        self.lab_room_mapping = {
            "ทั้งหมด": "",
            "แบคทีเรียวิทยา": "1",
            "ปรสิตวิทยา": "5",
            "อณูวิทยา": "8"
        }
        
        self.setup_treewidget()
        
        # เชื่อมต่อ signal เมื่อคลิกที่แถวใน TreeWidget
        self.view.ui.detail_order_treeWidget.itemClicked.connect(self.on_tree_item_clicked)
        
        # เชื่อมต่อ ComboBox เพื่อกรองตามห้องแล็บ
        self.view.ui.select_lab_comboBox.currentTextChanged.connect(self.on_lab_filter_changed)
        
        self.view.ui.return_report_pushButton.clicked.connect(self.return_to_main_page)
        self.view.ui.preview_pushButton.clicked.connect(self.export_report)
        
        # โหลดข้อมูลครั้งแรก
        self.load_pending_reports()
        
        
        
    def setup_treewidget(self):
        tree = self.view.ui.detail_order_treeWidget
        
        # ปรับความกว้างคอลัมน์ให้สมมาตรและเหมาะสม
        tree.setColumnWidth(0, 130)  # วันที่ลงรายงาน
        tree.setColumnWidth(1, 120)  # เลขที่รายงาน
        tree.setColumnWidth(2, 120)  # เลขที่ตัวอย่าง
        tree.setColumnWidth(3, 140)  # ตัวอย่างที่ส่งตรวจ
        tree.setColumnWidth(4, 170)  # ห้องปฏิบัติการ
        tree.setColumnWidth(5, 150)  # ผู้ลงรายงาน
        tree.setColumnWidth(6, 110)  # สถานะ
        
        # จัด Header ให้อยู่ตรงกลาง
        header = tree.header()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # จัดข้อความในแถวที่มีอยู่แล้วให้อยู่ตรงกลาง
        for i in range(tree.topLevelItemCount()):
            item = tree.topLevelItem(i)
            for j in range(tree.columnCount()):
                item.setTextAlignment(j, Qt.AlignmentFlag.AlignCenter)
        
        # เปิดใช้งาน alternating row colors
        tree.setAlternatingRowColors(True)
        
        # ปรับให้แถวมีความสูงเท่ากัน
        tree.setUniformRowHeights(True)
        
        
        self.update_pending_count()
        
    def update_pending_count(self):
        tree = self.view.ui.detail_order_treeWidget
        total_count = tree.topLevelItemCount()
        self.view.ui.stuck_order_lineEdit.setText(str(total_count))
        
        
    def clear_selection(self):
        """ล้างค่าที่เลือกใน TreeWidget และค่าในช่องเลขที่รายงาน"""
        tree = self.view.ui.detail_order_treeWidget
        tree.clearSelection()
        tree.setCurrentItem(None)
        
        if hasattr(self.view.ui, 'number_report_lineEdit'):
            self.view.ui.number_report_lineEdit.clear()
            self.view.ui.number_report_lineEdit.setText("")
        
        # โหลดข้อมูลใหม่เมื่อเปิดหน้านี้
        self.load_pending_reports()
        
        
        
    def on_tree_item_clicked(self, item, column):
        """เมื่อคลิกที่แถวใน TreeWidget"""
        report_number = item.text(1)        # เลขที่รายงาน
        report_id = item.data(0, Qt.ItemDataRole.UserRole)  # ดึง ID ที่เก็บไว้
        
        # แสดงเลขที่รายงานในช่อง
        self.view.ui.number_report_lineEdit.setText(report_number)
        
        
        
    def return_to_main_page(self):
        print("kkkkkk")

    def export_report(self):
        """แสดงตัวอย่างรายงาน"""
        try:
            # ดึงเลขที่รายงานจากช่อง
            report_number = self.view.ui.number_report_lineEdit.text()
            
            if not report_number or report_number.strip() == "":
                QMessageBox.warning(self.view, "แจ้งเตือน", "กรุณาเลือกรายงานที่ต้องการแสดงตัวอย่าง")
                return
            
            # สร้างโฟลเดอร์ temp_file_report
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            parent_dir = os.path.dirname(current_dir)
            temp_dir = os.path.join(parent_dir, "temp_file_report")
            os.makedirs(temp_dir, exist_ok=True)
            
            # กำหนด path สำหรับไฟล์ Word และ PDF (ใช้ชื่อคงที่)
            word_file = os.path.join(temp_dir, "doctor_report_download.docx")
            pdf_file = os.path.join(temp_dir, "preview_temp.pdf")
            
            # ลบไฟล์ Word เก่าถ้ามี
            if os.path.exists(word_file):
                try:
                    os.remove(word_file)
                except Exception as e:
                    print(f"⚠ ไม่สามารถลบไฟล์ Word เก่าได้: {e}")
            
            # ลบไฟล์ PDF เก่าถ้ามี
            if os.path.exists(pdf_file):
                try:
                    os.remove(pdf_file)
                except Exception as e:
                    print(f"⚠ ไม่สามารถลบไฟล์ PDF เก่าได้: {e}")
            
            # ดาวน์โหลดไฟล์ Word
            success = self.doctor_report_service.download_report_file(int(report_number), word_file)
            
            if not success:
                QMessageBox.critical(self.view, "ข้อผิดพลาด", "ไม่สามารถดาวน์โหลดไฟล์รายงานได้")
                return
            
            
            # แปลงเป็น PDF ใน Thread
            self.pdf_converter_thread = PDFConverterThread(word_file, pdf_file)
            self.pdf_converter_thread.finished.connect(self.on_pdf_conversion_finished)
            self.pdf_converter_thread.error.connect(self.on_pdf_conversion_error)
            self.pdf_converter_thread.start()
            
            # สร้าง Progress Dialog แบบไม่มี progress bar (แสดงแค่ spinner)
            self.progress_dialog = QProgressDialog(
                "กำลังแปลงไฟล์เป็น PDF กรุณารอสักครู่...",
                None,  # ไม่มีปุ่ม Cancel
                0, 0,  # min=0, max=0 จะทำให้แสดงแบบ busy indicator (หมุนๆ)
                self.view
            )
            self.progress_dialog.setWindowTitle("กำลังประมวลผล")
            self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            self.progress_dialog.setMinimumDuration(0)  # แสดงทันที
            self.progress_dialog.setCancelButton(None)  # ไม่มีปุ่มยกเลิก
            self.progress_dialog.setAutoClose(False)  # ไม่ปิดอัตโนมัติ
            self.progress_dialog.setAutoReset(False)
            self.progress_dialog.show()
            
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด\n{str(e)}")
    
    def on_pdf_conversion_finished(self, pdf_path):
        """เมื่อแปลง PDF เสร็จ"""
        try:
            # ปิด Progress Dialog
            if self.progress_dialog:
                self.progress_dialog.close()
                self.progress_dialog = None
            
            # ตรวจสอบไฟล์
            if not os.path.exists(pdf_path):
                QMessageBox.critical(self.view, "ข้อผิดพลาด", "ไม่พบไฟล์ PDF ที่แปลงเสร็จ")
                return
            
            
            # อ่านไฟล์ PDF และแปลงเป็น base64
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
                base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            
            # ตั้งค่า WebEngine ให้รองรับ PDF
            settings = self.view.ui.doctor_show_preview_webEngineView.page().settings()
            settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
            
            # สร้าง HTML content พร้อม base64 PDF
            pdf_filename = os.path.basename(pdf_path)
            html_content = self.create_pdf_viewer_html(base64_pdf, pdf_filename)
            
            # แสดง HTML ใน WebEngineView
            self.view.ui.doctor_show_preview_webEngineView.setHtml(html_content, QUrl("http://localhost"))
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"ไม่สามารถแสดง PDF ได้\n{str(e)}")
    
    def create_pdf_viewer_html(self, base64_data, filename="document.pdf"):
        """สร้าง HTML สำหรับแสดง PDF จาก base64 data"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{filename}</title>
            <style>
                body, html {{ 
                    margin: 0; 
                    padding: 0; 
                    height: 100%; 
                    overflow: hidden; 
                    background-color: #525659; 
                }}
                embed {{ 
                    width: 100%; 
                    height: 100%; 
                    border: none; 
                }}
            </style>
        </head>
        <body>
            <embed 
                src="data:application/pdf;base64,{base64_data}#toolbar=1&navpanes=0&scrollbar=1&page=1&view=FitH" 
                type="application/pdf" 
                width="100%" 
                height="100%"
            >
        </body>
        </html>
        """
    
    def on_pdf_conversion_error(self, error_message):
        """เมื่อเกิดข้อผิดพลาดในการแปลง PDF"""
        # ปิด Progress Dialog
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None
        
        QMessageBox.critical(self.view, "ข้อผิดพลาด", f"ไม่สามารถแปลงเป็น PDF ได้\n{error_message}")
        
    def load_pending_reports(self, room_id: str = ""):
        """โหลดรายการรายงานที่รอการตรวจสอบจาก API"""
        try:
            # ดึงข้อมูลจาก API
            response = self.doctor_report_service.get_pending_reports(room_id)
            
            if response and "data" in response:
                data_list = response["data"]
                
                # ล้างข้อมูลเดิมใน TreeWidget
                tree = self.view.ui.detail_order_treeWidget
                tree.clear()
                
                # เพิ่มข้อมูลใหม่
                for data in data_list:
                    item = QTreeWidgetItem()
                    
                    # แปลง datetime ให้แสดงทั้งวันที่และเวลา
                    report_date = data.get('report_date', '')
                    if isinstance(report_date, datetime):
                        report_date = report_date.strftime('%d-%m-%y %H:%M')
                    elif isinstance(report_date, str) and report_date:
                        try:
                            # ลองแปลงรูปแบบที่มี T (ISO format)
                            if 'T' in report_date:
                                # เอา T ออกและแปลงเป็นรูปแบบที่ต้องการ
                                date_part, time_part = report_date.split('T')
                                # เอาเฉพาะเวลา HH:MM (ไม่เอา seconds และ milliseconds)
                                time_part = time_part.split('.')[0]  # เอา milliseconds ออก
                                time_part = ':'.join(time_part.split(':')[:2])  # เอาเฉพาะ HH:MM
                                year, month, day = date_part.split('-')
                                report_date = f"{day}-{month}-{year[2:]} {time_part}"
                            else:
                                dt = datetime.strptime(report_date, '%Y-%m-%d %H:%M:%S')
                                report_date = dt.strftime('%d-%m-%y %H:%M')
                        except Exception as e:
                            try:
                                date_only = report_date.split(' ')[0] if ' ' in report_date else report_date
                                if len(date_only) >= 10:  # YYYY-MM-DD
                                    parts = date_only.split('-')
                                    if len(parts) == 3:
                                        report_date = f"{parts[2]}-{parts[1]}-{parts[0][2:]}"
                            except:
                                pass
                    
                    # ตั้งค่าข้อมูลในแต่ละคอลัมน์
                    item.setText(0, str(report_date))                                       # วันที่ลงรายงาน
                    item.setText(1, str(data.get('report_number', '') or ''))              # เลขที่รายงาน (report_form.id)
                    item.setText(2, str(data.get('sample_id', '') or ''))                  # เลขที่ตัวอย่าง (report_form.lab_order_id)
                    item.setText(3, str(data.get('sample_inspection', '') or ''))          # ตัวอย่างที่ส่งตรวจ
                    item.setText(4, str(data.get('lab_room', '') or ''))                   # ห้องปฏิบัติการ
                    item.setText(5, str(data.get('reporter_name', '') or ''))              # ผู้ลงรายงาน
                    item.setText(6, str(data.get('state_text', 'รอการยืนยัน') or ''))      # สถานะ
                    
                    # จัดข้อความให้อยู่ตรงกลาง
                    for j in range(tree.columnCount()):
                        item.setTextAlignment(j, Qt.AlignmentFlag.AlignCenter)
                    
                    # เก็บ ID ของรายงานไว้ใน item (สำหรับใช้งานภายหลัง)
                    item.setData(0, Qt.ItemDataRole.UserRole, data.get('id'))
                    
                    tree.addTopLevelItem(item)
                
                # อัปเดตจำนวนค้างในระบบ
                self.update_pending_count()
                
                
            else:
                QMessageBox.warning(self.view, "แจ้งเตือน", "ไม่พบข้อมูลรายงาน")
                
        except Exception as e:
            print(f"✗ Error loading reports: {e}")
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"ไม่สามารถโหลดข้อมูลได้\n{str(e)}")
    
    def on_lab_filter_changed(self, lab_name: str):
        """เมื่อเลือกห้องแล็บใน ComboBox ให้โหลดข้อมูลใหม่"""
        # แปลง lab_name เป็น room_id
        room_id = self.lab_room_mapping.get(lab_name, "")
        # โหลดข้อมูลตาม room_id ที่เลือก
        self.load_pending_reports(room_id)
