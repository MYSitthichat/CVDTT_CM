from View.view_edit_employee_frame import EditEmployeeWindow
from PySide6.QtCore import QObject, Qt, QBuffer, QIODevice, QTimer, QEvent, QPoint
from PySide6.QtWidgets import QMessageBox, QTreeWidgetItem, QFileDialog
from PySide6.QtGui import QPixmap, QMouseEvent
from API.client_app import APIApp
from datetime import datetime
import os
import base64


class EditEmployeeController(QObject):
    """Controller for Edit Employee Page - using API"""
    
    def __init__(self, view: EditEmployeeWindow, parent=None):
        super().__init__(parent)
        self.view = view
        self.view.controller = self  # Store reference for cleanup on close/hide
        self.api_app = APIApp()
        self.current_signature_path = None
        self.current_employee_id = None
        self.current_user_permission = None  # Store current user's permission level
        self.current_user_id = None  # Store current user's ID
        self.setup_ui()
        self.bind_employee_events()
        self.reset_page()  # Ensure clean state on initialization
    
    def setup_ui(self):
        """Setup UI elements"""
        # Load employee groups/positions into ComboBox
        self.load_employee_groups()
    
    def set_current_user(self, user_id):
        """Set current logged-in user and get their permission level"""
        self.current_user_id = user_id
        try:
            user_data = self.api_app.get_employee_by_id(user_id)
            if user_data:
                self.current_user_permission = user_data.get('group_id')
                # print(f"Current user permission level: {self.current_user_permission}")
        except Exception as e:
            print(f"Error getting current user permission: {e}")
            self.current_user_permission = 999  # Default to lowest permission
    
    def load_employee_groups(self):
        """Load employee groups from database into position ComboBox"""
        try:
            groups = self.api_app.get_employee_groups()
            self.view.employee_position_comboBox.clear()
            self.view.employee_position_comboBox.addItem("เลือกตำแหน่ง", None)  # Default option
            
            for group in groups:
                self.view.employee_position_comboBox.addItem(group['name'], group['id'])
                
        except Exception as e:
            print(f"Error loading employee groups: {e}")
    
    def bind_employee_events(self):
        """Bind all employee page button events"""
        # Search and navigation - NO .ui prefix!
        self.view.employee_search_pushButton.clicked.connect(self.search_employee)
        self.view.employee_new_pushButton.clicked.connect(self.create_new_employee)
        self.view.employee_edit_pushButton.clicked.connect(self.edit_employee_data)
        self.view.employee_delete_pushButton.clicked.connect(self.delete_employee_data)
        self.view.employee_back_pushButton.clicked.connect(self.back_to_home_from_employee)
        
        # Save button
        self.view.employee_save_pushButton.clicked.connect(self.save_employee_data)
        
        # TreeView selection
        self.view.employee_treeWidget.itemClicked.connect(self.on_employee_selected)
        
        # Real-time search as user types
        self.view.employee_search_lineEdit.textChanged.connect(self.on_search_text_changed)
    
    # ========== SEARCH FUNCTIONS ==========
    
    def on_search_text_changed(self, text):
        """Real-time search as user types"""
        search_text = text.strip()
        
        # Clear results if less than 2 characters
        if len(search_text) < 2:
            self.view.employee_treeWidget.clear()
            return
        
        # Perform search
        self.perform_employee_search(search_text)
    
    def search_employee(self):
        """Search employee by name or surname (when button is clicked)"""
        search_text = self.view.employee_search_lineEdit.text().strip()
        
        if len(search_text) < 2:
            return
        
        self.perform_employee_search(search_text)
    
    def perform_employee_search(self, search_text):
        """Perform employee search and display in treeview"""
        try:
            # Search in database via API
            employees = self.search_employee_in_database(search_text)
            
            # Check if API returned valid data
            if employees is None:
                self.view.employee_treeWidget.clear()
                return
            
            # Display results
            self.load_employee_search_results(employees)
                
        except Exception as e:
            print(f"Employee Search Error: {e}")
            self.view.employee_treeWidget.clear()
    
    def load_employee_search_results(self, employees):
        """Load search results into treeview - filter by permission
        Higher permission (lower group_id) can view lower permission (higher group_id)
        """
        self.view.employee_treeWidget.clear()
        
        if not employees:
            return
        
        # print(f"Search returned {len(employees)} employees")
        # print(f"Current user ID: {self.current_user_id}, Permission: {self.current_user_permission}")
        
        # Filter employees based on permission
        # Higher permission users (lower group_id) can see ALL employees including same level
        filtered_employees = []
        for emp in employees:
            emp_id = emp.get('id')
            emp_group_id = emp.get('group_id')
            emp_name = f"{emp.get('name', '')} {emp.get('surname', '')}"
            
            # print(f"Employee: {emp_name} (ID={emp_id}, group_id={emp_group_id})")
            
            # Skip if can't get permission
            if emp_group_id is None:
                # print(f"  -> Skipped: No group_id")
                continue
            
            # Show current user (can edit yourself)
            # Show employees with HIGHER group_id (lower permission)
            # Hide employees with SAME group_id who are not you (peers - cannot edit)
            # Hide employees with LOWER group_id (higher permission - cannot edit)
            
            is_self = (emp_id == self.current_user_id)
            has_lower_permission = (self.current_user_permission is not None and emp_group_id > self.current_user_permission)
            
            if is_self or has_lower_permission:
                filtered_employees.append(emp)
        
        # print(f"Filtered results: {len(filtered_employees)} employees")
        
        # Display filtered results
        for emp in filtered_employees:
            item = QTreeWidgetItem([
                str(emp.get('title', '')),
                str(emp.get('name', '')),
                str(emp.get('surname', ''))
            ])
            item.setData(0, Qt.UserRole, emp.get('id'))  # Store employee ID
            self.view.employee_treeWidget.addTopLevelItem(item)
        
        # Don't show any message when no results - for security
        # Lower permission users should not know that higher permission employees exist
        
        # Don't auto-select first item to prevent unwanted API calls
        # User must click to view employee details
    
    def on_employee_selected(self, item):
        """When employee is selected from search results - only store ID, don't show edit frame"""
        if not item:
            print("No item selected")
            return
            
        employee_id = item.data(0, Qt.UserRole)
        # print(f"Selected employee ID: {employee_id}")
        
        if not employee_id:
            print("No employee ID found in item data")
            return
            
        # Store selected employee ID but don't show edit frame yet
        self.current_employee_id = employee_id
    
    # ========== CRUD FUNCTIONS ==========
    
    def create_new_employee(self):
        """Create new employee"""
        self.current_employee_id = None
        self.clear_employee_fields()
        self.show_employee_edit_frame()
        # Enable password field for new employee
        self.view.employee_password_lineEdit.setEnabled(True)
        self.view.employee_password_lineEdit.setPlaceholderText("กรุณากรอกรหัสผ่าน")
        self.view.employee_password_lineEdit.clear()
        # Disable signature drawing until edit button is clicked
        self.view.signature_canvas.setEnabled(False)
    
    def edit_employee_data(self):
        """Edit selected employee"""
        selected_item = self.view.employee_treeWidget.currentItem()
        
        if not selected_item:
            QMessageBox.warning(self.view, "คำเตือน", "กรุณาเลือกพนักงานที่ต้องการแก้ไข!")
            return
        
        employee_id = selected_item.data(0, Qt.UserRole)
        if not employee_id:
            return
        
        # Check permission before allowing edit
        if not self.check_permission_to_edit(employee_id):
            QMessageBox.warning(
                self.view, 
                "ไม่มีสิทธิ์", 
                "คุณไม่มีสิทธิ์แก้ไขข้อมูลพนักงานคนนี้!\n\nเฉพาะผู้ที่มีตำแหน่งสูงกว่าเท่านั้นที่สามารถแก้ไขได้"
            )
            return
        
        # Load employee data and show edit frame
        self.current_employee_id = employee_id
        employee_data = self.get_employee_by_id(employee_id)
        
        if employee_data:
            self.populate_employee_fields(employee_data)
            self.show_employee_edit_frame()
            # Disable password field when viewing existing employee
            self.view.employee_password_lineEdit.setEnabled(False)
            self.view.employee_password_lineEdit.setPlaceholderText("(ไม่แสดงรหัสผ่าน)")
            # Disable signature drawing until edit button is clicked
            self.view.signature_canvas.setEnabled(False)
        else:
            QMessageBox.warning(self.view, "คำเตือน", "ไม่สามารถโหลดข้อมูลพนักงานได้!")
    
    def delete_employee_data(self):
        """Delete selected employee"""
        selected_item = self.view.employee_treeWidget.currentItem()
        
        if not selected_item:
            QMessageBox.warning(self.view, "คำเตือน", "กรุณาเลือกพนักงานที่ต้องการลบ!")
            return
        
        employee_id = selected_item.data(0, Qt.UserRole)
        if not employee_id:
            return
        
        # Check permission before allowing delete
        if not self.check_permission_to_edit(employee_id):
            QMessageBox.warning(
                self.view, 
                "ไม่มีสิทธิ์", 
                "คุณไม่มีสิทธิ์ลบข้อมูลพนักงานคนนี้!\n\nเฉพาะผู้ที่มีตำแหน่งสูงกว่าเท่านั้นที่สามารถลบได้"
            )
            return
            
        employee_name = f"{selected_item.text(1)} {selected_item.text(2)}"
        
        # Confirm deletion
        reply = QMessageBox.question(
            self.view, 
            "ยืนยันการลบ",
            f"คุณแน่ใจหรือไม่ว่าต้องการลบพนักงาน '{employee_name}'?\n\nการกระทำนี้ไม่สามารถย้อนกลับได้!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                result = self.delete_employee_from_database(employee_id)
                
                if result:
                    QMessageBox.information(self.view, "สำเร็จ", "ลบข้อมูลพนักงานสำเร็จ!")
                    self.search_employee()  # Refresh search results
                    self.hide_employee_edit_frame()
                    self.current_employee_id = None
                else:
                    QMessageBox.critical(self.view, "ข้อผิดพลาด", "ไม่สามารถลบข้อมูลได้!")
                    
            except Exception as e:
                QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
    
    def save_employee_data(self):
        """Save employee data (create or update)"""
        try:
            # Get data from form
            data = self.get_employee_data()
            
            # Validate required fields
            if not data['name'] or not data['surname']:
                QMessageBox.warning(self.view, "คำเตือน", "กรุณากรอกชื่อและนามสกุล!")
                return
            
            if not data['username']:
                QMessageBox.warning(self.view, "คำเตือน", "กรุณากรอก Username!")
                return
            
            if not data['email']:
                QMessageBox.warning(self.view, "คำเตือน", "กรุณากรอกอีเมล!")
                return
            
            # Validate email format (basic)
            if '@' not in data['email']:
                QMessageBox.warning(self.view, "คำเตือน", "รูปแบบอีเมลไม่ถูกต้อง!")
                return
            
            # Save signature image if drawn
            if data.get('signature_image'):
                signature_base64 = self.pixmap_to_base64(data['signature_image'])
                if signature_base64:
                    data['signature_base64'] = signature_base64
                else:
                    data['signature_base64'] = None
            else:
                data['signature_base64'] = None
            
            # Check if new employee or editing
            if self.current_employee_id:
                # Check permission for editing existing employee
                if not self.check_permission_to_edit(self.current_employee_id):
                    QMessageBox.warning(
                        self.view, 
                        "ไม่มีสิทธิ์", 
                        "คุณไม่มีสิทธิ์แก้ไขข้อมูลพนักงานคนนี้!"
                    )
                    return
                
                # Also check if the NEW permission level is valid for current user
                new_employee_group_id = data.get('group_id')
                if new_employee_group_id is not None and self.current_user_permission is not None:
                    if new_employee_group_id <= self.current_user_permission:
                        QMessageBox.warning(
                            self.view,
                            "ไม่มีสิทธิ์",
                            "ระบบไม่อนุญาติ"
                        )
                        return
                
                # Update existing employee (no password field)
                result = self.update_employee_in_database(self.current_employee_id, data)
                message = "แก้ไขข้อมูลพนักงานสำเร็จ!"
            else:
                # Create new employee
                if not data['password']:
                    QMessageBox.warning(self.view, "คำเตือน", "กรุณากรอกรหัสผ่าน!")
                    return
                
                if len(data['password']) < 6:
                    QMessageBox.warning(self.view, "คำเตือน", "รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร!")
                    return
                
                # Check permission: User can only create employees with LOWER permission (higher group_id)
                new_employee_group_id = data.get('group_id')
                if new_employee_group_id is not None and self.current_user_permission is not None:
                    if new_employee_group_id <= self.current_user_permission:
                        QMessageBox.warning(
                            self.view,
                            "ไม่มีสิทธิ์",
                            "ระบบไม่อนุญาติ"
                        )
                        return
                
                result = self.create_employee_in_database(data)
                message = "เพิ่มพนักงานใหม่สำเร็จ!"
            
            if result:
                QMessageBox.information(self.view, "สำเร็จ", message)
                self.clear_employee_fields()
                self.hide_employee_edit_frame()
                self.current_employee_id = None
                self.search_employee()  # Refresh search
            else:
                QMessageBox.critical(self.view, "ข้อผิดพลาด", "ไม่สามารถบันทึกข้อมูลได้!\n\nUsername อาจซ้ำหรือเซิร์ฟเวอร์ไม่พร้อมใช้งาน")
                
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
    
    # ========== DATA FUNCTIONS ==========
    
    def get_employee_data(self):
        """Get employee form data"""
        group_id = self.view.employee_position_comboBox.currentData()
        
        data = {
            'title': self.view.employee_title_lineEdit.text().strip(),
            'name': self.view.employee_name_lineEdit.text().strip(),
            'surname': self.view.employee_surname_lineEdit.text().strip(),
            'email': self.view.employee_email_lineEdit.text().strip(),
            'username': self.view.employee_username_lineEdit.text().strip(),
            'group_id': group_id if group_id else None,
        }
        
        # Get signature image from canvas (not file path)
        signature_image = self.view.get_signature_image()
        if signature_image and not signature_image.isNull():
            data['signature_image'] = signature_image
        else:
            data['signature_image'] = None
        
        # Only include password for new employees
        if self.view.employee_password_lineEdit.isEnabled():
            data['password'] = self.view.employee_password_lineEdit.text()
        
        return data
    
    def populate_employee_fields(self, employee_data):
        """Populate form fields with employee data"""
        if not employee_data:
            return
            
        self.view.employee_title_lineEdit.setText(str(employee_data.get('title', '')))
        self.view.employee_name_lineEdit.setText(str(employee_data.get('name', '')))
        self.view.employee_surname_lineEdit.setText(str(employee_data.get('surname', '')))
        self.view.employee_email_lineEdit.setText(str(employee_data.get('email', '')))
        self.view.employee_username_lineEdit.setText(str(employee_data.get('username', '')))
        
        # Set position in ComboBox by group_id
        group_id = employee_data.get('group_id')
        if group_id:
            index = self.view.employee_position_comboBox.findData(group_id)
            if index >= 0:
                self.view.employee_position_comboBox.setCurrentIndex(index)
        
        # Load signature from API
        username = employee_data.get('username')
        if username:
            try:
                signature_base64 = self.api_app.get_signature(username)
                if signature_base64:
                    # Decode base64 to QPixmap
                    image_data = base64.b64decode(signature_base64)
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)
                    if not pixmap.isNull():
                        self.view.set_signature_image(pixmap)
                        # print(f"Signature loaded from API for user: {username}")
                    else:
                        self.view.clear_signature()
                else:
                    self.view.clear_signature()
            except Exception as e:
                print(f"Error loading signature from API: {e}")
                self.view.clear_signature()
        else:
            self.view.clear_signature()
    
    def clear_employee_fields(self):
        """Clear all employee form fields"""
        self.view.employee_title_lineEdit.clear()
        self.view.employee_name_lineEdit.clear()
        self.view.employee_surname_lineEdit.clear()
        self.view.employee_email_lineEdit.clear()
        self.view.employee_username_lineEdit.clear()
        self.view.employee_password_lineEdit.clear()
        self.view.employee_position_comboBox.setCurrentIndex(0)  # Reset to first item
        self.view.clear_signature()
        # Disable signature drawing
        self.view.signature_canvas.setEnabled(False)
    
    # ========== UI VISIBILITY FUNCTIONS ==========
    
    def show_employee_edit_frame(self):
        """Show employee edit frame"""
        self.view.frame_2.setVisible(True)
    
    def hide_employee_edit_frame(self):
        """Hide employee edit frame"""
        self.view.frame_2.setVisible(False)
    
    def reset_page(self):
        """Reset page to clean state - called when window opens or closes"""
        # Clear all form fields
        self.clear_employee_fields()
        
        # Hide edit frame
        self.hide_employee_edit_frame()
        
        # Clear search results and search text
        self.view.employee_treeWidget.clear()
        self.view.employee_search_lineEdit.clear()
        
        # Reset current employee selection
        self.current_employee_id = None
    
    def cleanup_on_close(self):
        """Cleanup method called when window is closed/hidden - can be called externally"""
        self.reset_page()
    
    def back_to_home_from_employee(self):
        """Go back to new work page (รับงานใหม่)"""
        # Reset page to clean state
        self.reset_page()
        
        # Navigate back to new work page and trigger button click BEFORE closing window
        if self.parent():
            main_controller = self.parent()
            if hasattr(main_controller, 'main_window'):
                # Trigger the button click to properly update button highlight
                if hasattr(main_controller.main_window.ui, 'new_work_pushButton'):
                    main_controller.main_window.ui.new_work_pushButton.click()
                else:
                    # Fallback to direct method call
                    main_controller.main_window.show_add_work_page()
        
        # Close edit employee window AFTER button click (this will return to main window)
        self.view.close()
    
    # ========== PERMISSION FUNCTIONS ==========
    
    def check_permission_to_edit(self, target_employee_id):
        """Check if current user has permission to edit/delete target employee
        Rules:
        - CAN edit yourself
        - CAN edit lower permission (higher group_id)
        - CANNOT edit same permission peers (same group_id, different user)
        - CANNOT edit higher permission (lower group_id)
        """
        # If no permission level set, deny access
        if self.current_user_permission is None:
            return False
        
        # Allow editing yourself
        if target_employee_id == self.current_user_id:
            return True
        
        try:
            # Get target employee's permission level
            target_employee = self.api_app.get_employee_by_id(target_employee_id)
            if not target_employee:
                return False
            
            target_permission = target_employee.get('group_id')
            if target_permission is None:
                return False
            
            # Can only edit employees with HIGHER group_id (lower authority)
            # Cannot edit same or lower group_id (peers or superiors)
            can_edit = self.current_user_permission < target_permission

            return can_edit
            
        except Exception as e:
            print(f"Error checking permission: {e}")
            return False
    
    # ========== SIGNATURE FUNCTIONS ==========
    
    def pixmap_to_base64(self, pixmap):
        """Convert QPixmap to base64 string"""
        try:
            byte_array = QBuffer()
            byte_array.open(QIODevice.WriteOnly)
            pixmap.save(byte_array, "PNG")
            image_data = byte_array.data()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            return base64_data
        except Exception as e:
            print(f"Error converting pixmap to base64: {e}")
            return None
    
    # ========== DATABASE FUNCTIONS - USING API ==========
    
    def search_employee_in_database(self, search_text):
        """Search employee by name or surname using API"""
        try:
            employees = self.api_app.search_employee(search_text)
            if employees is None:
                return None
            return employees if isinstance(employees, list) else []
        except Exception as e:
            print(f"Error searching employee: {e}")
            return None
    
    def get_employee_by_id(self, employee_id):
        """Get employee by ID using API"""
        try:
            employee_data = self.api_app.get_employee_by_id(employee_id)
            return employee_data
        except Exception as e:
            print(f"Error getting employee: {e}")
            return None
    
    def create_employee_in_database(self, data):
        """Create new employee using API with version tracking"""
        try:
            employee_data = {
                "title": data.get('title', ''),
                "name": data.get('name', ''),
                "surname": data.get('surname', ''),
                "email": data.get('email', ''),
                "username": data.get('username', ''),
                "password": data.get('password', ''),
                "group_id": data.get('group_id'),
                "signature_base64": data.get('signature_base64'),
                "status": 1,  # New employee is active
                "updater": self.current_user_permission  # Track who created this
            }
            
            result = self.api_app.create_employee(employee_data)
            return result is not None and result.get('status') == 'success'
            
        except Exception as e:
            print(f"Error creating employee: {e}")
            return False
    
    def update_employee_in_database(self, employee_id, data):
        """Update employee data using API with version history
        This will:
        1. Set old record status=0 with updater tracking
        2. Insert new record with status=1 and updated data
        """
        try:
            employee_data = {
                "title": data.get('title', ''),
                "name": data.get('name', ''),
                "surname": data.get('surname', ''),
                "email": data.get('email', ''),
                "username": data.get('username', ''),
                "group_id": data.get('group_id'),
                "signature_base64": data.get('signature_base64'),
                "status": 1,  # New version is active
                "updater": self.current_user_permission  # Track who edited this
            }
            
            # print(f"Updating employee {employee_id} with data: {employee_data}")
            result = self.api_app.update_employee(employee_id, employee_data)
            # print(f"Update result: {result}")
            return result is not None and result.get('status') == 'success'
            
        except Exception as e:
            print(f"Error updating employee: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def delete_employee_from_database(self, employee_id):
        """Soft delete employee using API
        Sets status=0 and tracks who deleted it via updater field
        """
        try:
            # Send updater info for soft delete tracking
            delete_data = {
                "updater": self.current_user_permission  # Track who deleted this
            }
            result = self.api_app.delete_employee(employee_id, delete_data)
            return result is not None and result.get('status') == 'success'
        except Exception as e:
            print(f"Error deleting employee: {e}")
            return False