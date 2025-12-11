from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox
from SERVICES_REGISTER.after_death_service import AfterDeathService
from SERVICES_REGISTER.lab_service import LabService


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
        self.after_death_service = AfterDeathService()
        self.api_client = LabService()  # For lab_order and tracking
        
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
        
        # Checkbox events for dynamic UI updates (changed from radio buttons)
        self.view.ui.rb_waste.toggled.connect(self._on_service_type_changed)
        self.view.ui.rb_cremation.toggled.connect(self._on_service_type_changed)
        self.view.ui.rb_jewelrya.toggled.connect(self._on_service_type_changed)

    def _setup_ui_state(self):
        """Setup initial UI state"""
        # Don't set default checked - user can select multiple services
        # All checkboxes start unchecked
        
        # Enable save button (user can save any combination)
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
        Extract Sample ID from specimen_controller (เหมือน parasite_controller)
        Note: main_controller here is actually main_window
        
        Returns:
            str: Sample ID or None if not found
        """
        try:
            # Get sample_id from specimen_controller (แบบเดียวกับ parasite)
            # Note: self.main_controller is actually main_window
            sample_id = None
            
            # Try getting from main_window.specimen_controller
            if hasattr(self.main_controller, 'specimen_controller'):
                specimen_ctrl = self.main_controller.specimen_controller
                if hasattr(specimen_ctrl, 'specimen_id') and specimen_ctrl.specimen_id:
                    sample_id = str(specimen_ctrl.specimen_id)
                    # print(f"[After Death] Found specimen_id: {sample_id}")
            
            if sample_id:
                self.current_sample_id = sample_id
                return sample_id
            
            print("[After Death] specimen_id not found in specimen_controller")
            return None
            
        except Exception as e:
            print(f"[After Death Controller] Error getting sample_id: {e}")
            return None

    def _get_user_id(self):
        """
        Get current logged-in user ID from main_controller (เหมือน parasite_controller)
        Note: main_controller here is actually main_window
        
        Returns:
            int: User ID or None if not logged in
        """
        try:
            # Get user_id from main controller (แบบเดียวกับ parasite)
            # Note: self.main_controller is actually main_window
            user_id = None
            
            # Try getting from main_window.main_controller
            if hasattr(self.main_controller, 'main_controller'):
                main_ctrl = self.main_controller.main_controller
                if hasattr(main_ctrl, 'logged_in_user_id') and main_ctrl.logged_in_user_id:
                    user_id = main_ctrl.logged_in_user_id
                    # print(f"[After Death] Found user_id: {user_id}")
            
            if user_id:
                return user_id
                
            print("[After Death] user_id not found in main_controller")
            return None
            
        except (IndexError, TypeError, AttributeError) as e:
            print(f"[After Death Controller] Error getting user ID: {e}")
            return None

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

        # Validate based on service type (can be multiple)
        if 'Infectious Waste' in service_type:
            waste_details = data.get('waste_details')
            if not waste_details:  # No data filled
                QMessageBox.warning(
                    self.view, 
                    "Validation Error", 
                    "กรุณากรอกข้อมูลขยะติดเชื้อ"
                )
                return False
            if not self._validate_waste_data(waste_details):
                return False
            
        if 'Cremation' in service_type:
            cremation_details = data.get('cremation_details')
            if not cremation_details:  # No data filled
                QMessageBox.warning(
                    self.view, 
                    "Validation Error", 
                    "กรุณากรอกข้อมูลการฌาปนกิจ"
                )
                return False
            if not self._validate_cremation_data(cremation_details):
                return False
            
        if 'Jewelry' in service_type:
            jewelry_details = data.get('jewelry_details')
            if not jewelry_details:  # No data filled
                QMessageBox.warning(
                    self.view, 
                    "Validation Error", 
                    "กรุณากรอกข้อมูลเครื่องประดับ"
                )
                return False
            if not self._validate_jewelry_data(jewelry_details):
                return False

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
        materials = jewelry_data.get('materials', {})
        
        if not materials:
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
        # Step 1: Get Sample ID (แบบเดียวกับ parasite)
        sample_id = self._get_sample_id()
        if not sample_id:
            QMessageBox.warning(
                self.view,
                "ไม่พบหมายเลข Sample ID",
                "กรุณาบันทึกข้อมูล Specimen ในหน้าก่อนหน้านี้ก่อน\n"
                "แล้วจึงกลับมาเลือกบริการหลังความตาย"
            )
            return
        
        # Step 2: Get User ID (แบบเดียวกับ parasite)
        user_id = self._get_user_id()
        if not user_id:
            QMessageBox.warning(
                self.view, 
                "ไม่พบข้อมูลผู้ใช้", 
                "กรุณา Login ใหม่อีกครั้ง"
            )
            return
        
        user_name = self._get_user_name()
        
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
            # f"Sample ID: {self.current_sample_id}\n"
            # f"Service: {service_type}\n\n"
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
        Save data to database and track status (แบบเดียวกับ parasite_controller)
        
        Args:
            sample_id (str): Sample identifier
            data (dict): Form data
            user_id (int): Current user ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            service_type = data.get('service_type', 'Unknown')
            
            # Get room_id for after death service (แบบเดียวกับ parasite)
            room_id = "10"  # Default room_id for After Death Service
            if hasattr(self.main_controller, 'specimen_controller'):
                specimen_ctrl = self.main_controller.specimen_controller
                if hasattr(specimen_ctrl, 'room_mapping') and 'after_death' in specimen_ctrl.room_mapping:
                    room_id = specimen_ctrl.room_mapping['after_death']
            
            # Prepare data for after_death API (แบบเดียวกับ parasite)
            after_death_data = {
                "sample_id": sample_id,
                "service_type": service_type,
                "service_data": data,
                "updater": user_id
            }
            
            # Prepare data for lab order API (แบบเดียวกับ parasite)
            lab_order_data = {
                "sample_id": sample_id,
                "room_id": str(room_id),
                "comments": "",
                "state": "0",
                "status": "1",
                "updater": user_id
            }
            
            # Prepare first tracking entry (แบบเดียวกับ parasite)
            first_update_tracking_lab_order_data = {
                "sample_id": sample_id,
                "tracking_info": "รับงานเข้าระบบ",
                "receiver": str(user_id),
                "updater": str(user_id)
            }
            
            # Call APIs (แบบเดียวกับ parasite)
            save_after_death_result = self.after_death_service.save_after_death(
                sample_id=after_death_data["sample_id"],
                service_type=after_death_data["service_type"],
                service_data=after_death_data["service_data"],
                user_id=after_death_data["updater"]
            )
            insert_lab_order = self.api_client.add_new_lab_order(lab_order_data)
            first_update_tracking = self.api_client.update_tracking_lab_order(first_update_tracking_lab_order_data)
            
            # Check results (แบบเดียวกับ parasite)
            if (save_after_death_result and 
                insert_lab_order and 
                first_update_tracking and 
                first_update_tracking.get("status") == "success"):
                
                return True
            else:
                error_msg = "Unknown error"
                if save_after_death_result and isinstance(save_after_death_result, dict):
                    error_msg = save_after_death_result.get('detail', error_msg)
                
                QMessageBox.critical(
                    self.view,
                    "ข้อผิดพลาด",
                    f"บันทึกข้อมูลไม่สำเร็จ\n\n{error_msg}"
                )
                return False
            
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
        # Check if form has data
        if self._has_unsaved_data():
            reply = QMessageBox.question(
                self.view,
                "ยืนยันการยกเลิก",
                "คุณต้องการยกเลิกและล้างข้อมูลหรือไม่?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                QMessageBox.information(self.view, "ยกเลิก", "ยกเลิกการกรอกข้อมูลแล้ว")
                # Clear the form
                self.view.clear_page()
                # Navigate back to specimen page
                self.go_back()
                
            if reply == QMessageBox.No:
                return
        


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
        Get currently selected service types (can be multiple)
        
        Returns:
            str: Comma-separated service type names
        """
        types = []
        if self.view.ui.rb_waste.isChecked():
            types.append('Infectious Waste')
        if self.view.ui.rb_cremation.isChecked():
            types.append('Cremation')
        if self.view.ui.rb_jewelrya.isChecked():
            types.append('Jewelry')
        return ', '.join(types) if types else 'Unknown'

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