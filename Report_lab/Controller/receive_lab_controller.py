from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QAbstractItemView
from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from View.view_receive_lab_frame import ReceiveLabFormView
from SERVICES_REPORT_LAB.receive_lab_service import ReceiveLabService

class ReceiveLabController(QObject):
    """ Controller for the Receive Lab Page """

    def __init__(self, view: ReceiveLabFormView,):
        super().__init__()
        self.view: ReceiveLabFormView = view
        self.receive_lab_service = ReceiveLabService()
        
        # Lazy loading state
        self.current_offset = 0
        self.limit = 50
        self.is_loading = False
        self.has_more_data = True
        self.all_data = []
        
        # Setup table model
        self.setup_table_model()
        
        self._setup_connections()
    
    def setup_table_model(self):
        """Setup QStandardItemModel for tableView"""
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['เวลา', 'Lab Order ID', 'ความเร็ว', 'ตัวอย่าง'])
        self.view.ui.tableView.setModel(self.model)
        
        # Set column widths to fit the table width (1261 pixels total)
        # Adjusting to prevent horizontal scrollbar
        self.view.ui.tableView.setColumnWidth(0, 180)   # เวลา
        self.view.ui.tableView.setColumnWidth(1, 220)   # Lab Order ID
        self.view.ui.tableView.setColumnWidth(2, 200)   # ความเร็ว
        self.view.ui.tableView.setColumnWidth(3, 240)   # ตัวอย่าง (remaining space)
        
        # Disable horizontal scrollbar and stretch last column
        self.view.ui.tableView.horizontalHeader().setStretchLastSection(True)
        
        # Enable grid lines for better visibility
        self.view.ui.tableView.setShowGrid(True)
        
        # Set selection behavior
        self.view.ui.tableView.setSelectionBehavior(self.view.ui.tableView.SelectionBehavior.SelectRows)
        self.view.ui.tableView.setSelectionMode(self.view.ui.tableView.SelectionMode.SingleSelection)
        
        # Alternate row colors for better readability
        self.view.ui.tableView.setAlternatingRowColors(True)
        
        
        
    
    def _setup_connections(self):
        self.view.ui.clear_pushButton.clicked.connect(self.clear_pushButton_clicked)
        self.view.ui.export_pushButton.clicked.connect(self.export_pushButton_clicked)
        self.view.ui.search_pushButton.clicked.connect(self.loaded_lab_orders)
        
        # Connect scroll event for lazy loading
        scrollbar = self.view.ui.tableView.verticalScrollBar()
        scrollbar.valueChanged.connect(self.on_scroll)
        self.view.ui.tableView.doubleClicked.connect(self.on_cell_double_clicked)
        self.view.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)

    def on_cell_double_clicked(self, index):
        """Handle double click on table cell"""
        row = index.row()
        column = index.column()
        
        # วิธีที่ 1: ดึงข้อมูลจาก model โดยตรง
        time_value = self.model.item(row, 0).text()
        lab_order_id = self.model.item(row, 1).text()
        speed = self.model.item(row, 2).text()
        sample_inspection = self.model.item(row, 3).text()

        # แสดงข้อมูล
        print(f"Cell double clicked - Row: {row}, Column: {column}")
        print(f"Time: {time_value}")
        print(f"Lab Order ID: {lab_order_id}")
        print(f"Speed: {speed}")
        print(f"Sample Inspection: {sample_inspection}")

    def clear_pushButton_clicked(self):
        print("Clear button clicked - ReceiveLabController")
        self.view.ui.barcode_lineEdit.clear()
        self.model.removeRows(0, self.model.rowCount())
        self.reset_lazy_loading_state()
        
    def export_pushButton_clicked(self):
        print("Export button clicked - ReceiveLabController")
    
    def reset_lazy_loading_state(self):
        self.current_offset = 0
        self.is_loading = False
        self.has_more_data = True
        self.all_data = []
    
    def on_scroll(self, value):
        scrollbar = self.view.ui.tableView.verticalScrollBar()
        if value >= scrollbar.maximum() - 10:
            if self.has_more_data and not self.is_loading:
                barcode = self.view.ui.barcode_lineEdit.text()
                if barcode == "":
                    self.load_more_lab_orders()
    
    def loaded_lab_orders(self):
        barcode = self.view.ui.barcode_lineEdit.text()
        
        if barcode == "":
            self.model.removeRows(0, self.model.rowCount())
            self.reset_lazy_loading_state()
            room_id = self.log_room_id if hasattr(self, 'log_room_id') else None
            self.load_lab_orders_data(room_id, self.current_offset, self.limit)
        else:
            if len(barcode) == 12:
                print("Search by barcode:", barcode)
            else:
                print("Barcode length incorrect")
                QMessageBox.warning(self.view, "Barcode Error", "เลข Barcode ต้องมีจำนวน 12 ตัวเลขเท่านั้น.")
                self.view.ui.barcode_lineEdit.clear()
                return
    
    def load_more_lab_orders(self):
        """Load more lab orders (lazy loading)"""
        if self.is_loading or not self.has_more_data:
            return
        room_id = self.log_room_id if hasattr(self, 'log_room_id') else None
        self.load_lab_orders_data(room_id, self.current_offset, self.limit)
    
    def load_lab_orders_data(self, room_id, offset, limit):
        """Load lab orders data from API"""
        if room_id is None:
            return
        self.is_loading = True
        try:
            result = self.receive_lab_service.get_lab_order_to_day(
                room_id=room_id, 
                offset=offset, 
                limit=limit
            )
            if result and 'job_progress' in result:
                job_progress = result['job_progress']
                self.has_more_data = result.get('has_more', False)
                for item in job_progress:
                    time_item = QStandardItem(str(item.get('time', '')))
                    time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    lab_order_id = str(item.get('lab_order_id', ''))
                    lab_order_id_formatted = lab_order_id.zfill(12)
                    lab_order_id_item = QStandardItem(lab_order_id_formatted)
                    lab_order_id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    speed_item = QStandardItem(str(item.get('speed', '')))
                    speed_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    sample_inspection_item = QStandardItem(str(item.get('sample_inspection', '')))
                    sample_inspection_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    row = [time_item, lab_order_id_item, speed_item, sample_inspection_item]
                    self.model.appendRow(row)
                    self.all_data.append(item)
                self.current_offset += len(job_progress)
                
            else:
                self.has_more_data = False
                
        except Exception as e:
            QMessageBox.warning(self.view, "Load Error", f"ไม่สามารถโหลดข้อมูลได้: {str(e)}")
            self.has_more_data = False
        finally:
            self.is_loading = False

    def _set_room_for_user(self, room, room_id):
        self.log_room = room
        self.log_room_id = room_id
        if self.log_room == "ห้องปฏิบัติการส่วนกลาง":
            self.log_room_id = 5
        return self.log_room, self.log_room_id

