from PySide6.QtWidgets import QMessageBox, QAbstractItemView
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
        # Room and access control state
        self.log_room = None
        self.log_room_id = None
        self.admin_comein = False
        # Setup table model
        self.setup_table_model()
        
        self._setup_connections()
    
    def setup_table_model(self):
        """Setup QStandardItemModel for tableView"""
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['เวลา', 'Lab Order ID', 'ความเร็ว', 'ตัวอย่าง'])
        self.view.ui.tableView.setModel(self.model)
        self.view.ui.tableView.setColumnWidth(0, 180)   # เวลา
        self.view.ui.tableView.setColumnWidth(1, 220)   # Lab Order ID
        self.view.ui.tableView.setColumnWidth(2, 200)   # ความเร็ว
        self.view.ui.tableView.setColumnWidth(3, 240)   # ตัวอย่าง (remaining space)
        self.view.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.view.ui.tableView.setShowGrid(True)
        self.view.ui.tableView.setSelectionBehavior(self.view.ui.tableView.SelectionBehavior.SelectRows)
        self.view.ui.tableView.setSelectionMode(self.view.ui.tableView.SelectionMode.SingleSelection)
        self.view.ui.tableView.setAlternatingRowColors(True)
        
        
        
    
    def _setup_connections(self):
        self.view.ui.clear_pushButton.clicked.connect(self.clear_pushButton_clicked)
        self.view.ui.export_pushButton.clicked.connect(self.export_pushButton_clicked)
        self.view.ui.search_pushButton.clicked.connect(self.loaded_lab_orders)
        self.view.ui.receive_pushButton.clicked.connect(self.receive_lab_orders)
        scrollbar = self.view.ui.tableView.verticalScrollBar()
        scrollbar.valueChanged.connect(self.on_scroll)
        self.view.ui.tableView.doubleClicked.connect(self.on_cell_double_clicked)
        self.view.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)



    def on_cell_double_clicked(self, index):
        """เมื่อ double click ที่แถวใน tableView จะแสดงรายละเอียดของ Lab Order นั้น"""
        row = index.row()
        lab_order_id = self.model.item(row, 1).text()
        lab_order_id = lab_order_id.lstrip('0')
        if self.admin_comein == True:
            room_id = self.view.get_type_search()
        else:
            room_id = self.log_room_id if hasattr(self, 'log_room_id') else None
            
        print(f"Lab Order ID: {lab_order_id} from Room ID: {room_id}")
        
        
        
        
        
    def receive_lab_orders(self):
        print("RECEIVE BUTTON CLICKED - ReceiveLabController")
        


    def export_pushButton_clicked(self):
        print("Export button clicked - ReceiveLabController")



    def clear_pushButton_clicked(self):
        self.view.ui.barcode_lineEdit.clear()
        self.model.removeRows(0, self.model.rowCount())
        self.reset_lazy_loading_state()
    
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
        barcode = self.view.ui.barcode_lineEdit.text().strip()
        if barcode == "":
            self.view.clear_all_table()
            self.model.removeRows(0, self.model.rowCount())
            self.reset_lazy_loading_state()
            self.view.ui.tableView.scrollToTop()
            if self.admin_comein == True:
                room_id = self.view.get_type_search()
            else:
                room_id = self.log_room_id if hasattr(self, 'log_room_id') else None
            self.load_lab_orders_data(room_id, self.current_offset, self.limit)
        else:
            if len(barcode) == 12:
                barcode = barcode.lstrip('0')
                self.search_by_barcode(barcode)
            else:
                QMessageBox.warning(self.view, "Barcode Error", "เลข Barcode ต้องมีจำนวน 12 ตัวเลขเท่านั้น.")
                self.view.ui.barcode_lineEdit.clear()
                return
    
    def search_by_barcode(self, barcode):
        """Search lab orders by barcode"""
        self.model.removeRows(0, self.model.rowCount())
        self.view.ui.tableView.scrollToTop()
        try:
            room_id_param = "" if self.admin_comein else str(self.log_room_id)
            result = self.receive_lab_service.get_lab_order_by_barcode(barcode, room_id_param)
            if result and result.get('found', False):
                job_progress = result['job_progress']
                self.all_data = job_progress
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
                QMessageBox.information(self.view, "Success", result.get('message', f"พบข้อมูล {len(job_progress)} รายการ"))
            else:
                message = result.get('message', 'ไม่พบข้อมูล Barcode นี้') if result else 'ไม่พบข้อมูล Barcode นี้'
                QMessageBox.warning(self.view, "Not Found", message)
                
        except Exception as e:
            QMessageBox.warning(self.view, "Search Error", f"ไม่สามารถค้นหาข้อมูลได้: {str(e)}")
    
    
    def load_more_lab_orders(self):
        if self.is_loading or not self.has_more_data:
            return
        room_id = self.log_room_id if hasattr(self, 'log_room_id') else None
        self.load_lab_orders_data(room_id, self.current_offset, self.limit)
    
    def load_lab_orders_data(self, room_id, offset, limit):
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
            self.admin_comein = True
            self.view.show_radio_buttons()
            self.log_room_id = self.view.get_type_search()
        else:
            self.admin_comein = False
            self.view.hide_radio_buttons()
        return self.log_room, self.log_room_id
    