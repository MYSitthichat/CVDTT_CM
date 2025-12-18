import base64
import os
from PySide6.QtWidgets import QMessageBox, QFileDialog, QAbstractItemView
from PySide6.QtCore import QObject, Qt, QTimer, QUrl
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWebEngineCore import QWebEngineSettings
from View.view_report_from_frame import ReportFormView
from SERVICES_REPORT_LAB.send_lab_report_service import SendLabService
from docx2pdf import convert


class SendLabController(QObject):
    """ Controller for the Send Lab Page """

    def __init__(self, view: ReportFormView, main_controller=None):
        super().__init__()
        self.view: ReportFormView = view
        self.send_lab_service = SendLabService()
        self.main_controller = main_controller
        
        # Lazy loading state
        self.current_offset = 0
        self.limit = 50
        self.is_loading = False
        self.has_more_data = True
        self.all_data = []
        
        # Room and access control state
        self.log_room = None
        self.log_room_id = None
        self.admin_comein = False
        
        # Current selected lab order
        self.current_lab_order_id = None
        
        # PDF conversion state
        self.progress_timer = None
        self.progress_value = 0
        self.pdf_output_path = None
        
        # Setup barcode table model
        self.setup_barcode_table_model()
        
        # Disable search file button ตอนเริ่มต้น
        self.view.ui.search_location_file_pushButton.setEnabled(False)
        
        self._setup_connections()
    
    def setup_barcode_table_model(self):
        """Setup QStandardItemModel for barcode_tableView"""
        self.barcode_model = QStandardItemModel()
        self.barcode_model.setHorizontalHeaderLabels(['Lab Order ID'])
        self.view.ui.barcode_tableView.setModel(self.barcode_model)
        self.view.ui.barcode_tableView.setColumnWidth(0, 200)   # Lab Order ID
        self.view.ui.barcode_tableView.horizontalHeader().setStretchLastSection(True)
        self.view.ui.barcode_tableView.verticalHeader().setVisible(False)  # ซ่อนเลขแถว
        self.view.ui.barcode_tableView.setShowGrid(True)
        self.view.ui.barcode_tableView.setSelectionBehavior(self.view.ui.barcode_tableView.SelectionBehavior.SelectRows)
        self.view.ui.barcode_tableView.setSelectionMode(self.view.ui.barcode_tableView.SelectionMode.SingleSelection)
        self.view.ui.barcode_tableView.setAlternatingRowColors(True)
    
    def _setup_connections(self):
        self.view.ui.search_location_file_pushButton.clicked.connect(self.browse_file_clicked)
        self.view.ui.clear_location_file_pushButton.clicked.connect(self.clear_pushButton_clicked)
        self.view.ui.send_report_file_pushButton.clicked.connect(self.send_pushButton_clicked)
        self.view.ui.convert_word_to_pdf_pushButton.clicked.connect(self.convert_to_pdf_clicked)
        self.view.ui.select_barcode_pushButton.clicked.connect(self.select_barcode_clicked)
        
        # Setup barcode search and lazy loading
        scrollbar = self.view.ui.barcode_tableView.verticalScrollBar()
        scrollbar.valueChanged.connect(self.on_scroll)
        self.view.ui.barcode_tableView.doubleClicked.connect(self.on_cell_double_clicked)
        self.view.ui.barcode_tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.ui.barcode_tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # ค้นหาทันทีที่พิมพ์ barcode (ไม่ต้องกด Enter)
        self.view.ui.barcode_lineEdit.textChanged.connect(self.on_barcode_text_changed)
        
    def on_cell_double_clicked(self, index):
        """เมื่อ double click ที่แถวใน barcode_tableView จะแสดงรายละเอียดของ Lab Order นั้น"""
        row = index.row()
        lab_order_id = self.barcode_model.item(row, 0).text()
        lab_order_id = lab_order_id.lstrip('0')
        
        # เก็บ lab_order_id สำหรับใช้ในการส่งรายงาน
        self.current_lab_order_id = int(lab_order_id)
        
        if self.admin_comein == True:
            # Admin สามารถเลือก room_id ได้
            # TODO: เพิ่ม logic สำหรับ admin ในภายหลัง
            room_id = self.log_room_id
        else:
            room_id = self.log_room_id if hasattr(self, 'log_room_id') else None
            
        print(f"Selected Lab Order ID: {lab_order_id} from Room ID: {room_id}")
        QMessageBox.information(self.view, "เลือกแล้ว", f"เลือก Lab Order ID: {str(self.current_lab_order_id).zfill(12)}")
        
    def on_barcode_text_changed(self, text):
        """เมื่อพิมพ์ barcode ใน lineEdit - ค้นหาทันทีเมื่อครบ 12 หลัก"""
        barcode = text.strip()
        
        if barcode == "":
            # ถ้าไม่มี barcode ให้โหลดข้อมูลทั้งหมด
            self.loaded_lab_orders()
        elif len(barcode) == 12:
            # ค้นหาทันทีเมื่อครบ 12 หลัก
            barcode = barcode.lstrip('0')
            self.search_by_barcode(barcode)
        # ถ้ายังไม่ครบ 12 หลัก ไม่ทำอะไร (รอพิมพ์ต่อ)
    
    def loaded_lab_orders(self):
        """โหลดข้อมูล lab ที่รับแล้วทั้งหมด"""
        print("SendLabController: Loading all data (no barcode filter)")
        self.barcode_model.removeRows(0, self.barcode_model.rowCount())
        self.reset_lazy_loading_state()
        self.view.ui.barcode_tableView.scrollToTop()
        # Enable table เพื่อให้สามารถเลือกรายการใหม่ได้
        self.view.ui.barcode_tableView.setEnabled(True)
        # Disable search file button
        self.view.ui.search_location_file_pushButton.setEnabled(False)
        self.current_lab_order_id = None
        
        if self.admin_comein == True:
            # Admin ดูข้อมูลทุกห้อง - ส่ง empty string
            room_id = ""
            print("SendLabController: Admin mode - loading data from all rooms")
        else:
            room_id = self.log_room_id if hasattr(self, 'log_room_id') else None
        
        if room_id is not None:
            self.load_received_labs_data(room_id, self.current_offset, self.limit)
        else:
            print("SendLabController: room_id is None, cannot load data")
    
    def search_by_barcode(self, barcode):
        """ค้นหา lab ที่รับแล้วด้วย barcode"""
        self.barcode_model.removeRows(0, self.barcode_model.rowCount())
        self.view.ui.barcode_tableView.scrollToTop()
        # Enable table เพื่อให้สามารถเลือกรายการใหม่ได้
        self.view.ui.barcode_tableView.setEnabled(True)
        # Disable search file button
        self.view.ui.search_location_file_pushButton.setEnabled(False)
        self.current_lab_order_id = None
        try:
            room_id_param = "" if self.admin_comein else str(self.log_room_id)
            result = self.send_lab_service.get_received_labs_by_barcode(barcode, room_id_param)
            
            if result and result.get('found', False):
                job_progress = result['job_progress']
                self.all_data = job_progress
                
                for item in job_progress:
                    lab_order_id = str(item.get('lab_order_id', ''))
                    lab_order_id_formatted = lab_order_id.zfill(12)
                    lab_order_id_item = QStandardItem(lab_order_id_formatted)
                    lab_order_id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    row = [lab_order_id_item]
                    self.barcode_model.appendRow(row)
                
                QMessageBox.information(self.view, "Success", result.get('message', f"พบข้อมูล {len(job_progress)} รายการ"))
            else:
                message = result.get('message', 'ไม่พบข้อมูล Barcode นี้ในรายการที่รับแล้ว') if result else 'ไม่พบข้อมูล Barcode นี้ในรายการที่รับแล้ว'
                QMessageBox.warning(self.view, "Not Found", message)
                
        except Exception as e:
            QMessageBox.warning(self.view, "Search Error", f"ไม่สามารถค้นหาข้อมูลได้: {str(e)}")
    
    def on_scroll(self, value):
        """ตรวจสอบ scroll bar และโหลดข้อมูลเพิ่มเมื่อเลื่อนมาถึงจุดสุดท้าย"""
        scrollbar = self.view.ui.barcode_tableView.verticalScrollBar()
        if value >= scrollbar.maximum() - 10:
            if self.has_more_data and not self.is_loading:
                barcode = self.view.ui.barcode_lineEdit.text()
                if barcode == "":
                    self.load_more_received_labs()
    
    def load_more_received_labs(self):
        """โหลดข้อมูล lab ที่รับแล้วเพิ่มเติม"""
        if self.is_loading or not self.has_more_data:
            return
        
        # ถ้าเป็น admin ให้ส่ง empty string, ถ้าไม่ใช่ให้ส่ง room_id
        if self.admin_comein:
            room_id = ""
        else:
            room_id = self.log_room_id if hasattr(self, 'log_room_id') else None
        
        if room_id is not None:
            self.load_received_labs_data(room_id, self.current_offset, self.limit)
    
    def load_received_labs_data(self, room_id, offset, limit):
        """โหลดข้อมูล lab ที่รับแล้วจาก API"""
        if room_id is None:
            print("SendLabController: room_id is None, cannot load data")
            return
        
        room_display = "all rooms" if room_id == "" else room_id
        print(f"SendLabController: Loading data for room_id={room_display}, offset={offset}, limit={limit}")
        self.is_loading = True
        try:
            result = self.send_lab_service.get_received_labs_to_day(
                room_id=str(room_id), 
                offset=offset, 
                limit=limit
            )
            
            print(f"SendLabController: API result: {result}")
            
            if result and 'job_progress' in result:
                job_progress = result['job_progress']
                self.has_more_data = result.get('has_more', False)
                print(f"SendLabController: Found {len(job_progress)} items")
                
                for item in job_progress:
                    lab_order_id = str(item.get('lab_order_id', ''))
                    lab_order_id_formatted = lab_order_id.zfill(12)
                    lab_order_id_item = QStandardItem(lab_order_id_formatted)
                    lab_order_id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    row = [lab_order_id_item]
                    self.barcode_model.appendRow(row)
                    self.all_data.append(item)
                
                self.current_offset += len(job_progress)
            else:
                self.has_more_data = False
                
        except Exception as e:
            QMessageBox.warning(self.view, "Load Error", f"ไม่สามารถโหลดข้อมูลได้: {str(e)}")
            self.has_more_data = False
        finally:
            self.is_loading = False
    
    def reset_lazy_loading_state(self):
        """รีเซ็ตสถานะการโหลดข้อมูล"""
        self.current_offset = 0
        self.is_loading = False
        self.has_more_data = True
        self.all_data = []
    
    def clear_all_data(self):
        """เคลียร์ข้อมูลทั้งหมดเมื่อ login เข้ามาใหม่"""
        self.view.ui.barcode_lineEdit.clear()
        self.view.ui.location_file_lineEdit.clear()
        self.barcode_model.removeRows(0, self.barcode_model.rowCount())
        self.reset_lazy_loading_state()
        self.current_lab_order_id = None
    
    def reload_data(self):
        """โหลดข้อมูลใหม่เมื่อเข้าหน้า send_lab"""
        print("SendLabController: reload_data called")
        if self.log_room_id is not None:
            # เคลียร์ barcode และโหลดข้อมูลใหม่
            self.view.ui.barcode_lineEdit.clear()
            # Enable table เพื่อให้สามารถเลือกรายการใหม่ได้
            self.view.ui.barcode_tableView.setEnabled(True)
            # Disable search file button
            self.view.ui.search_location_file_pushButton.setEnabled(False)
            self.loaded_lab_orders()
        else:
            print("SendLabController: room_id not set yet, cannot reload data")
        
    def clear_pushButton_clicked(self):
        """เคลียร์ข้อมูลทั้งหมด"""
        self.view.ui.barcode_lineEdit.clear()
        self.view.ui.location_file_lineEdit.clear()
        # Enable table กลับเพื่อให้สามารถเลือกรายการใหม่ได้
        self.view.ui.barcode_tableView.setEnabled(True)
        # Disable search file button
        self.view.ui.search_location_file_pushButton.setEnabled(False)
        self.current_lab_order_id = None
        print("Clear button clicked - cleared selection")
        
    def send_pushButton_clicked(self):
        print("Send report clicked - feature under development")

    def browse_file_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, 
            "เลือกไฟล์รายงาน (Word)", 
            "", 
            "Word Files (*.docx *.doc);;All Files (*)"
        )
        
        # If the user selected a file (didn't press Cancel)
        if file_path:
            # Update the lineEdit with the full path
            self.view.ui.location_file_lineEdit.setText(file_path)
            print(f"Selected file: {file_path}")

    def convert_to_pdf_clicked(self):
        """แปลงไฟล์ Word เป็น PDF พร้อมแสดง progress bar"""
        # ตรวจสอบว่ามีไฟล์ที่เลือกหรือไม่
        word_file_path = self.view.ui.location_file_lineEdit.text().strip()
        
        if not word_file_path:
            QMessageBox.warning(self.view, "แจ้งเตือน", "กรุณาเลือกไฟล์ Word ก่อน")
            return
        
        if not os.path.exists(word_file_path):
            QMessageBox.warning(self.view, "แจ้งเตือน", "ไม่พบไฟล์ที่เลือก")
            return
        
        if not word_file_path.lower().endswith(('.docx', '.doc')):
            QMessageBox.warning(self.view, "แจ้งเตือน", "กรุณาเลือกไฟล์ Word (.docx หรือ .doc) เท่านั้น")
            return
        
        try:
            # สร้าง pdf_temp folder ถ้ายังไม่มี
            pdf_temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'pdf_temp')
            pdf_temp_dir = os.path.abspath(pdf_temp_dir)
            os.makedirs(pdf_temp_dir, exist_ok=True)
            
            # สร้างชื่อไฟล์ PDF output
            word_filename = os.path.basename(word_file_path)
            pdf_filename = os.path.splitext(word_filename)[0] + '.pdf'
            self.pdf_output_path = os.path.join(pdf_temp_dir, pdf_filename)
            
            # แสดง progress bar
            self.view.ui.convert_file_progressBar.setVisible(True)
            self.view.ui.convert_file_progressBar.setValue(0)
            self.progress_value = 0
            
            # Disable convert button ระหว่างแปลง
            self.view.ui.convert_word_to_pdf_pushButton.setEnabled(False)
            
            # เริ่ม progress animation
            self.progress_timer = QTimer()
            self.progress_timer.timeout.connect(self.update_progress)
            self.progress_timer.start(50)  # อัพเดททุก 50ms
            
            # แปลงไฟล์ในพื้นหลัง
            QTimer.singleShot(100, lambda: self.perform_conversion(word_file_path))
            
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
            self.view.ui.convert_word_to_pdf_pushButton.setEnabled(True)
            if self.progress_timer:
                self.progress_timer.stop()
    
    def update_progress(self):
        """อัพเดท progress bar"""
        if self.progress_value < 90:
            self.progress_value += 2
            self.view.ui.convert_file_progressBar.setValue(self.progress_value)
    
    def perform_conversion(self, word_file_path):
        """ทำการแปลงไฟล์จริง"""
        try:
            # แปลงไฟล์
            print(f"Converting {word_file_path} to {self.pdf_output_path}")
            convert(word_file_path, self.pdf_output_path)
            
            # อัพเดท progress เป็น 100%
            if self.progress_timer:
                self.progress_timer.stop()
            self.view.ui.convert_file_progressBar.setValue(100)
            
            # แสดง popup แจ้งเตือน
            QMessageBox.information(
                self.view, 
                "สำเร็จ", 
                f"แปลงไฟล์เป็น PDF สำเร็จ"
            )
            
            # แสดงตัวอย่าง PDF
            self.display_pdf_preview()
            
        except Exception as e:
            if self.progress_timer:
                self.progress_timer.stop()
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"ไม่สามารถแปลงไฟล์ได้: {str(e)}")
        
        finally:
            # Enable convert button กลับ
            self.view.ui.convert_word_to_pdf_pushButton.setEnabled(True)
            # ซ่อน progress bar หลัง 2 วินาที
            QTimer.singleShot(2000, lambda: self.view.ui.convert_file_progressBar.setVisible(False))
    
    def display_pdf_preview(self):
        """
        Reads the PDF file, converts it to Base64, and displays it in WebEngineView.
        """
        if self.pdf_output_path and os.path.exists(self.pdf_output_path):
            try:
                # 1. Get Absolute Path
                abs_pdf_path = os.path.abspath(self.pdf_output_path)
                
                # 2. Enable PDF Viewer settings
                # We access the settings object from the view's page
                settings = self.view.ui.preview_pdf_webEngineView.page().settings()
                settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
                settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)

                # 3. Read PDF file as binary and encode to Base64
                with open(abs_pdf_path, "rb") as f:
                    pdf_data = f.read()
                    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')

                # 4. Create HTML with embedded Base64 data
                html_content = self.create_pdf_viewer_html(base64_pdf)
                
                # 5. Load HTML
                # Use a dummy URL (http://localhost) to avoid local file restrictions
                self.view.ui.preview_pdf_webEngineView.setHtml(html_content, QUrl("http://localhost"))
                
                print(f"Loaded PDF preview for: {abs_pdf_path}")
                
            except Exception as e:
                print(f"Error displaying PDF: {str(e)}")
                QMessageBox.warning(self.view, "ข้อผิดพลาด", f"ไม่สามารถแสดงตัวอย่าง PDF ได้: {str(e)}")
        else:
            print("PDF file not found for preview")

    def create_pdf_viewer_html(self, base64_data):
        """
        Creates an HTML wrapper that embeds the PDF using Base64 data.
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>PDF Preview</title>
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
                }}
            </style>
        </head>
        <body>
            <embed 
                src="data:application/pdf;base64,{base64_data}" 
                type="application/pdf" 
                width="100%" 
                height="100%"
            >
        </body>
        </html>
        """
        return html

    def select_barcode_clicked(self):
        """
        Locks the selection and shows a confirmation popup.
        """
        # Get the selection model from the table view
        selection_model = self.view.ui.barcode_tableView.selectionModel()

        # Check if the user has actually selected a row
        if not selection_model.hasSelection():
            QMessageBox.warning(self.view, "แจ้งเตือน", "กรุณาคลิกเลือกรายการ Lab Order ในตารางก่อน")
            return

        # Get the selected row data
        selected_indexes = selection_model.selectedRows()
        if selected_indexes:
            row = selected_indexes[0].row()
            lab_order_text = self.barcode_model.item(row, 0).text()
            
            # Update the internal state with the selected ID
            self.current_lab_order_id = int(lab_order_text.lstrip('0'))
            
            # --- Key Requirement: Disable the table ---
            self.view.ui.barcode_tableView.setEnabled(False)
            
            # --- Enable search file button ---
            self.view.ui.search_location_file_pushButton.setEnabled(True)
            
            # --- Key Requirement: Show Popup ---
            QMessageBox.information(
                self.view, 
                "ยืนยันการเลือก", 
                f"เลือก Lab Order ID: {lab_order_text} สำเร็จ"
            )
            
            print(f"Locked selection on Lab Order: {self.current_lab_order_id}")
    
    def _set_room_for_user(self, room, room_id):
        """ตั้งค่าห้องแลปสำหรับผู้ใช้และโหลดข้อมูล"""
        print(f"SendLabController: _set_room_for_user called with room={room}, room_id={room_id}")
        self.log_room = room
        self.log_room_id = room_id
        
        if self.log_room == "ห้องปฏิบัติการส่วนกลาง":
            self.admin_comein = True
            print("SendLabController: Admin mode enabled - will load data from all rooms")
        else:
            self.admin_comein = False
            print(f"SendLabController: Normal user mode for room: {room}")
        
        # โหลดข้อมูล lab ที่รับแล้วครั้งแรก
        self.reset_lazy_loading_state()
        # ถ้าเป็น admin ให้ส่ง empty string, ถ้าไม่ใช่ให้ส่ง room_id
        load_room_id = "" if self.admin_comein else self.log_room_id
        self.load_received_labs_data(load_room_id, self.current_offset, self.limit)
        
        return self.log_room, self.log_room_id