import warnings
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QCompleter
from PySide6.QtCore import QObject, QStringListModel, Qt, QTimer
from barcode_utils.barcode_generator import BarcodeGenerator
from SERVICES_REGISTER.barcode_service import BarcodeService
from SERVICES_REGISTER.customer_service import CustomerService
from SERVICES_REGISTER.employee_service import EmployeeService

class BarcodePageController(QObject):
    """ Controller for the Barcode/Sticker Page """

    def __init__(self, view):
        super().__init__()
        self.view = view 
        self.api = BarcodeService() 
        self.customer_api = CustomerService()
        self.employee_api = EmployeeService()

        # Initialize autocomplete variables
        self.customer_records_map = {}
        self.is_selecting = False
        self.last_search_text = ""
        self.is_printing = False  # Flag to prevent double print
        
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
            results = self.customer_api.fetch_search_results(text)
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

    def search_today_cases(self):
        self.view.clear_inputs()
        self.selected_employee_id = None  # Reset employee selection
        
        # Call API
        response_data = self.api.get_today_cases()
        self.populate_table(response_data)

    def search_by_customer(self):
        name = self.ui.lineEdit_firstname.text()
        surname = self.ui.lineEdit_lastname.text()

        if name == "" and surname == "":
            QMessageBox.warning(self.view, "Warning", "กรุณากรอกชื่อหรือนามสกุลเพื่อค้นหา")
            return

        response_data = self.api.search_barcode_cases(name, surname)
        self.populate_table(response_data)

    def search_by_employee(self):
        """ Search cases by employee (ชื่อผู้นำส่ง) """
        sender_name = self.ui.lineEdit_sender.text().strip()
        
        if sender_name == "":
            QMessageBox.warning(self.view, "Warning", "กรุณากรอกชื่อพนักงานเพื่อค้นหา")
            return
        
        # If we have a selected employee ID from autocomplete, use it directly
        if self.selected_employee_id is not None:
            # print(f"[DEBUG] Using selected employee ID: {self.selected_employee_id}")
            response_data = self.api.search_barcode_by_employee(self.selected_employee_id)
            if response_data and len(response_data) > 0:
                self.populate_table(response_data)
            else:
                QMessageBox.information(self.view, "Info", "ไม่พบข้อมูล (No data found)")
            return
        
        # Split full name and search with first part (name) to improve matching
        search_term = sender_name.split()[0] if ' ' in sender_name else sender_name
        # print(f"[DEBUG] Searching for employee: {search_term} (original: {sender_name})")
        results = self.employee_api.search_employee(search_term)
        # print(f"[DEBUG] Employee search results: {results}")
        
        if results and len(results) > 0:
            # Try each matching employee until we find one with data
            found_data = False
            for emp in results:
                employee_id = emp.get('id')
                emp_name = str(emp.get('name', '') or '').strip()
                emp_surname = str(emp.get('surname', '') or '').strip()
                full_name = f"{emp_name} {emp_surname}".strip()
                
                # print(f"[DEBUG] Trying employee ID: {employee_id} ({full_name})")
                
                # Only try employees that match the search name
                if sender_name in full_name or full_name in sender_name or emp_name in sender_name:
                    response_data = self.api.search_barcode_by_employee(employee_id)
                    # print(f"[DEBUG] Barcode search response for ID {employee_id}: {len(response_data) if response_data else 0} results")
                    
                    if response_data and len(response_data) > 0:
                        self.populate_table(response_data)
                        found_data = True
                        break
            
            if not found_data:
                QMessageBox.information(self.view, "Info", "ไม่พบข้อมูล (No data found)")
        else:
            QMessageBox.warning(self.view, "Warning", "ไม่พบพนักงานที่ค้นหา")

    def populate_table(self, api_response):
        """ Populates the QTableWidget with API data """
        table = self.ui.tableWidget
        table.setRowCount(0) 

        # --- FIX: Handle different API response formats ---
        data_list = []
        
        # Case A: API returns {"status": "success", "data": [...]}
        if isinstance(api_response, dict):
            if "data" in api_response and isinstance(api_response["data"], list):
                data_list = api_response["data"]
            else:
                # API returned a dict but not the expected format, or error message
                # print(f"API returned dictionary: {api_response}")
                return

        # Case B: API returns direct list [...]
        elif isinstance(api_response, list):
            data_list = api_response
            
        # Check if empty
        if not data_list:
            QMessageBox.information(self.view, "Info", "ไม่พบข้อมูล (No data found)")
            return

        # --- Populate ---
        for row_idx, item in enumerate(data_list):
            table.insertRow(row_idx)
            
            # Validates that item is actually a dictionary
            if not isinstance(item, dict):
                continue

            # 0. Date
            date_val = str(item.get('date', '-'))
            if 'T' in date_val:
                 date_val = date_val.replace('T', ' ')
            table.setItem(row_idx, 0, QTableWidgetItem(date_val))
            
            # 1. Barcode ID
            barcode_val = str(item.get('barcode', '')).zfill(10)
            table.setItem(row_idx, 1, QTableWidgetItem(barcode_val))
            
            # 2. Species (ชนิดสัตว์)
            species_val = item.get('species') or '-'
            table.setItem(row_idx, 2, QTableWidgetItem(str(species_val)))
            
            # 3. Lab Name
            table.setItem(row_idx, 3, QTableWidgetItem(str(item.get('lab_name', '-'))))
            
            # 4. Storage
            table.setItem(row_idx, 4, QTableWidgetItem(str(item.get('storage', '-'))))
            
            # 5. Urgency
            table.setItem(row_idx, 5, QTableWidgetItem(str(item.get('urgency', '-'))))
            
            # 6. Info (Sample Name)
            sample_name = item.get('sample_name') or ''
            table.setItem(row_idx, 6, QTableWidgetItem(str(sample_name)))

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
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"เกิดข้อผิดพลาดในการพิมพ์: {str(e)}")
        finally:
            self.is_printing = False