from PySide6.QtWidgets import QTableWidgetItem, QMessageBox
from PySide6.QtCore import QObject, Qt
from SERVICES_REGISTER.check_job_service import CheckJobService
import traceback


class CheckJobProgressController(QObject):
    """ Controller for the Check Job Progress Page """

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.api = CheckJobService()
        
        # Store job progress data
        self.job_data = []
        
        # Pagination state
        self.current_offset = 0
        self.limit = 100
        self.has_more = True
        self.is_loading = False
        self.total_count = 0

        # Bind Events
        self.event_bindings()

    def event_bindings(self):
        self.view.ui.btn_jobs_in_system.clicked.connect(self.search_jobs_in_system)
        self.view.ui.btn_show_details.clicked.connect(self.show_job_details)
        
        # Bind scroll event to detect when reaching bottom
        self.view.ui.tableTop.verticalScrollBar().valueChanged.connect(self.on_scroll)

    def search_jobs_in_system(self):
        self.current_offset = 0
        self.job_data = []
        self.has_more = True
        
        self.view.ui.tableTop.setRowCount(0)
        self.view.ui.tableBottom.setRowCount(0)

        self.load_more_jobs()
    
    def load_more_jobs(self):
        if self.is_loading or not self.has_more:
            return
        
        self.is_loading = True
        
        try:
            result = self.api.get_job_progress(offset=self.current_offset, limit=self.limit)
            
            if not result:
                if self.current_offset == 0:
                    QMessageBox.warning(
                        self.view,
                        "ข้อผิดพลาด",
                        "ไม่สามารถเชื่อมต่อกับ API ได้"
                    )
                self.is_loading = False
                return
            
            if 'job_progress' not in result:
                if self.current_offset == 0:
                    QMessageBox.warning(
                        self.view,
                        "ข้อผิดพลาด",
                        f"รูปแบบข้อมูลไม่ถูกต้อง: {result}"
                    )
                self.is_loading = False
                return
            
            new_jobs = result['job_progress']
            self.total_count = result.get('total', 0)
            self.has_more = result.get('has_more', False)
            
            if len(new_jobs) == 0 and self.current_offset == 0:
                QMessageBox.information(
                    self.view,
                    "ไม่พบข้อมูล",
                    "ไม่มีงานในระบบในขณะนี้"
                )
                self.is_loading = False
                return
            self.job_data.extend(new_jobs)
            self.update_table()
            self.current_offset += len(new_jobs)
            
        except Exception as e:
            print(f"[ERROR] Exception in load_more_jobs: {e}")
            traceback.print_exc()
            if self.current_offset == 0:
                QMessageBox.critical(
                    self.view,
                    "ข้อผิดพลาด",
                    f"เกิดข้อผิดพลาด: {str(e)}"
                )
        finally:
            self.is_loading = False
    
    def update_table(self):
        table = self.view.ui.tableTop
        table.setRowCount(len(self.job_data))
        for row, job in enumerate(self.job_data):
            datetime_item = QTableWidgetItem(job.get('dtime', ''))
            datetime_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 0, datetime_item)
            barcode_raw = str(job.get('id', '0'))
            barcode_formatted = barcode_raw.zfill(12)
            barcode_item = QTableWidgetItem(barcode_formatted)
            barcode_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, barcode_item)
            status_item = QTableWidgetItem(job.get('tracking_info', ''))
            status_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 2, status_item)
        table.setColumnWidth(0, 200)  # วันเวลาสถานะปัจจุบัน
        table.setColumnWidth(1, 180)  # หมายเลขบาร์โค้ด
        table.setColumnWidth(2, 300)  # สถานะปัจจุบัน
    
    def on_scroll(self, value):
        scrollbar = self.view.ui.tableTop.verticalScrollBar()
        if value >= scrollbar.maximum() * 0.95:
            if self.has_more and not self.is_loading and len(self.job_data) > 0:
                self.load_more_jobs()

    def show_job_details(self):
        table_top = self.view.ui.tableTop
        selected_rows = table_top.selectedIndexes()
        
        if not selected_rows:
            QMessageBox.warning(
                self.view,
                "ไม่พบรายการที่เลือก",
                "กรุณาเลือกรายการงานจากตารางด้านบน"
            )
            return
        selected_row = selected_rows[0].row()
        selected_job = self.job_data[selected_row]
        table_bottom = self.view.ui.tableBottom
        table_bottom.setRowCount(1)
        datetime_item = QTableWidgetItem(selected_job.get('dtime', ''))
        datetime_item.setTextAlignment(Qt.AlignCenter)
        table_bottom.setItem(0, 0, datetime_item)
        barcode_raw = str(selected_job.get('id', '0'))
        barcode_formatted = barcode_raw.zfill(12)
        barcode_item = QTableWidgetItem(barcode_formatted)
        barcode_item.setTextAlignment(Qt.AlignCenter)
        table_bottom.setItem(0, 1, barcode_item)
        status_item = QTableWidgetItem(selected_job.get('tracking_info', ''))
        status_item.setTextAlignment(Qt.AlignCenter)
        table_bottom.setItem(0, 2, status_item)
        receiver_name_item = QTableWidgetItem(selected_job.get('receiver_name', ''))
        receiver_name_item.setTextAlignment(Qt.AlignCenter)
        table_bottom.setItem(0, 3, receiver_name_item)
        table_bottom.setColumnWidth(0, 200)  # เวลา
        table_bottom.setColumnWidth(1, 180)  # หมายเลขบาร์โค้ด
        table_bottom.setColumnWidth(2, 300)  # รายละเอียด
        table_bottom.setColumnWidth(3, 250)  # ผู้ดำเนินงาน
