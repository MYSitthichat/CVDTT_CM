from View.view_parasite_frame import parasiteFrameView
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox
import pyodbc
from datetime import datetime


class ParasiteController(QObject):
    """Controller for Parasite Biology Page - mimicking lab_manager structure"""
    
    def __init__(self, view: parasiteFrameView, parent=None):
        super().__init__(parent)
        self.view = view
        self.main_window = parent  # Store reference to main window
        # Test prices (adjust as needed) - CORRECTED based on UI labels
        self.test_prices = {
            'PCV': 50,
            'Floatation': 50,
            'Parasite_in_meat': 300,
            'Parasite_identification': 100,
            'Stained_Woo_PCV': 150,
            'Centrifugal_dog_cat': 150,
            'Floatation_centrifugal': 200,
            'Floatation_dog_cat': 100,
            'Stained_blood_smear': 100,
            'Sedimentation': 50,
            'Woo': 50,
            'Mc_Master': 100
        }
        self.bind_parasite_events()
    
    def bind_parasite_events(self):
        """Bind all parasite page events - CORRECTED WIDGET NAMES"""
        # Bind all test checkboxes to auto-calculate summary
        self.view.ui.parasite_PCV_checkBox.stateChanged.connect(self.calculate_summary)
        self.view.ui.parasite_floatation_checkBox.stateChanged.connect(self.calculate_summary)
        self.view.ui.parasite_parasite_in_meat_checkBox.stateChanged.connect(self.calculate_summary)
        self.view.ui.parasite_parasite_identification_checkBox.stateChanged.connect(self.calculate_summary)
        self.view.ui.parasite_stained_Woo_PCV_checkBox.stateChanged.connect(self.calculate_summary)
        self.view.ui.parasite_centrifugal_dog_cat_checkBox.stateChanged.connect(self.calculate_summary)
        self.view.ui.parasite_floatation_centrifugal_checkBox.stateChanged.connect(self.calculate_summary)
        self.view.ui.parasite_floatation_dog_cat_checkBox.stateChanged.connect(self.calculate_summary)
        self.view.ui.parasite_stained_blood_smear_checkBox.stateChanged.connect(self.calculate_summary)
        self.view.ui.parasite_sedimentation_checkBox.stateChanged.connect(self.calculate_summary)
        self.view.ui.parasite_Woo_checkBox.stateChanged.connect(self.calculate_summary)
        self.view.ui.parasite_mc_master_egg_count_checkBox.stateChanged.connect(self.calculate_summary)
        
        # Bind buttons (pushButtons not labels) - CORRECTED NAMES
        self.view.ui.parasite_save_pushButton.clicked.connect(self.save_parasite_data)
        self.view.ui.parasite_cancel_pushButton.clicked.connect(self.cancel_parasite)
    
    def calculate_summary(self):
        """Calculate total number of tests and total cost - auto updates when checkbox changes"""
        total_tests = 0
        total_cost = 0.0
        
        # Check each test and add to totals - CORRECTED WIDGET NAMES
        if self.view.ui.parasite_PCV_checkBox.isChecked():
            total_tests += 1
            total_cost += self.test_prices['PCV']
        
        if self.view.ui.parasite_floatation_checkBox.isChecked():
            total_tests += 1
            total_cost += self.test_prices['Floatation']
        
        if self.view.ui.parasite_parasite_in_meat_checkBox.isChecked():
            total_tests += 1
            total_cost += self.test_prices['Parasite_in_meat']
        
        if self.view.ui.parasite_parasite_identification_checkBox.isChecked():
            total_tests += 1
            total_cost += self.test_prices['Parasite_identification']
        
        if self.view.ui.parasite_stained_Woo_PCV_checkBox.isChecked():
            total_tests += 1
            total_cost += self.test_prices['Stained_Woo_PCV']
        
        if self.view.ui.parasite_centrifugal_dog_cat_checkBox.isChecked():
            total_tests += 1
            total_cost += self.test_prices['Centrifugal_dog_cat']
        
        if self.view.ui.parasite_floatation_centrifugal_checkBox.isChecked():
            total_tests += 1
            total_cost += self.test_prices['Floatation_centrifugal']
        
        if self.view.ui.parasite_floatation_dog_cat_checkBox.isChecked():
            total_tests += 1
            total_cost += self.test_prices['Floatation_dog_cat']
        
        if self.view.ui.parasite_stained_blood_smear_checkBox.isChecked():
            total_tests += 1
            total_cost += self.test_prices['Stained_blood_smear']
        
        if self.view.ui.parasite_sedimentation_checkBox.isChecked():
            total_tests += 1
            total_cost += self.test_prices['Sedimentation']
        
        if self.view.ui.parasite_Woo_checkBox.isChecked():
            total_tests += 1
            total_cost += self.test_prices['Woo']
        
        if self.view.ui.parasite_mc_master_egg_count_checkBox.isChecked():
            total_tests += 1
            total_cost += self.test_prices['Mc_Master']
        
        # Update summary display - CORRECTED WIDGET NAMES
        self.view.ui.parasite_num_lineEdit.setText(str(total_tests))
        self.view.ui.parasit_cost_lineEdit.setText(f"{total_cost:.2f}")  # Note: typo in UI "parasit" not "parasite"
    
    def get_parasite_data(self):
        """Get all parasite form data - CORRECTED WIDGET NAMES"""
        return {
            'PCV': self.view.ui.parasite_PCV_checkBox.isChecked(),
            'Floatation': self.view.ui.parasite_floatation_checkBox.isChecked(),
            'Parasite_in_meat': self.view.ui.parasite_parasite_in_meat_checkBox.isChecked(),
            'Parasite_identification': self.view.ui.parasite_parasite_identification_checkBox.isChecked(),
            'Stained_Woo_PCV': self.view.ui.parasite_stained_Woo_PCV_checkBox.isChecked(),
            'Centrifugal_dog_cat': self.view.ui.parasite_centrifugal_dog_cat_checkBox.isChecked(),
            'Floatation_centrifugal': self.view.ui.parasite_floatation_centrifugal_checkBox.isChecked(),
            'Floatation_dog_cat': self.view.ui.parasite_floatation_dog_cat_checkBox.isChecked(),
            'Stained_blood_smear': self.view.ui.parasite_stained_blood_smear_checkBox.isChecked(),
            'Sedimentation': self.view.ui.parasite_sedimentation_checkBox.isChecked(),
            'Woo': self.view.ui.parasite_Woo_checkBox.isChecked(),
            'Mc_Master': self.view.ui.parasite_mc_master_egg_count_checkBox.isChecked(),
            'total_tests': self.view.ui.parasite_num_lineEdit.text(),
            'total_cost': self.view.ui.parasit_cost_lineEdit.text()
        }
    
    def save_parasite_data(self):
        """Save parasite test data to database"""
        try:
            # Get data
            data = self.get_parasite_data()
            
            # Validate - at least one test must be selected
            if data['total_tests'] == '0' or not data['total_tests']:
                QMessageBox.warning(self.view, "คำเตือน", "กรุณาเลือกการตรวจอย่างน้อย 1 รายการ!")
                return
            
            # Connect to database
            connection = self.connect_database()
            cursor = connection.cursor()
            
            # SQL insert
            sql = """
            INSERT INTO parasite_biology_tests 
            (PCV, Floatation, Parasite_in_meat, Parasite_identification,
             Stained_Woo_PCV, Centrifugal_dog_cat, Floatation_centrifugal,
             Floatation_dog_cat, Stained_blood_smear, Sedimentation,
             Woo, Mc_Master, total_tests, total_cost, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(sql, (
                data['PCV'],
                data['Floatation'],
                data['Parasite_in_meat'],
                data['Parasite_identification'],
                data['Stained_Woo_PCV'],
                data['Centrifugal_dog_cat'],
                data['Floatation_centrifugal'],
                data['Floatation_dog_cat'],
                data['Stained_blood_smear'],
                data['Sedimentation'],
                data['Woo'],
                data['Mc_Master'],
                data['total_tests'],
                data['total_cost'],
                datetime.now()
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            QMessageBox.information(self.view, "สำเร็จ", "บันทึกข้อมูลการตรวจปรสิตสำเร็จ!")
            self.clear_parasite_information()
            self.go_back_to_new_work()  # ✅ Go back to New Work page instead of staying
            
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการบันทึก: {str(e)}")
    
    def clear_parasite_information(self):
        """Clear all parasite form fields - CORRECTED WIDGET NAMES"""
        # Uncheck all test checkboxes
        self.view.ui.parasite_PCV_checkBox.setChecked(False)
        self.view.ui.parasite_floatation_checkBox.setChecked(False)
        self.view.ui.parasite_parasite_in_meat_checkBox.setChecked(False)
        self.view.ui.parasite_parasite_identification_checkBox.setChecked(False)
        self.view.ui.parasite_stained_Woo_PCV_checkBox.setChecked(False)
        self.view.ui.parasite_centrifugal_dog_cat_checkBox.setChecked(False)
        self.view.ui.parasite_floatation_centrifugal_checkBox.setChecked(False)
        self.view.ui.parasite_floatation_dog_cat_checkBox.setChecked(False)
        self.view.ui.parasite_stained_blood_smear_checkBox.setChecked(False)
        self.view.ui.parasite_sedimentation_checkBox.setChecked(False)
        self.view.ui.parasite_Woo_checkBox.setChecked(False)
        self.view.ui.parasite_mc_master_egg_count_checkBox.setChecked(False)
        
        # Clear summary fields
        self.view.ui.parasite_num_lineEdit.clear()
        self.view.ui.parasit_cost_lineEdit.clear()
    
    def cancel_parasite(self):
        """Cancel and clear form"""
        reply = QMessageBox.question(
            self.view,
            "ยืนยันการยกเลิก",
            "คุณต้องการยกเลิกและล้างข้อมูลหรือไม่?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.clear_parasite_information()
            QMessageBox.information(self.view, "ยกเลิก", "ยกเลิกการกรอกข้อมูลแล้ว")
            self.go_back_to_specimen()
    
    def go_back_to_specimen(self):
        """Navigate back to Specimen page"""
        if self.main_window and hasattr(self.main_window, 'specimen_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.specimen_widget)
        else:
            print("Warning: Cannot navigate back to specimen page")
    
    def go_back_to_new_work(self):
        """Navigate back to New Work page and refresh data"""
        if self.main_window and hasattr(self.main_window, 'add_work_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.add_work_widget)
            
            # ✅ Refresh/update treewidget data when returning to New Work page
            if hasattr(self.main_window, 'new_work_controller') and self.main_window.new_work_controller:
                self.main_window.new_work_controller.update_treewidget_data()
        else:
            print("Warning: Cannot navigate back to new work page")
    
    def load_parasite_data(self, record_id):
        """Load existing parasite test data by ID"""
        try:
            connection = self.connect_database()
            cursor = connection.cursor()
            
            sql = "SELECT * FROM parasite_biology_tests WHERE id = ?"
            cursor.execute(sql, (record_id,))
            row = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if row:
                # Load checkboxes (columns 1-12)
                self.view.ui.parasite_PCV_checkBox.setChecked(bool(row[1]))
                self.view.ui.parasite_floatation_checkBox.setChecked(bool(row[2]))
                self.view.ui.parasite_parasite_in_meat_checkBox.setChecked(bool(row[3]))
                self.view.ui.parasite_parasite_identification_checkBox.setChecked(bool(row[4]))
                self.view.ui.parasite_stained_Woo_PCV_checkBox.setChecked(bool(row[5]))
                self.view.ui.parasite_centrifugal_dog_cat_checkBox.setChecked(bool(row[6]))
                self.view.ui.parasite_floatation_centrifugal_checkBox.setChecked(bool(row[7]))
                self.view.ui.parasite_floatation_dog_cat_checkBox.setChecked(bool(row[8]))
                self.view.ui.parasite_stained_blood_smear_checkBox.setChecked(bool(row[9]))
                self.view.ui.parasite_sedimentation_checkBox.setChecked(bool(row[10]))
                self.view.ui.parasite_Woo_checkBox.setChecked(bool(row[11]))
                self.view.ui.parasite_mc_master_egg_count_checkBox.setChecked(bool(row[12]))
                
                # Load summary (columns 13-14)
                self.view.ui.parasite_num_lineEdit.setText(str(row[13]))
                self.view.ui.parasit_cost_lineEdit.setText(str(row[14]))
                
                QMessageBox.information(self.view, "สำเร็จ", "โหลดข้อมูลสำเร็จ!")
            else:
                QMessageBox.warning(self.view, "คำเตือน", "ไม่พบข้อมูล!")
                
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
    
    def enable_parasite_widgets(self):
        """Enable all parasite widgets - CORRECTED WIDGET NAMES"""
        self.view.ui.parasite_PCV_checkBox.setEnabled(True)
        self.view.ui.parasite_floatation_checkBox.setEnabled(True)
        self.view.ui.parasite_parasite_in_meat_checkBox.setEnabled(True)
        self.view.ui.parasite_parasite_identification_checkBox.setEnabled(True)
        self.view.ui.parasite_stained_Woo_PCV_checkBox.setEnabled(True)
        self.view.ui.parasite_centrifugal_dog_cat_checkBox.setEnabled(True)
        self.view.ui.parasite_floatation_centrifugal_checkBox.setEnabled(True)
        self.view.ui.parasite_floatation_dog_cat_checkBox.setEnabled(True)
        self.view.ui.parasite_stained_blood_smear_checkBox.setEnabled(True)
        self.view.ui.parasite_sedimentation_checkBox.setEnabled(True)
        self.view.ui.parasite_Woo_checkBox.setEnabled(True)
        self.view.ui.parasite_mc_master_egg_count_checkBox.setEnabled(True)
        self.view.ui.parasite_save_pushButton.setEnabled(True)
        self.view.ui.parasite_cancel_pushButton.setEnabled(True)
    
    def disable_parasite_widgets(self):
        """Disable all parasite widgets - CORRECTED WIDGET NAMES"""
        self.view.ui.parasite_PCV_checkBox.setEnabled(False)
        self.view.ui.parasite_floatation_checkBox.setEnabled(False)
        self.view.ui.parasite_parasite_in_meat_checkBox.setEnabled(False)
        self.view.ui.parasite_parasite_identification_checkBox.setEnabled(False)
        self.view.ui.parasite_stained_Woo_PCV_checkBox.setEnabled(False)
        self.view.ui.parasite_centrifugal_dog_cat_checkBox.setEnabled(False)
        self.view.ui.parasite_floatation_centrifugal_checkBox.setEnabled(False)
        self.view.ui.parasite_floatation_dog_cat_checkBox.setEnabled(False)
        self.view.ui.parasite_stained_blood_smear_checkBox.setEnabled(False)
        self.view.ui.parasite_sedimentation_checkBox.setEnabled(False)
        self.view.ui.parasite_Woo_checkBox.setEnabled(False)
        self.view.ui.parasite_mc_master_egg_count_checkBox.setEnabled(False)
        self.view.ui.parasite_save_pushButton.setEnabled(False)
        self.view.ui.parasite_cancel_pushButton.setEnabled(False)
    
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