import warnings
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QCompleter
from PySide6.QtCore import QObject, QStringListModel, Qt, QTimer
from barcode_utils.barcode_generator import BarcodeGenerator
from SERVICES_REGISTER.barcode_service import BarcodeService
from SERVICES_REGISTER.customer_service import CustomerService
from SERVICES_REGISTER.employee_service import EmployeeService
from SERVICES_REGISTER.work_service import WorkService

class BarcodePageController(QObject):
    """ Controller for the Barcode/Sticker Page """

    def __init__(self, view):
        super().__init__()
        self.view = view 
        self.api = BarcodeService() 
        self.customer_api = CustomerService()
        self.employee_api = EmployeeService()
        self.work_api = WorkService()  # Add WorkService for state changes

        # Initialize autocomplete variables
        self.customer_records_map = {}
        self.is_selecting = False
        self.last_search_text = ""
        self.is_printing = False  # Flag to prevent double print
        
        # Pagination state
        self.current_offset = 0
        self.limit = 100
        self.has_more = True
        self.is_loading = False
        self.total_count = 0
        self.barcode_data = []  # Store all loaded barcode data
        self.current_search_type = None  # 'today', 'customer', 'employee'
        self.current_search_params = {}  # Store search parameters for pagination
        
        # Setup autocomplete
        self._setup_autocomplete()
        self._setup_employee_autocomplete()
        
        self.event_bindings()

    @property
    def ui(self):
        if hasattr(self.view, 'ui'):
            return self.view.ui
        return self.view
    
    def _setup_autocomplete(self):
        """ Setup autocomplete for customer name search """
        # Timer for debouncing search
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._perform_search)
        self.search_delay = 400
        
        # Completer setup - parent to view to ensure proper lifecycle
        self.completer_model = QStringListModel()
        self.completer = QCompleter(self.completer_model, self.view)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        
        # Connect activated signal
        self.completer.activated.connect(self._on_customer_selected)
        
        # Set completer on the line edit
        self.ui.lineEdit_firstname.setCompleter(self.completer)
        self.ui.lineEdit_firstname.textChanged.connect(self._on_text_changed)
    
    def _on_text_changed(self, text):
        """ Called when user types in the name field """
        if self.is_selecting:
            return
        self.last_search_text = text
        self.search_timer.start(self.search_delay)
    
    def _perform_search(self):
        """ Perform API search for customer names """
        if self.is_selecting:
            return
            
        text = self.last_search_text.strip()
        if len(text) < 2:
            self.completer_model.setStringList([])
            return
            
        try:
            # Use search_customer instead of fetch_search_results
            results = self.customer_api.search_customer(text)
            if not results:
                self.completer_model.setStringList([])
                return

            # Create display names and map to records
            display_names = []
            self.customer_records_map = {}
            
            for r in results:
                name = str(r.get('name', '') or '').strip()
                surname = str(r.get('surname', '') or '').strip()
                display_name = f"{name} {surname}".strip()
                
                if display_name:
                    display_names.append(display_name)
                    if display_name not in self.customer_records_map:
                        self.customer_records_map[display_name] = []
                    self.customer_records_map[display_name].append(r)

            # Update model and show popup
            self.completer_model.setStringList(display_names)
            if display_names:
                self.completer.complete()
            
        except Exception as e:
            print(f"Search Error: {e}")
            self.completer_model.setStringList([])
    
    def _on_customer_selected(self, text):
        """ Called when user selects a customer from autocomplete """
        self.is_selecting = True
        
        try:
            records = self.customer_records_map.get(text, [])
            if records:
                r = records[0]
                
                name_val = str(r.get('name', '') or '')
                surname_val = str(r.get('surname', '') or '')
                tax_val = str(r.get('tax_id', '') or '')
                
                # Store values for delayed update (after completer finishes)
                self._pending_name = name_val
                self._pending_surname = surname_val
                self._pending_tax = tax_val
                
                # Use QTimer to set values AFTER completer finishes
                from PySide6.QtCore import QTimer
                QTimer.singleShot(10, self._apply_customer_selection)
                
        except Exception as e:
            print(f"Selection Error: {e}")
    
    def _apply_customer_selection(self):
        """ Apply the customer selection after completer finishes """
        try:
            # Block signals to prevent recursive calls
            self.ui.lineEdit_firstname.blockSignals(True)
            
            self.ui.lineEdit_firstname.setText(self._pending_name)
            self.ui.lineEdit_lastname.setText(self._pending_surname)
            self.ui.lineEdit_taxid.setText(self._pending_tax)
            
            self.ui.lineEdit_firstname.blockSignals(False)
        finally:
            self.is_selecting = False

    def _setup_employee_autocomplete(self):
        """ Setup autocomplete for employee name search (ชื่อผู้นำส่ง) """
        # Initialize employee autocomplete variables
        self.employee_records_map = {}
        self.is_selecting_employee = False
        self.last_employee_search_text = ""
        self.selected_employee_id = None
        
        # Timer for debouncing search
        self.employee_search_timer = QTimer()
        self.employee_search_timer.setSingleShot(True)
        self.employee_search_timer.timeout.connect(self._perform_employee_search)
        self.employee_search_delay = 400
        
        # Completer setup for employee
        self.employee_completer_model = QStringListModel()
        self.employee_completer = QCompleter(self.employee_completer_model, self.view)
        self.employee_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.employee_completer.setFilterMode(Qt.MatchContains)
        self.employee_completer.setCompletionMode(QCompleter.PopupCompletion)
        
        # Connect activated signal
        self.employee_completer.activated.connect(self._on_employee_selected)
        
        # Set completer on the sender line edit
        self.ui.lineEdit_sender.setCompleter(self.employee_completer)
        self.ui.lineEdit_sender.textChanged.connect(self._on_employee_text_changed)
    
    def _on_employee_text_changed(self, text):
        """ Called when user types in the employee/sender field """
        if self.is_selecting_employee:
            return
        self.last_employee_search_text = text
        self.employee_search_timer.start(self.employee_search_delay)
    
    def _perform_employee_search(self):
        """ Perform API search for employee names """
        if self.is_selecting_employee:
            return
            
        text = self.last_employee_search_text.strip()
        if len(text) < 2:
            self.employee_completer_model.setStringList([])
            return
            
        try:
            results = self.employee_api.search_employee(text)
            if not results:
                self.employee_completer_model.setStringList([])
                return

            # Create display names and map to records
            display_names = []
            self.employee_records_map = {}
            
            for r in results:
                name = str(r.get('name', '') or '').strip()
                surname = str(r.get('surname', '') or '').strip()
                display_name = f"{name} {surname}".strip()
                
                if display_name:
                    display_names.append(display_name)
                    if display_name not in self.employee_records_map:
                        self.employee_records_map[display_name] = []
                    self.employee_records_map[display_name].append(r)

            # Update model and show popup
            self.employee_completer_model.setStringList(display_names)
            if display_names:
                self.employee_completer.complete()
            
        except Exception as e:
            print(f"Employee Search Error: {e}")
            self.employee_completer_model.setStringList([])
    
    def _on_employee_selected(self, text):
        """ Called when user selects an employee from autocomplete """
        self.is_selecting_employee = True
        
        try:
            records = self.employee_records_map.get(text, [])
            # print(f"[DEBUG] _on_employee_selected: text='{text}', records={records}")
            if records:
                r = records[0]
                
                # Store the selected employee ID for later search
                self.selected_employee_id = r.get('id')
                # print(f"[DEBUG] Selected employee ID set to: {self.selected_employee_id}")
                
                name_val = str(r.get('name', '') or '')
                surname_val = str(r.get('surname', '') or '')
                
                # Store values for delayed update
                self._pending_employee_name = f"{name_val} {surname_val}".strip()
                
                # Use QTimer to set values AFTER completer finishes
                QTimer.singleShot(10, self._apply_employee_selection)
                
        except Exception as e:
            print(f"Employee Selection Error: {e}")
    
    def _apply_employee_selection(self):
        """ Apply the employee selection after completer finishes """
        try:
            # Block signals to prevent recursive calls
            self.ui.lineEdit_sender.blockSignals(True)
            self.ui.lineEdit_sender.setText(self._pending_employee_name)
            self.ui.lineEdit_sender.blockSignals(False)
        finally:
            self.is_selecting_employee = False

    def event_bindings(self):
        # Connect signals - since this is called once in __init__, no need to disconnect
        self.ui.btn_search_today.clicked.connect(self.search_today_cases)
        self.ui.btn_search_customer.clicked.connect(self.search_by_customer)
        self.ui.btn_search_employee.clicked.connect(self.search_by_employee)
        self.ui.btn_print.clicked.connect(self.print_barcode)
        
        # Bind scroll event for pagination
        self.ui.tableWidget.verticalScrollBar().valueChanged.connect(self.on_scroll)

    def search_today_cases(self):
        """ค้นหารายการในวันนี้ พร้อม Pagination"""
        self.view.clear_inputs()
        self.selected_employee_id = None  # Reset employee selection
        
        # Reset pagination state
        self.current_offset = 0
        self.barcode_data = []
        self.has_more = True
        self.current_search_type = 'today'
        self.current_search_params = {}
        
        self.ui.tableWidget.setRowCount(0)
        self.load_more_data()

    def search_by_customer(self):
        """ค้นหารายการด้วยชื่อลูกค้า พร้อม Pagination"""
        name = self.ui.lineEdit_firstname.text().strip()
        surname = self.ui.lineEdit_lastname.text().strip()

        if name == "" and surname == "":
            QMessageBox.warning(self.view, "Warning", "กรุณากรอกชื่อหรือนามสกุลเพื่อค้นหา")
            return

        # Reset pagination state
        self.current_offset = 0
        self.barcode_data = []
        self.has_more = True
        self.current_search_type = 'customer'
        self.current_search_params = {'name': name, 'surname': surname}
        
        self.ui.tableWidget.setRowCount(0)
        self.load_more_data()

    def search_by_employee(self):
        """ Search cases by employee (ชื่อผู้นำส่ง) พร้อม Pagination """
        sender_name = self.ui.lineEdit_sender.text().strip()
        
        if sender_name == "":
            QMessageBox.warning(self.view, "Warning", "กรุณากรอกชื่อพนักงานเพื่อค้นหา")
            return
        
        # If we have a selected employee ID from autocomplete, use it directly
        if self.selected_employee_id is not None:
            # Reset pagination state
            self.current_offset = 0
            self.barcode_data = []
            self.has_more = True
            self.current_search_type = 'employee'
            self.current_search_params = {'employee_id': self.selected_employee_id}
            
            self.ui.tableWidget.setRowCount(0)
            self.load_more_data()
            return
        
        # Split full name and search with first part (name) to improve matching
        search_term = sender_name.split()[0] if ' ' in sender_name else sender_name
        results = self.employee_api.search_employee(search_term)
        
        if results and len(results) > 0:
            # Find matching employee
            for emp in results:
                employee_id = emp.get('id')
                emp_name = str(emp.get('name', '') or '').strip()
                emp_surname = str(emp.get('surname', '') or '').strip()
                full_name = f"{emp_name} {emp_surname}".strip()
                
                # Only try employees that match the search name
                if sender_name in full_name or full_name in sender_name or emp_name in sender_name:
                    # Reset pagination state
                    self.current_offset = 0
                    self.barcode_data = []
                    self.has_more = True
                    self.current_search_type = 'employee'
                    self.current_search_params = {'employee_id': employee_id}
                    
                    self.ui.tableWidget.setRowCount(0)
                    self.load_more_data()
                    return
            
            QMessageBox.information(self.view, "Info", "ไม่พบข้อมูล (No data found)")
        else:
            QMessageBox.warning(self.view, "Warning", "ไม่พบพนักงานที่ค้นหา")
    
    def load_more_data(self):
        """โหลดข้อมูลเพิ่มเติมตามประเภทการค้นหา"""
        if self.is_loading or not self.has_more:
            return
        
        self.is_loading = True
        
        try:
            response_data = None
            
            if self.current_search_type == 'today':
                response_data = self.api.get_today_cases(
                    offset=self.current_offset,
                    limit=self.limit
                )
            elif self.current_search_type == 'customer':
                response_data = self.api.search_barcode_cases(
                    name=self.current_search_params.get('name', ''),
                    surname=self.current_search_params.get('surname', ''),
                    offset=self.current_offset,
                    limit=self.limit
                )
            elif self.current_search_type == 'employee':
                response_data = self.api.search_barcode_by_employee(
                    employee_id=self.current_search_params.get('employee_id'),
                    offset=self.current_offset,
                    limit=self.limit
                )
            
            if not response_data:
                if self.current_offset == 0:
                    QMessageBox.information(self.view, "Info", "ไม่พบข้อมูล (No data found)")
                self.has_more = False
                return
            
            # Handle different response formats
            new_data = []
            if isinstance(response_data, dict):
                new_data = response_data.get('data', [])
                self.total_count = response_data.get('total', 0)
                self.has_more = response_data.get('has_more', False)
            elif isinstance(response_data, list):
                new_data = response_data
                # If server doesn't support pagination yet, assume no more data
                self.has_more = len(new_data) >= self.limit
            
            if len(new_data) == 0:
                if self.current_offset == 0:
                    QMessageBox.information(self.view, "Info", "ไม่พบข้อมูล (No data found)")
                self.has_more = False
                return
            
            # Add new data to existing data
            self.barcode_data.extend(new_data)
            self.update_table()
            self.current_offset += len(new_data)
            
        except Exception as e:
            print(f"[ERROR] Exception in load_more_data: {e}")
            import traceback
            traceback.print_exc()
            if self.current_offset == 0:
                QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
            self.has_more = False
        finally:
            self.is_loading = False
    
    def on_scroll(self, value):
        """ตรวจจับการเลื่อน scroll bar"""
        scrollbar = self.ui.tableWidget.verticalScrollBar()
        # When scroll reaches 90% of maximum, load more data
        if value >= scrollbar.maximum() * 0.9:
            if self.has_more and not self.is_loading and len(self.barcode_data) > 0:
                self.load_more_data()
    
    def update_table(self):
        """อัพเดตตารางด้วยข้อมูลทั้งหมด"""
        table = self.ui.tableWidget
        table.setRowCount(len(self.barcode_data))
        
        for row_idx, item in enumerate(self.barcode_data):
            if not isinstance(item, dict):
                continue

            # 0. Date
            date_val = str(item.get('date', '-'))
            if 'T' in date_val:
                date_val = date_val.replace('T', ' ')
            date_item = QTableWidgetItem(date_val)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row_idx, 0, date_item)
            
            # 1. Barcode ID
            barcode_val = str(item.get('barcode', '')).zfill(10)
            barcode_item = QTableWidgetItem(barcode_val)
            barcode_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row_idx, 1, barcode_item)
            
            # 2. Species (ชนิดสัตว์)
            species_val = item.get('species') or '-'
            species_item = QTableWidgetItem(str(species_val))
            species_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row_idx, 2, species_item)
            
            # 3. Lab Name
            lab_name_item = QTableWidgetItem(str(item.get('lab_name', '-')))
            lab_name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row_idx, 3, lab_name_item)
            
            # 4. Storage
            storage_item = QTableWidgetItem(str(item.get('storage', '-')))
            storage_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row_idx, 4, storage_item)
            
            # 5. Urgency
            urgency_item = QTableWidgetItem(str(item.get('urgency', '-')))
            urgency_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row_idx, 5, urgency_item)
            
            # 6. Info (Sample Name)
            sample_name = item.get('sample_name') or ''
            sample_name_item = QTableWidgetItem(str(sample_name))
            sample_name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row_idx, 6, sample_name_item)
        
        # Set column widths for better display
        table.setColumnWidth(0, 180)  # Date/Time
        table.setColumnWidth(1, 120)  # Barcode ID
        table.setColumnWidth(2, 150)  # Species
        table.setColumnWidth(3, 200)  # Lab Name
        table.setColumnWidth(4, 120)  # Storage
        table.setColumnWidth(5, 100)  # Urgency
        # Column 6 (Sample Name) will stretch to fill remaining space

    def print_barcode(self):
        # Prevent double execution
        if self.is_printing:
            return
        self.is_printing = True
        
        try:
            table = self.ui.tableWidget
            selected_ranges = table.selectedRanges()
            
            if not selected_ranges:
                QMessageBox.critical(self.view, "Error", "กรุณาเลือกรายการเพื่อพิมพ์บาร์โค้ด")
                return

            selected_row = selected_ranges[0].topRow()
            
            # Get order_id (barcode) from column 1
            barcode_item = table.item(selected_row, 1)
            order_id_str = barcode_item.text() if barcode_item else ""
            
            # Debug: แสดงข้อมูลที่ได้จาก table
            # print(f"[DEBUG] Barcode string from table: '{order_id_str}'")
            
            # Parse order_id: ลบศูนย์นำหน้าแล้วแปลงเป็น int
            try:
                order_id = int(order_id_str.lstrip('0')) if order_id_str and order_id_str.strip() else 0
                # print(f"[DEBUG] Parsed order_id: {order_id}")
            except ValueError:
                # print(f"[DEBUG] Failed to parse order_id from: '{order_id_str}'")
                order_id = 0
            
            row_data = []
            for col in range(6): 
                item = table.item(selected_row, col)
                text = item.text() if item else ""
                row_data.append(text)

            data_to_print = [row_data]

            try:
                barcode_obj = BarcodeGenerator()
                barcode_obj.generate(data_to_print)
                barcode_obj.print_barcode()
                
                # Update state to "1" (printed sticker) if order_id is valid
                if order_id > 0:
                    try:
                        result = self.work_api.change_state_work(order_id, 1)
                        if result and isinstance(result, dict):
                            if result.get('status') == 'success':
                                msg = result.get('message', '')
                                if 'already' in msg:
                                    # print(f"ℹ Order {order_id}: State is already 1 or higher")
                                    pass
                                else:
                                    # print(f"✓ State updated to '1' (printed sticker) for order_id: {order_id}")
                                    pass
                            elif result.get('status') == 'error':
                                error_detail = result.get('detail', 'Unknown error')
                                # ถ้า error เป็นเรื่องของ state backwards ให้ skip โดยไม่แจ้งเตือน
                                if 'backwards' in error_detail or 'Current state is' in error_detail:
                                    # print(f"ℹ Skipping state update for order_id {order_id}: {error_detail}")
                                    pass
                                else:
                                    # print(f"✗ Failed to update state for order_id {order_id}: {error_detail}")
                                    # แจ้งเตือนเฉพาะ error ที่ไม่ใช่เรื่อง state backwards
                                    # QMessageBox.warning(
                                    #     self.view, 
                                    #     "Warning", 
                                    #     f"บาร์โค้ดพิมพ์สำเร็จ แต่ไม่สามารถอัพเดทสถานะได้\nรายละเอียด: {error_detail}"
                                    # )
                                    pass
                        else:
                            print(f"Unexpected response for order_id {order_id}: {result}")
                    except Exception as e:
                        print(f"Error updating state for order_id {order_id}: {e}")
                        import traceback
                        traceback.print_exc()
                else:
                    # print(f"Skipping state update - Invalid order_id: {order_id_str}")
                    pass
                        
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"เกิดข้อผิดพลาดในการพิมพ์: {str(e)}")
        finally:
            self.is_printing = False