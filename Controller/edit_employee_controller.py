from View.view_edit_employee_frame import EditEmployeeWindow
from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QMessageBox, QTreeWidgetItem, QFileDialog
from PySide6.QtGui import QPixmap
import pyodbc
import hashlib
from datetime import datetime


class EditEmployeeController(QObject):
    """Controller for Edit Employee Page - mimicking lab_manager structure"""
    
    def __init__(self, view: EditEmployeeWindow, parent=None):
        super().__init__(parent)
        self.view = view
        self.current_signature_path = None
        self.current_employee_id = None
        self.bind_employee_events()
        self.hide_employee_edit_frame()  # Hide edit frame initially
    
    def bind_employee_events(self):
        """Bind all employee page button events"""
        # Search and navigation - CORRECTED NAMES
        self.view.ui.employee_search_pushButton.clicked.connect(self.search_employee)
        self.view.ui.employee_new_pushButton.clicked.connect(self.create_new_employee)
        self.view.ui.employee_edit_pushButton.clicked.connect(self.edit_employee_data)
        self.view.ui.employee_delete_pushButton.clicked.connect(self.delete_employee_data)
        self.view.ui.employee_back_pushButton.clicked.connect(self.back_to_home_from_employee)
        
        # Save and signature - CORRECTED NAMES
        self.view.ui.employee_save_pushButton.clicked.connect(self.save_employee_data)
        self.view.ui.employee_edit_signature_pushButton.clicked.connect(self.edit_employee_signature)
        
        # TreeView selection - CORRECTED NAME
        self.view.ui.employee_treeWidget.itemClicked.connect(self.on_employee_selected)
    
    # ========== SEARCH FUNCTIONS ==========
    
    def search_employee(self):
        """Search employee by name or surname"""
        search_text = self.view.ui.employee_search_lineEdit.text().strip()  # CORRECTED
        
        if not search_text:
            QMessageBox.warning(self.view, "คำเตือน", "กรุณากรอกชื่อหรือนามสกุลที่ต้องการค้นหา!")
            return
        
        try:
            # Search in database
            employees = self.search_employee_in_database(search_text)
            
            # Display results
            self.load_employee_search_results(employees)
            
            if not employees:
                QMessageBox.information(self.view, "ผลการค้นหา", "ไม่พบข้อมูลพนักงาน!")
                
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการค้นหา: {str(e)}")
    
    def load_employee_search_results(self, employees):
        """Load search results into treeview"""
        self.view.ui.employee_treeWidget.clear()  # CORRECTED
        
        for emp in employees:
            item = QTreeWidgetItem([
                emp.get('title', ''),
                emp.get('name', ''),
                emp.get('surname', '')
            ])
            item.setData(0, Qt.UserRole, emp['id'])  # Store employee ID
            self.view.ui.employee_treeWidget.addTopLevelItem(item)  # CORRECTED
    
    def on_employee_selected(self, item):
        """When employee is selected from search results"""
        employee_id = item.data(0, Qt.UserRole)
        self.current_employee_id = employee_id
        
        employee_data = self.get_employee_by_id(employee_id)
        
        if employee_data:
            self.populate_employee_fields(employee_data)
            self.show_employee_edit_frame()
    
    # ========== CRUD FUNCTIONS ==========
    
    def create_new_employee(self):
        """Create new employee"""
        self.current_employee_id = None
        self.clear_employee_fields()
        self.show_employee_edit_frame()
        self.view.ui.employee_password_lineEdit.setEnabled(True)  # CORRECTED
        self.view.ui.employee_password_lineEdit.setPlaceholderText("กรุณากรอกรหัสผ่าน")  # CORRECTED
    
    def edit_employee_data(self):
        """Edit selected employee"""
        selected_item = self.view.ui.employee_treeWidget.currentItem()  # CORRECTED
        
        if not selected_item:
            QMessageBox.warning(self.view, "คำเตือน", "กรุณาเลือกพนักงานที่ต้องการแก้ไข!")
            return
        
        self.on_employee_selected(selected_item)
        self.view.ui.employee_password_lineEdit.setEnabled(False)  # CORRECTED
        self.view.ui.employee_password_lineEdit.setPlaceholderText("(ไม่แสดงรหัสผ่าน)")  # CORRECTED
    
    def delete_employee_data(self):
        """Delete selected employee"""
        selected_item = self.view.ui.employee_treeWidget.currentItem()  # CORRECTED
        
        if not selected_item:
            QMessageBox.warning(self.view, "คำเตือน", "กรุณาเลือกพนักงานที่ต้องการลบ!")
            return
        
        employee_id = selected_item.data(0, Qt.UserRole)
        employee_name = f"{selected_item.text(1)} {selected_item.text(2)}"
        
        # Confirm deletion
        reply = QMessageBox.question(
            self.view, 
            "ยืนยันการลบ",
            f"คุณแน่ใจหรือไม่ว่าต้องการลบพนักงาน '{employee_name}'?",
            QMessageBox.Yes | QMessageBox.No
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
            
            # Check if new employee or editing
            if self.current_employee_id:
                # Update existing employee
                result = self.update_employee_in_database(self.current_employee_id, data)
                message = "แก้ไขข้อมูลพนักงานสำเร็จ!"
            else:
                # Create new employee
                if not data['password']:
                    QMessageBox.warning(self.view, "คำเตือน", "กรุณากรอกรหัสผ่าน!")
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
                QMessageBox.critical(self.view, "ข้อผิดพลาด", "ไม่สามารถบันทึกข้อมูลได้!")
                
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
    
    # ========== DATA FUNCTIONS ==========
    
    def get_employee_data(self):
        """Get employee form data"""
        return {
            'title': self.view.ui.employee_title_lineEdit.text(),  # CORRECTED
            'name': self.view.ui.employee_name_lineEdit.text(),  # CORRECTED
            'surname': self.view.ui.employee_surname_lineEdit.text(),  # CORRECTED
            'email': self.view.ui.employee_email_lineEdit.text(),  # CORRECTED
            'username': self.view.ui.employee_username_lineEdit.text(),  # CORRECTED
            'password': self.view.ui.employee_password_lineEdit.text(),  # CORRECTED
            'position': self.view.ui.employee_position_comboBox.currentText(),  # CORRECTED
            'signature': self.current_signature_path
        }
    
    def populate_employee_fields(self, employee_data):
        """Populate form fields with employee data"""
        self.view.ui.employee_title_lineEdit.setText(employee_data.get('title', ''))  # CORRECTED
        self.view.ui.employee_name_lineEdit.setText(employee_data.get('name', ''))  # CORRECTED
        self.view.ui.employee_surname_lineEdit.setText(employee_data.get('surname', ''))  # CORRECTED
        self.view.ui.employee_email_lineEdit.setText(employee_data.get('email', ''))  # CORRECTED
        self.view.ui.employee_username_lineEdit.setText(employee_data.get('username', ''))  # CORRECTED
        self.view.ui.employee_position_comboBox.setCurrentText(employee_data.get('position', ''))  # CORRECTED
        
        # Load signature if exists
        signature_path = employee_data.get('signature')
        if signature_path:
            self.current_signature_path = signature_path
            self.load_employee_signature(signature_path)
    
    def clear_employee_fields(self):
        """Clear all employee form fields"""
        self.view.ui.employee_title_lineEdit.clear()  # CORRECTED
        self.view.ui.employee_name_lineEdit.clear()  # CORRECTED
        self.view.ui.employee_surname_lineEdit.clear()  # CORRECTED
        self.view.ui.employee_email_lineEdit.clear()  # CORRECTED
        self.view.ui.employee_username_lineEdit.clear()  # CORRECTED
        self.view.ui.employee_password_lineEdit.clear()  # CORRECTED
        self.view.ui.employee_position_comboBox.setCurrentIndex(0)  # CORRECTED
        self.current_signature_path = None
    
    # ========== UI VISIBILITY FUNCTIONS ==========
    
    def show_employee_edit_frame(self):
        """Show employee edit frame"""
        self.view.ui.frame_2.setVisible(True)  # CORRECTED - frame_2 is the edit frame
    
    def hide_employee_edit_frame(self):
        """Hide employee edit frame"""
        self.view.ui.frame_2.setVisible(False)  # CORRECTED - frame_2 is the edit frame
    
    def back_to_home_from_employee(self):
        """Go back to home page"""
        # Emit signal or call parent navigation
        print("Navigate back to home")
        # If you have a parent window with stackedWidget:
        # self.parent().stackedWidget.setCurrentIndex(0)
    
    # ========== SIGNATURE FUNCTIONS ==========
    
    def edit_employee_signature(self):
        """Edit employee signature - open file dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "เลือกไฟล์ลายเซ็น",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            self.current_signature_path = file_path
            self.load_employee_signature(file_path)
    
    def load_employee_signature(self, signature_path):
        """Load and display employee signature"""
        try:
            pixmap = QPixmap(signature_path)
            if not pixmap.isNull():
                # Scale to fit signature frame
                scaled_pixmap = pixmap.scaled(
                    self.view.ui.employee_signature_frame.size(),  # CORRECTED
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                
                # Note: You need to add a QLabel inside employee_signature_frame in Qt Designer
                # to display the image. For now, just storing the path.
                
                print(f"Signature loaded: {signature_path}")
        except Exception as e:
            print(f"Error loading signature: {e}")
    
    # ========== DATABASE FUNCTIONS ==========
    
    def search_employee_in_database(self, search_text):
        """Search employee by name or surname in database"""
        try:
            connection = self.connect_database()
            cursor = connection.cursor()
            
            sql = """
            SELECT id, title, name, surname, email, username, position, signature
            FROM employees
            WHERE name LIKE ? OR surname LIKE ?
            ORDER BY name
            """
            
            cursor.execute(sql, (f'%{search_text}%', f'%{search_text}%'))
            rows = cursor.fetchall()
            
            employees = []
            for row in rows:
                employees.append({
                    'id': row[0],
                    'title': row[1],
                    'name': row[2],
                    'surname': row[3],
                    'email': row[4],
                    'username': row[5],
                    'position': row[6],
                    'signature': row[7]
                })
            
            cursor.close()
            connection.close()
            
            return employees
            
        except Exception as e:
            print(f"Error searching employee: {e}")
            return []
    
    def get_employee_by_id(self, employee_id):
        """Get employee by ID from database"""
        try:
            connection = self.connect_database()
            cursor = connection.cursor()
            
            sql = "SELECT * FROM employees WHERE id = ?"
            cursor.execute(sql, (employee_id,))
            row = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if row:
                return {
                    'id': row[0],
                    'title': row[1],
                    'name': row[2],
                    'surname': row[3],
                    'email': row[4],
                    'username': row[5],
                    'password': row[6],
                    'position': row[7],
                    'signature': row[8]
                }
            return None
            
        except Exception as e:
            print(f"Error getting employee: {e}")
            return None
    
    def create_employee_in_database(self, data):
        """Create new employee in database"""
        try:
            connection = self.connect_database()
            cursor = connection.cursor()
            
            # Hash password
            hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
            
            sql = """
            INSERT INTO employees 
            (title, name, surname, email, username, password, position, signature, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(sql, (
                data['title'],
                data['name'],
                data['surname'],
                data['email'],
                data['username'],
                hashed_password,
                data['position'],
                data.get('signature'),
                datetime.now()
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
            
        except Exception as e:
            print(f"Error creating employee: {e}")
            return False
    
    def update_employee_in_database(self, employee_id, data):
        """Update employee data in database"""
        try:
            connection = self.connect_database()
            cursor = connection.cursor()
            
            sql = """
            UPDATE employees 
            SET title=?, name=?, surname=?, email=?, username=?, position=?, signature=?, updated_date=?
            WHERE id=?
            """
            
            cursor.execute(sql, (
                data['title'],
                data['name'],
                data['surname'],
                data['email'],
                data['username'],
                data['position'],
                data.get('signature'),
                datetime.now(),
                employee_id
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
            
        except Exception as e:
            print(f"Error updating employee: {e}")
            return False
    
    def delete_employee_from_database(self, employee_id):
        """Delete employee from database"""
        try:
            connection = self.connect_database()
            cursor = connection.cursor()
            
            sql = "DELETE FROM employees WHERE id = ?"
            cursor.execute(sql, (employee_id,))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
            
        except Exception as e:
            print(f"Error deleting employee: {e}")
            return False
    
    def connect_database(self):
        """Connect to SQL Server database"""
        # Replace with your actual database credentials
        connection_string = (
            "DRIVER={SQL Server};"
            "SERVER=your_server_name;"
            "DATABASE=your_database_name;"
            "UID=your_username;"
            "PWD=your_password;"
        )
        return pyodbc.connect(connection_string)