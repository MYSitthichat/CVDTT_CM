from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox
from API.client_app import APIApp


class AfterDeathPageController(QObject):
    """Controller for the After Death Service Page"""
    
    # Signals for communication
    data_saved = Signal(str)  # Emits sample_id when data is saved
    navigation_requested = Signal(str)  # Emits target page name
    
    def __init__(self, model, view, main_controller):
        """
        Initialize the controller
        
        Args:
            model: Database model for after death services
            view: AfterDeathPageWidget instance
            main_controller: Main application controller
        """
        super().__init__()
        self.model = model
        self.view = view
        self.main_controller = main_controller
        self.api_client = APIApp()
        
        # State tracking
        self.current_sample_id = None
        self.is_editing = False
        
        self.event_bindings()
        self._setup_ui_state()

    def event_bindings(self):
        """Bind UI events to controller methods"""
        # Button events
        self.view.ui.btn_save.clicked.connect(self.save_data)
        self.view.ui.btn_cancel.clicked.connect(self.cancel_and_go_back)
        
        # Radio button events for dynamic UI updates
        self.view.ui.rb_waste.toggled.connect(self._on_service_type_changed)
        self.view.ui.rb_cremation.toggled.connect(self._on_service_type_changed)
        self.view.ui.rb_jewelry.toggled.connect(self._on_service_type_changed)

    def _setup_ui_state(self):
        """Setup initial UI state"""
        # Set default selection
        self.view.ui.rb_waste.setChecked(True)
        
        # Disable save button until data is entered
        self.view.ui.btn_save.setEnabled(True)

    def _on_service_type_changed(self, checked):
        """
        Handle service type selection changes
        Optional: Enable/disable relevant sections
        """
        if checked:
            sender = self.sender()
            # print(f"Service type changed to: {sender.text()}")
            
            # You can add logic here to show/hide group boxes
            # based on selected service type
            
    # ==================== Data Retrieval Methods ====================
    
    def _get_sample_id(self):
        """
        Extract Sample ID from specimen page
        NOTE: For compatibility with old system, actual sample_id is NOT used in database
        (Database always uses '10' - see server_api.py)
        This is kept for display/reference purposes only
        
        Returns:
            str: Sample ID or '10' as fallback (matches old system)
        """
        try:
            # Try to get from specimen widget
            if hasattr(self.main_controller, 'specimen_widget'):
                specimen_widget = self.main_controller.specimen_widget
                
                # Try to get sample ID from the label
                if hasattr(specimen_widget.ui, 'specimen_ID_label'):
                    sample_id_text = specimen_widget.ui.specimen_ID_label.text()
                    
                    # Parse "Sample ID: XXXXX" format or just "XXXXX"
                    if sample_id_text:
                        # If it contains ":", split and get the part after it
                        if ":" in sample_id_text:
                            sample_id = sample_id_text.split(":")[1].strip()
                        else:
                            sample_id = sample_id_text.strip()
                        
                        # Accept any non-empty value (no validation needed - not used in DB)
                        if sample_id:
                            self.current_sample_id = sample_id
                            # print(f"[Controller] Found sample_id from specimen: {sample_id} (for reference only)")
                            return sample_id
            
            # Fallback: Return '10' to match old system behavior
            # print("[Controller] No sample_id found, using '10' (matches old system)")
            self.current_sample_id = "10"
            return "10"
            
        except Exception as e:
            print(f"[Controller] Error getting sample_id: {e}, using '10' as fallback")
            self.current_sample_id = "10"
            return "10"

    def _get_user_id(self):
        """
        Get current logged-in user ID
        
        Returns:
            int: User ID or None if not logged in
        """
        try:
            if (hasattr(self.main_controller, 'user_login_info') and 
                self.main_controller.user_login_info):
                
                # user_login_info structure: [(user_info_tuple)]
                # user_info_tuple[1] is user_id
                user_id = self.main_controller.user_login_info[0][1]
                return user_id
            
            # Fallback: Check for test mode
            # print("Warning: No user login info found")
            
            # For testing, return a default user ID (1 = admin/system user)
            return 1  # Changed from None to 1 for testing
            
        except (IndexError, TypeError, AttributeError) as e:
            print(f"Error getting user ID: {e}")
            return 1  # Return default user ID instead of None

    def _get_user_name(self):
        """
        Get current logged-in user's full name
        
        Returns:
            str: User's full name or "Unknown User"
        """
        try:
            if (hasattr(self.main_controller, 'user_login_info') and 
                self.main_controller.user_login_info):
                
                user_info = self.main_controller.user_login_info[0]
                # Assuming structure: [id, user_id, username, fname, lname, ...]
                if len(user_info) >= 5:
                    fname = user_info[3] or ""
                    lname = user_info[4] or ""
                    return f"{fname} {lname}".strip()
            
            return "Unknown User"
            
        except Exception as e:
            print(f"Error getting user name: {e}")
            return "Unknown User"

    # ==================== Data Validation Methods ====================
    
    def _validate_data(self, data):
        """
        Validate form data before saving
        
        Args:
            data (dict): Form data to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Check if service type is selected
        service_type = data.get('service_type')
        
        if not service_type or service_type == 'Unknown':
            QMessageBox.warning(
                self.view, 
                "Validation Error", 
                "กรุณาเลือกประเภทบริการ"
            )
            return False

        # Validate based on service type
        if service_type == 'Infectious Waste':
            waste_details = data.get('waste_details')
            if not waste_details:  # No data filled
                QMessageBox.warning(
                    self.view, 
                    "Validation Error", 
                    "กรุณากรอกข้อมูลขยะติดเชื้อ"
                )
                return False
            return self._validate_waste_data(waste_details)
            
        elif service_type == 'Cremation':
            cremation_details = data.get('cremation_details')
            if not cremation_details:  # No data filled
                QMessageBox.warning(
                    self.view, 
                    "Validation Error", 
                    "กรุณากรอกข้อมูลการฌาปนกิจ"
                )
                return False
            return self._validate_cremation_data(cremation_details)
            
        elif service_type == 'Jewelry':
            jewelry_details = data.get('jewelry_details')
            if not jewelry_details:  # No data filled
                QMessageBox.warning(
                    self.view, 
                    "Validation Error", 
                    "กรุณากรอกข้อมูลเครื่องประดับ"
                )
                return False
            return self._validate_jewelry_data(jewelry_details)

        return True

    def _validate_waste_data(self, waste_data):
        """Validate infectious waste data - now supports multiple checkbox selections"""
        items = waste_data.get('items', [])
        
        if not items:
            QMessageBox.warning(
                self.view, 
                "Validation Error", 
                "กรุณาเลือกรายการขยะติดเชื้อออย่างน้อย 1 รายการ"
            )
            return False
        
        # Validate that selected items have quantity or weight
        for item in items:
            if not any(word in item.lower() for word in ['qty', 'kg', 'weight']):
                QMessageBox.warning(
                    self.view,
                    "Validation Warning",
                    f"รายการ '{item.split(':')[0]}' ไม่มีข้อมูลจำนวนหรือน้ำหนัก\n"
                    "กรุณากรอกข้อมูลให้ครบถ้วน"
                )
                return False
        
        return True

    def _validate_cremation_data(self, cremation_data):
        """Validate cremation service data - now supports multiple checkbox selections"""
        request_type = cremation_data.get('request_type', '')
        
        if not request_type:
            QMessageBox.warning(
                self.view, 
                "Validation Error", 
                "กรุณาเลือกประเภทการฌาปนกิจ"
            )
            return False
        
        # Check if ceremony date is provided for ceremony service
        if 'Ceremony' in request_type:
            date = cremation_data.get('date', '')
            if not date or date in ["01/01/2000"]:
                QMessageBox.warning(
                    self.view, 
                    "Validation Error", 
                    "กรุณาระบุวันที่"
                )
                return False
        
        # Check if incineration weight is provided when incineration is selected
        if 'Incineration' in request_type and '(' not in request_type:
            reply = QMessageBox.question(
                self.view,
                'Confirmation',
                'ไม่ได้ระบุน้ำหนักสำหรับการเผา ต้องการดำเนินการต่อหรือไม่?\n',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return False
        
        return True

    def _validate_jewelry_data(self, jewelry_data):
        """Validate jewelry service data - now supports multiple selections"""
        material = jewelry_data.get('material', '')
        
        if not material:
            QMessageBox.warning(
                self.view, 
                "Validation Error", 
                "กรุณาเลือกวัสดุที่ใช้ทำเครื่องประดับ\n"
            )
            return False
        
        # Optional: Warn if size not specified
        size = jewelry_data.get('size', '')
        if not size:
            reply = QMessageBox.question(
                self.view,
                'Confirmation',
                'ไม่ได้ระบุขนาดเพชร ต้องการดำเนินการต่อหรือไม่?\n',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return False
        
        # Validate that if jewelry type is selected, at least one accessory checkbox is checked
        jewelry_type = jewelry_data.get('jewelry_type', '')
        if not jewelry_type:
            reply = QMessageBox.question(
                self.view,
                'Confirmation',
                'ไม่ได้เลือกประเภทเครื่องประดับ ต้องการดำเนินการต่อหรือไม่?\n',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return False
        
        return True

    # ==================== Data Saving Methods ====================
    
    def save_data(self):
        """
        Main method to save after death service data
        Orchestrates the entire save process
        """
        # print("=" * 60)
        # print("ACTION: Save After Death Data")
        # print("=" * 60)
        
        # Step 1: Get Sample ID
        sample_id = self._get_sample_id()
        if not sample_id:
            return  # Error message already shown
        
        # print(f"Sample ID: {sample_id}")
        
        # Step 2: Get User ID
        user_id = self._get_user_id()
        if not user_id:
            QMessageBox.warning(
                self.view, 
                "Warning", 
                "ไม่พบข้อมูลผู้ใช้ กรุณาเข้าสู่ระบบใหม่\n"
            )
            return
        
        user_name = self._get_user_name()
        # print(f"User: {user_name} (ID: {user_id})")
        
        # Step 3: Get Data from View
        data = self.view.get_data()
        # print(f"Service Type: {data.get('service_type')}")
        # print(f"Data: {data}")
        
        # Step 4: Validate Data
        if not self._validate_data(data):
            return  # Validation message already shown
        
        # Step 5: Confirm before saving
        if not self._confirm_save(data):
            # print("Save cancelled by user")
            return
        
        # Step 6: Save to Database
        if self._save_to_database(sample_id, data, user_id):
            # Success
            QMessageBox.information(
                self.view, 
                "Success", 
                "บันทึกข้อมูลเรียบร้อยแล้ว\n"
            )
            
            # Emit signal for other components
            self.data_saved.emit(sample_id)
            
            # Clear form
            self.view.clear_page()
            
            # Navigate back
            self.go_back_to_new_work()
            
            # print("=" * 60)
            # print("Save completed successfully")
            # print("=" * 60)
        else:
            # Error message already shown in _save_to_database
            # print("=" * 60)
            # print("Save failed")
            # print("=" * 60)
            pass

    def _confirm_save(self, data):
        """
        Show confirmation dialog before saving
        
        Args:
            data (dict): Data to be saved
            
        Returns:
            bool: True if user confirms, False otherwise
        """
        service_type = data.get('service_type', 'Unknown')
        
        message = (
            f"ยืนยันการบันทึกข้อมูล\n"
            f"Sample ID: {self.current_sample_id}\n"
            f"Service: {service_type}\n\n"
            f"ต้องการบันทึกข้อมูลหรือไม่?"
        )
        
        reply = QMessageBox.question(
            self.view,
            'ยืนยันการบันทึก',
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        return reply == QMessageBox.Yes

    def _save_to_database(self, sample_id, data, user_id):
        """
        Save data to database and track status
        
        Args:
            sample_id (str): Sample identifier
            data (dict): Form data
            user_id (int): Current user ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # print("Saving to database...")
            
            service_type = data.get('service_type', 'Unknown')
            # print(f"Sample ID: {sample_id}")
            # print(f"Service Type: {service_type}")
            # print(f"User ID: {user_id}")
            # print(f"Full Data: {data}")
            
            # Save to database via API
            success = self.api_client.save_after_death(
                sample_id=sample_id,
                service_type=service_type,
                service_data=data,
                user_id=user_id
            )
            
            if not success:
                QMessageBox.critical(
                    self.view, 
                    "Database Error", 
                    "ไม่สามารถบันทึกข้อมูลได้\n"
                )
                return False
            
            # print("Main data saved successfully to database")
            
            # Save tracking information
            service_desc = f"After Death Service: {service_type}"
            
            # Add more details based on service type (now with multiple selections)
            if service_type == 'Infectious Waste':
                items = data.get('waste_details', {}).get('items', [])
                if items:
                    service_desc += f" - {len(items)} items"
                    # Add item names (first 3 only if many)
                    item_names = [item.split(':')[0] for item in items]
                    if len(item_names) <= 3:
                        service_desc += f" ({', '.join(item_names)})"
                    else:
                        service_desc += f" ({', '.join(item_names[:3])}, ...)"
            elif service_type == 'Cremation':
                req_type = data.get('cremation_details', {}).get('request_type', '')
                if req_type:
                    # Handle multiple request types
                    service_desc += f" - {req_type}"
            elif service_type == 'Jewelry':
                material = data.get('jewelry_details', {}).get('material', '')
                size = data.get('jewelry_details', {}).get('size', '')
                jewelry_type = data.get('jewelry_details', {}).get('jewelry_type', '')
                
                if material:
                    # Count materials (comma-separated)
                    material_count = len(material.split(','))
                    service_desc += f" - {material_count} material(s)"
                if size:
                    service_desc += f", {size}"
                if jewelry_type:
                    # Count jewelry types
                    jewelry_count = len(jewelry_type.split(','))
                    service_desc += f" ({jewelry_count} piece(s))"
            
            # print(f"Tracking: {service_desc}")
            
            # TODO: Add tracking save if needed
            # self.api_client.save_tracking(sample_id, user_id, user_id, service_desc)
            
            # print("Tracking information saved successfully")
            
            return True
            
        except Exception as e:
            print(f"Error in _save_to_database: {e}")
            QMessageBox.critical(
                self.view, 
                "Error", 
                f"เกิดข้อผิดพลาดในการบันทึกข้อมูล\n"
            )
            return False

    # ==================== Navigation Methods ====================
    
    def cancel_and_go_back(self):
        """
        Cancel current operation and return to previous page
        Shows confirmation if there's unsaved data
        """
        # Check if form has data
        if self._has_unsaved_data():
            reply = QMessageBox.question(
                self.view,
                'ยืนยันการยกเลิก',
                'มีข้อมูลที่ยังไม่ได้บันทึก\n'
                'คุณต้องการยกเลิกและออกจากหน้านี้หรือไม่?\n\n',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                return
        
        # Clear the form
        self.view.clear_page()
        
        # Navigate back to specimen page
        self.go_back()

    def go_back(self):
        """Navigate back to specimen page"""
        try:
            if hasattr(self.main_controller, 'specimen_widget'):
                self.main_controller.ui.stackedWidget.setCurrentWidget(
                    self.main_controller.specimen_widget
                )
                # print("Navigated back to specimen page")
            else:
                print("Warning: Specimen widget not found")
                QMessageBox.warning(
                    self.view,
                    "Warning",
                    "ไม่สามารถกลับไปหน้าตัวอย่างได้"
                )
        except Exception as e:
            print(f"Error navigating back: {e}")
            QMessageBox.critical(
                self.view,
                "Error",
                f"เกิดข้อผิดพลาดในการเปลี่ยนหน้า\n{str(e)}"
            )
    
    def go_back_to_new_work(self):
        """
        Navigate back to New Work page and refresh data
        This is called after successful save
        """
        try:
            if hasattr(self.main_controller, 'add_work_widget'):
                # Switch to new work page
                self.main_controller.ui.stackedWidget.setCurrentWidget(
                    self.main_controller.add_work_widget
                )
                
                # print("Navigated to new work page")
                
                # Refresh tree widget data to show updated status
                if (hasattr(self.main_controller, 'new_work_controller') and 
                    self.main_controller.new_work_controller):
                    
                    self.main_controller.new_work_controller.update_treewidget_data()
                    # print("Tree widget data refreshed")
                
                # Emit signal
                self.navigation_requested.emit("new_work")
                
            else:
                # print("Warning: Cannot navigate back to new work page")
                # print("Falling back to specimen page")
                self.go_back()
                
        except Exception as e:
            print(f"Error navigating to new work page: {e}")
            # Fallback to specimen page
            self.go_back()

    # ==================== Utility Methods ====================
    
    def _has_unsaved_data(self):
        """
        Check if form has any unsaved data
        
        Returns:
            bool: True if there's unsaved data
        """
        try:
            data = self.view.get_data()
            
            # If any detail section exists (not None), there's data
            if data.get('waste_details'):
                return True
            
            if data.get('cremation_details'):
                return True
            
            if data.get('jewelry_details'):
                return True
            
            return False
            
        except Exception as e:
            print(f"Error checking unsaved data: {e}")
            return False

    def load_existing_data(self, sample_id):
        """
        Load existing after death data for editing
        
        Args:
            sample_id (str): Sample ID to load data for
        """
        try:
            # TODO: When ready, add API call to fetch data
            # api_client = APIApp()
            # existing_data = api_client.get_after_death_data(sample_id)
            
            existing_data = None  # For now, no existing data
            
            if existing_data:
                # Populate form with existing data
                self.view.set_data(existing_data)
                self.current_sample_id = sample_id
                self.is_editing = True
                # print(f"Loaded existing data for sample: {sample_id}")
            else:
                print(f"No existing data found for sample: {sample_id}")
                
        except Exception as e:
            print(f"Error loading existing data: {e}")
            QMessageBox.warning(
                self.view,
                "Warning",
                f"ไม่สามารถโหลดข้อมูลเดิมได้\n{str(e)}"
            )

    def reset_controller_state(self):
        """Reset controller state for new entry"""
        self.current_sample_id = None
        self.is_editing = False
        self.view.clear_page()
        # print("Controller state reset")

    def get_current_service_type(self):
        """
        Get currently selected service type
        
        Returns:
            str: Service type name
        """
        if self.view.ui.rb_waste.isChecked():
            return 'Infectious Waste'
        elif self.view.ui.rb_cremation.isChecked():
            return 'Cremation'
        elif self.view.ui.rb_jewelry.isChecked():
            return 'Jewelry'
        return 'Unknown'

    def print_debug_info(self):
        # """Print debug information for troubleshooting"""
        # print("\n" + "=" * 60)
        # print("DEBUG INFO: After Death Controller")
        # print("=" * 60)
        # print(f"Current Sample ID: {self.current_sample_id}")
        # print(f"Is Editing: {self.is_editing}")
        # print(f"User ID: {self._get_user_id()}")
        # print(f"User Name: {self._get_user_name()}")
        # print(f"Service Type: {self.get_current_service_type()}")
        # print(f"Has Unsaved Data: {self._has_unsaved_data()}")
        # print("=" * 60 + "\n")
        pass