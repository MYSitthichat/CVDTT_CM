import base64
import os
import shutil
import sys
import pythoncom
from datetime import datetime
from PySide6.QtWidgets import QMessageBox, QFileDialog, QAbstractItemView
from PySide6.QtCore import QObject, Qt, QTimer, QUrl, QThread, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWebEngineCore import QWebEngineSettings
from docx2pdf import convert
from View.view_report_from_frame import ReportFormView
from SERVICES_REPORT_LAB.send_lab_report_service import SendLabService
from SERVICES_REPORT_LAB.save_report_lab_folder_service import SaveReportLabFolderService


class ConvertPDFThread(QThread):
    finished_signal = Signal()      
    error_signal = Signal(str)       

    def __init__(self, word_path, pdf_path):
        super().__init__()
        self.word_path = word_path
        self.pdf_path = pdf_path

    def run(self):
        try:
            pythoncom.CoInitialize()
            convert(self.word_path, self.pdf_path)
            self.finished_signal.emit()
            
        except Exception as e:
            self.error_signal.emit(str(e))
            
        finally:
            pythoncom.CoUninitialize()

class SendLabController(QObject):
    """ Controller for the Send Lab Page """

    def __init__(self, view: ReportFormView, main_controller=None):
        super().__init__()
        self.view: ReportFormView = view
        self.send_lab_service = SendLabService()
        self.save_file_to_server = SaveReportLabFolderService()
        self.main_controller = main_controller
        
        # --- State Variables ---
        self.current_offset = 0
        self.limit = 50
        self.is_loading = False
        self.has_more_data = True
        self.all_data = []
        
        # Room & User Info
        self.log_room = None
        self.log_room_id = None
        self.admin_comein = False
        
        # Selection Data
        self.current_lab_order_id = None
        self.case_id = None
        self.lab_order_id = None
        self.sample_id = None
        self.room_name = None
        
        # PDF Conversion State
        self.pdf_output_path = None
        self.convert_thread = None  # ตัวเก็บ Thread Object

        # --- Setup ---
        self.setup_barcode_table_model()
        self._setup_ui()
        self._setup_connections()
        
        # --- Temp Folder Setup (วางไว้ระดับเดียวกับ Folder Project หรือ EXE) ---
        if getattr(sys, 'frozen', False):
            # กรณีรันเป็น EXE
            base_dir = os.path.dirname(sys.executable)
        else:
            current_script_path = os.path.abspath(__file__)
            controller_dir = os.path.dirname(current_script_path)
            project_dir = os.path.dirname(controller_dir)
            base_dir = os.path.dirname(project_dir)
            
        self.temp_report_dir = os.path.join(base_dir, 'temp_file_report')
        if not os.path.exists(self.temp_report_dir):
            try:
                os.makedirs(self.temp_report_dir)
                print(f"Created Temp Dir at: {self.temp_report_dir}")
            except OSError as e:
                print(f"Error creating temp dir: {e}")
                fallback_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'temp_file_report')
                os.makedirs(fallback_dir, exist_ok=True)
                self.temp_report_dir = fallback_dir

    def setup_barcode_table_model(self):
        """ตั้งค่าตารางรายการ Lab Order"""
        self.barcode_model = QStandardItemModel()
        self.barcode_model.setHorizontalHeaderLabels(['Lab Order ID'])
        self.view.ui.barcode_tableView.setModel(self.barcode_model)
        self.view.ui.barcode_tableView.setColumnWidth(0, 200)
        self.view.ui.barcode_tableView.horizontalHeader().setStretchLastSection(True)
        self.view.ui.barcode_tableView.verticalHeader().setVisible(False)
        self.view.ui.barcode_tableView.setShowGrid(True)
        self.view.ui.barcode_tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.ui.barcode_tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.view.ui.barcode_tableView.setAlternatingRowColors(True)
        self.view.ui.barcode_tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def _setup_ui(self):
        """ตั้งค่า UI เริ่มต้น (Disable ปุ่มต่างๆ)"""
        self.view.ui.search_location_file_pushButton.setEnabled(False)
        self.view.ui.convert_word_to_pdf_pushButton.setEnabled(False)
        self.view.ui.send_report_file_pushButton.setEnabled(False)
        self.view.ui.select_barcode_pushButton.setEnabled(True)
        self.view.ui.convert_file_progressBar.setVisible(False)
        self.view.ui.location_file_lineEdit.setEnabled(False)
        self.view.ui.barcode_lineEdit.setEnabled(True)
        self.view.ui.preview_pdf_webEngineView.setHtml("")
        self.view.ui.barcode_lineEdit.setPlaceholderText("พิมพ์ หรือเลือกจากตารางด้านล่าง")
        self.view.ui.clear_location_file_pushButton.setEnabled(False)
        self.view.ui.barcode_lineEdit.clear()
        self.view.ui.location_file_lineEdit.clear()
    
    def _setup_ui_select(self):
        """ตั้งค่า UI เมื่อเลือกรายการแล้ว (Enable ปุ่มต่างๆ)"""
        self.view.ui.search_location_file_pushButton.setEnabled(True)
        self.view.ui.convert_word_to_pdf_pushButton.setEnabled(True)
        self.view.ui.send_report_file_pushButton.setEnabled(True)
        self.view.ui.clear_location_file_pushButton.setEnabled(True)
        self.view.ui.convert_file_progressBar.setVisible(False)
        self.view.ui.select_barcode_pushButton.setEnabled(False)
        self.view.ui.location_file_lineEdit.setEnabled(True)
        self.view.ui.barcode_lineEdit.setEnabled(False)

    def _setup_connections(self):
        self.view.ui.search_location_file_pushButton.clicked.connect(self.browse_file_clicked)
        self.view.ui.clear_location_file_pushButton.clicked.connect(self.clear_pushButton_clicked)
        self.view.ui.send_report_file_pushButton.clicked.connect(self.send_pushButton_clicked)
        self.view.ui.convert_word_to_pdf_pushButton.clicked.connect(self.convert_to_pdf_clicked)
        self.view.ui.select_barcode_pushButton.clicked.connect(self.select_barcode_clicked)
        scrollbar = self.view.ui.barcode_tableView.verticalScrollBar()
        scrollbar.valueChanged.connect(self.on_scroll)
        self.view.ui.barcode_tableView.doubleClicked.connect(self.on_cell_double_clicked)
        self.view.ui.barcode_lineEdit.textChanged.connect(self.on_barcode_text_changed)
        
        self.clear_log_data()


    def send_pushButton_clicked(self):
        if not self.current_lab_order_id:
            QMessageBox.warning(self.view, "แจ้งเตือน", "กรุณาเลือกรายการ Lab Order")
            return

        original_word_path = self.view.ui.location_file_lineEdit.text().strip()
        if not original_word_path or not os.path.exists(original_word_path):
            QMessageBox.warning(self.view, "แจ้งเตือน", "ไม่พบไฟล์ Word ต้นฉบับ")
            return

        if not self.pdf_output_path or not os.path.exists(self.pdf_output_path):
            QMessageBox.warning(self.view, "แจ้งเตือน", "กรุณากดแปลงไฟล์เป็น PDF ก่อนส่ง")
            return
            
        if not self.room_name:
            QMessageBox.warning(self.view, "ข้อมูลไม่ครบ", "ไม่พบข้อมูลห้องปฏิบัติการ (Room Name)")
            return
        
        if not all([self.case_id, self.lab_order_id, self.log_room_id]):
            QMessageBox.warning(self.view, "ข้อมูลไม่ครบ", "ข้อมูล Case ID หรือ Room ID ไม่ถูกต้อง")
            return
        current_user_id = 1
        if self.main_controller and hasattr(self.main_controller, 'user_id'):
            current_user_id = self.main_controller.user_id

        temp_word_path = None
        temp_pdf_path = None

        try:
            self.view.ui.send_report_file_pushButton.setEnabled(False)
            self.view.ui.send_report_file_pushButton.setText("กำลังส่งไฟล์...")
            dTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            barcode_str = str(self.current_lab_order_id).zfill(12)
            case_id_str = str(self.case_id)
            new_filename = f"{barcode_str}_{case_id_str}_{dTime}"
            temp_word_path = os.path.join(self.temp_report_dir, f"{new_filename}.docx")
            temp_pdf_path = os.path.join(self.temp_report_dir, f"{new_filename}.pdf")
            shutil.copy2(original_word_path, temp_word_path)
            shutil.copy2(self.pdf_output_path, temp_pdf_path)
            result = self.save_file_to_server.save_report_files(
                lab_name=self.room_name,
                barcode=barcode_str,
                lab_id=self.lab_order_id,
                case_id=self.case_id,           
                room_id=self.log_room_id,       
                updater=current_user_id,        
                date_str=dTime,
                word_path=temp_word_path,
                pdf_path=temp_pdf_path
            )
            if result and result.get('status') == 'success':
                QMessageBox.information(self.view, "สำเร็จ", "ส่งไฟล์และบันทึกข้อมูลเรียบร้อยแล้ว")
                self.clear_log_data()
                self.clear_pushButton_clicked()
                self.view.ui.convert_file_progressBar.setValue(0)
                self.view.ui.preview_pdf_webEngineView.setHtml("")
            else:
                msg = result.get('message', 'Unknown Error') if result else 'Unknown Error'
                QMessageBox.critical(self.view, "ล้มเหลว", f"Server Error:\n{msg}")

        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"เกิดข้อผิดพลาด: {str(e)}")
            
        finally:
            for f in [temp_word_path, temp_pdf_path]:
                if f and os.path.exists(f):
                    try: os.remove(f)
                    except: pass
            self.view.ui.send_report_file_pushButton.setText("ส่งใบส่งแลป")

    def convert_to_pdf_clicked(self):
        """เริ่มกระบวนการแปลงไฟล์โดยใช้ Thread"""
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
        self.pdf_output_path = os.path.join(self.temp_report_dir, 'preview_temp.pdf')
        self.view.ui.convert_file_progressBar.setVisible(True)
        self.view.ui.convert_file_progressBar.setRange(0, 0) 
        self.view.ui.convert_word_to_pdf_pushButton.setEnabled(False)
        self.convert_thread = ConvertPDFThread(word_file_path, self.pdf_output_path)
        self.convert_thread.finished_signal.connect(self.on_conversion_finished)
        self.convert_thread.error_signal.connect(self.on_conversion_error)
        self.convert_thread.start()

    def on_conversion_finished(self):
        """ทำงานเมื่อแปลงไฟล์เสร็จ"""
        self.view.ui.convert_file_progressBar.setRange(0, 100)
        self.view.ui.convert_file_progressBar.setValue(100)
        self.view.ui.convert_file_progressBar.setVisible(False)
        
        self.view.ui.convert_word_to_pdf_pushButton.setEnabled(True)
        
        QMessageBox.information(self.view, "สำเร็จ", "แปลงไฟล์เป็น PDF สำเร็จ")
        self.display_pdf_preview()
        self.convert_thread = None

    def on_conversion_error(self, error_msg):
        """ทำงานเมื่อแปลงไฟล์ Error"""
        self.view.ui.convert_file_progressBar.setRange(0, 100)
        self.view.ui.convert_file_progressBar.setVisible(False)
        self.view.ui.convert_word_to_pdf_pushButton.setEnabled(True)
        QMessageBox.critical(self.view, "ข้อผิดพลาด", f"ไม่สามารถแปลงไฟล์ได้: {error_msg}")
        self.convert_thread = None

    def display_pdf_preview(self):
        """แสดงตัวอย่าง PDF ใน WebEngineView"""
        if self.pdf_output_path and os.path.exists(self.pdf_output_path):
            try:
                abs_pdf_path = os.path.abspath(self.pdf_output_path)
                settings = self.view.ui.preview_pdf_webEngineView.page().settings()
                settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
                settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
                with open(abs_pdf_path, "rb") as f:
                    pdf_data = f.read()
                    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
                pdf_filename = os.path.basename(abs_pdf_path)
                html_content = self.create_pdf_viewer_html(base64_pdf, pdf_filename)
                self.view.ui.preview_pdf_webEngineView.setHtml(html_content, QUrl("http://localhost"))
            except Exception as e:
                print(f"Error displaying PDF: {str(e)}")
                QMessageBox.warning(self.view, "ข้อผิดพลาด", f"ไม่สามารถแสดงตัวอย่าง PDF ได้: {str(e)}")
        else:
            print("PDF file not found for preview")

    def create_pdf_viewer_html(self, base64_data, filename="document.pdf"):
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{filename}</title>
            <style>
                body, html {{ margin: 0; padding: 0; height: 100%; overflow: hidden; background-color: #525659; }}
                embed {{ width: 100%; height: 100%; border: none; }}
            </style>
        </head>
        <body>
            <embed 
                src="data:application/pdf;base64,{base64_data}#toolbar=1&navpanes=0&scrollbar=1&page=1&view=FitH" 
                type="application/pdf" width="100%" height="100%"
            >
        </body>
        </html>
        """

    def browse_file_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, "เลือกไฟล์รายงาน (Word)", "", "Word Files (*.docx *.doc);;All Files (*)"
        )
        if file_path:
            self.view.ui.location_file_lineEdit.setText(file_path)

    def select_barcode_clicked(self):
        selection_model = self.view.ui.barcode_tableView.selectionModel()
        if not selection_model.hasSelection():
            QMessageBox.warning(self.view, "แจ้งเตือน", "กรุณาคลิกเลือกรายการ Lab Order ในตารางก่อน")
            return
        selected_indexes = selection_model.selectedRows()
        if selected_indexes:
            row = selected_indexes[0].row()
            lab_order_text = self.barcode_model.item(row, 0).text()
            self.current_lab_order_id = int(lab_order_text.lstrip('0'))
            self.view.ui.barcode_tableView.setEnabled(False)
            self.get_data_by_lab_order_id(self.current_lab_order_id)
            QMessageBox.information(self.view, "ยืนยันการเลือก", f"เลือก Lab Order ID: {lab_order_text} สำเร็จ")
            self._setup_ui_select()

    def get_data_by_lab_order_id(self, lab_order_id):
        result = self.send_lab_service.get_detail_by_laborder(int(lab_order_id))
        if result:
            self.case_id = result.get('case_id')
            self.lab_order_id = result.get('lab_order_id')
            self.sample_id = result.get('sample_id')
            self.room_name = result.get('room_name')
            print(f"Data Loaded: Case={self.case_id}, LabOrder={self.lab_order_id}, Room={self.room_name}")

    def on_cell_double_clicked(self, index):
        row = index.row()
        lab_order_text = self.barcode_model.item(row, 0).text()
        self.current_lab_order_id = int(lab_order_text.lstrip('0'))
        QMessageBox.information(self.view, "เลือกแล้ว", f"เลือก Lab Order ID: {lab_order_text}")

    def on_barcode_text_changed(self, text):
        barcode = text.strip()
        if barcode == "":
            self.loaded_lab_orders()
        elif len(barcode) == 12:
            self.search_by_barcode(barcode.lstrip('0'))

    def loaded_lab_orders(self):
        self.barcode_model.removeRows(0, self.barcode_model.rowCount())
        self.reset_lazy_loading_state()
        self.view.ui.barcode_tableView.scrollToTop()
        self.view.ui.barcode_tableView.setEnabled(True)
        self.view.ui.search_location_file_pushButton.setEnabled(False)
        self.current_lab_order_id = None
        
        load_room_id = "" if self.admin_comein else self.log_room_id
        if load_room_id is not None:
            self.load_received_labs_data(load_room_id, self.current_offset, self.limit)

    def search_by_barcode(self, barcode):
        self.barcode_model.removeRows(0, self.barcode_model.rowCount())
        self.view.ui.barcode_tableView.scrollToTop()
        self.view.ui.barcode_tableView.setEnabled(True)
        self.view.ui.search_location_file_pushButton.setEnabled(False)
        self.current_lab_order_id = None
        
        try:
            room_id_param = "" if self.admin_comein else str(self.log_room_id)
            result = self.send_lab_service.get_received_labs_by_barcode(barcode, room_id_param)
            
            if result and result.get('found', False):
                for item in result['job_progress']:
                    self._add_row_to_table(item)
                QMessageBox.information(self.view, "Success", result.get('message', "พบข้อมูล"))
            else:
                QMessageBox.warning(self.view, "Not Found", "ไม่พบข้อมูล Barcode นี้")
        except Exception as e:
            QMessageBox.warning(self.view, "Error", str(e))

    def load_received_labs_data(self, room_id, offset, limit):
        self.is_loading = True
        try:
            result = self.send_lab_service.get_received_labs_to_day(str(room_id), offset, limit)
            if result and 'job_progress' in result:
                self.has_more_data = result.get('has_more', False)
                for item in result['job_progress']:
                    self._add_row_to_table(item)
                    self.all_data.append(item)
                self.current_offset += len(result['job_progress'])
            else:
                self.has_more_data = False
        except Exception as e:
            print(f"Load Error: {e}")
        finally:
            self.is_loading = False

    def _add_row_to_table(self, item):
        lab_id = str(item.get('lab_order_id', '')).zfill(12)
        item_obj = QStandardItem(lab_id)
        item_obj.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.barcode_model.appendRow([item_obj])

    def on_scroll(self, value):
        scrollbar = self.view.ui.barcode_tableView.verticalScrollBar()
        if value >= scrollbar.maximum() - 10:
            if self.has_more_data and not self.is_loading:
                if not self.view.ui.barcode_lineEdit.text():
                    self.load_more_received_labs()

    def load_more_received_labs(self):
        load_room_id = "" if self.admin_comein else self.log_room_id
        if load_room_id is not None:
            self.load_received_labs_data(load_room_id, self.current_offset, self.limit)

    def reset_lazy_loading_state(self):
        self.current_offset = 0
        self.is_loading = False
        self.has_more_data = True
        self.all_data = []

    def clear_log_data(self):
        self.case_id = None
        self.lab_order_id = None
        self.sample_id = None
        self.room_name = None

    def clear_pushButton_clicked(self):
        self.view.ui.barcode_lineEdit.clear()
        self.view.ui.location_file_lineEdit.clear()
        self.view.ui.barcode_tableView.setEnabled(True)
        self.view.ui.search_location_file_pushButton.setEnabled(False)
        self.current_lab_order_id = None
        self._setup_ui()

    def _set_room_for_user(self, room, room_id):
        self.log_room = room
        self.log_room_id = room_id
        self.admin_comein = (self.log_room == "ห้องปฏิบัติการส่วนกลาง")
        self.reset_lazy_loading_state()
        self.loaded_lab_orders()
        return self.log_room, self.log_room_id
    
    def reload_data(self):
        if self.log_room_id is not None:
            self.view.ui.barcode_lineEdit.clear()
            self.view.ui.barcode_tableView.setEnabled(True)
            self.view.ui.search_location_file_pushButton.setEnabled(False)
            self.loaded_lab_orders()

    def clear_all_data(self):
        self.clear_pushButton_clicked()
        self.barcode_model.removeRows(0, self.barcode_model.rowCount())
        self.reset_lazy_loading_state()