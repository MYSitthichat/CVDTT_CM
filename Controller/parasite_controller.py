from View.view_parasite_frame import parasiteFrameView
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox
from API.client_app import APIApp
import pyodbc
from datetime import datetime


class ParasiteController(QObject):
    """Controller for Parasite Biology Page - mimicking lab_manager structure"""
    
    def __init__(self, view: parasiteFrameView, parent=None):
        super().__init__(parent)
        self.view = view
        self.main_window = parent  # Store reference to main window
        self.api_client = APIApp()  # Initialize API client
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
        """
        Get all parasite test data in the same format as molecular biology.
        Returns a list of dictionaries with test name (with price), quantity, and price separated.
        """
        # Define test mappings with proper names and prices - in order t1 to t12
        test_configs = [
            {'name': 'PCV', 'price': 50, 'checkbox': self.view.ui.parasite_PCV_checkBox},
            {'name': 'Floatation', 'price': 50, 'checkbox': self.view.ui.parasite_floatation_checkBox},
            {'name': 'Parasite in meat', 'price': 300, 'checkbox': self.view.ui.parasite_parasite_in_meat_checkBox},
            {'name': 'Parasite identification', 'price': 100, 'checkbox': self.view.ui.parasite_parasite_identification_checkBox},
            {'name': 'Stained + Woo + PCV', 'price': 150, 'checkbox': self.view.ui.parasite_stained_Woo_PCV_checkBox},
            {'name': 'Centrifugal for dog/cat', 'price': 150, 'checkbox': self.view.ui.parasite_centrifugal_dog_cat_checkBox},
            {'name': 'Floatation + Centrifugal', 'price': 200, 'checkbox': self.view.ui.parasite_floatation_centrifugal_checkBox},
            {'name': 'Floatation for dog/cat', 'price': 100, 'checkbox': self.view.ui.parasite_floatation_dog_cat_checkBox},
            {'name': 'Stained blood smear', 'price': 100, 'checkbox': self.view.ui.parasite_stained_blood_smear_checkBox},
            {'name': 'Sedimentation', 'price': 50, 'checkbox': self.view.ui.parasite_sedimentation_checkBox},
            {'name': 'Woo\'s', 'price': 50, 'checkbox': self.view.ui.parasite_Woo_checkBox},
            {'name': 'Mc Master egg count', 'price': 100, 'checkbox': self.view.ui.parasite_mc_master_egg_count_checkBox}
        ]
        
        test_items = []
        for config in test_configs:
            is_checked = config['checkbox'].isChecked()
            name_with_price = f"{config['name']} ({config['price']})"
            test_items.append({
                'name': name_with_price,  # Name with price e.g., "PCV (50)"
                'quantity': 1 if is_checked else 0,  # 1 if selected, 0 if not
                'price': config['price']  # Always include unit price
            })
        
        return test_items
    
    def save_parasite_data(self):
        try:
            # Get all test items
            all_test_items = self.get_parasite_data()
            
            # Get only selected items for validation
            selected_items = [item for item in all_test_items if item['quantity'] > 0]
            
            if not selected_items:
                QMessageBox.warning(
                    self.view, 
                    "Warning", 
                    "กรุณาเลือกรายการที่ต้องการส่งตรวจ\n(Please select at least one test)"
                )
                return
            
            # Get sample_id from specimen_controller
            sample_id = None
            if hasattr(self.main_window, 'specimen_controller'):
                specimen_ctrl = self.main_window.specimen_controller
                if hasattr(specimen_ctrl, 'specimen_id') and specimen_ctrl.specimen_id:
                    sample_id = str(specimen_ctrl.specimen_id)
            
            if not sample_id:
                QMessageBox.warning(
                    self.view,
                    "ไม่พบหมายเลข Sample ID",
                    "กรุณาบันทึกข้อมูล Specimen ในหน้าก่อนหน้านี้ก่อน\n"
                    "แล้วจึงกลับมาเลือกรายการตรวจ Parasite"
                )
                return
            
            # Get user_id from main controller
            user_id = None
            if hasattr(self.main_window, 'main_controller'):
                main_ctrl = self.main_window.main_controller
                if hasattr(main_ctrl, 'logged_in_user_id') and main_ctrl.logged_in_user_id:
                    user_id = main_ctrl.logged_in_user_id
            
            if not user_id:
                QMessageBox.warning(
                    self.view,
                    "ไม่พบข้อมูลผู้ใช้",
                    "กรุณา Login ใหม่อีกครั้ง"
                )
                return
            
            # Get room_id for parasite lab
            room_id = None
            if hasattr(self.main_window, 'specimen_controller'):
                specimen_ctrl = self.main_window.specimen_controller
                if hasattr(specimen_ctrl, 'room_mapping') and 'parasitology' in specimen_ctrl.room_mapping:
                    room_id = specimen_ctrl.room_mapping['parasitology']
            
            # Prepare data for parasite biology API
            parasite_data = {
                "sample_id": sample_id,
                "tests": all_test_items,
                "updater": user_id
            }
            # Prepare data for lab order API
            lab_order_data = {
                "sample_id": sample_id,
                "room_id": str(room_id) if room_id else None,
                "comments": "",
                "state": "0",
                "status": "1",
                "updater": user_id
            }
            
            # Prepare first tracking entry
            first_update_tracking_lab_order_data = {
                "lab_order_id": sample_id,
                "tracking_info": "รับงานเข้าระบบ",
                "receiver": str(user_id),
                "updater": str(user_id)
            }
            
            # Call APIs
            save_parasite_result = self.api_client.save_parasite_biology(parasite_data)
            insert_lab_order = self.api_client.add_new_lab_order(lab_order_data)
            first_update_tracking = self.api_client.update_tracking_lab_order(first_update_tracking_lab_order_data)
            
            # Check results
            if (save_parasite_result and save_parasite_result.get("status") == "success" and
                insert_lab_order and first_update_tracking and 
                first_update_tracking.get("status") == "success"):
                
                selected_count = len(selected_items)
                total_cost = sum(item['price'] * item['quantity'] for item in selected_items)
                
                QMessageBox.information(
                    self.view,
                    "สำเร็จ",
                    f"บันทึกข้อมูลการตรวจปรสิตเรียบร้อย\n\n"
                    f"Sample ID: {sample_id}\n"
                    f"รายการที่เลือก: {selected_count} รายการ\n"
                    f"ราคารวม: {total_cost:.2f} บาท"
                )
                
                self.clear_parasite_information()
                self.go_back_to_new_work()
            else:
                error_msg = "Unknown error"
                if save_parasite_result and isinstance(save_parasite_result, dict):
                    error_msg = save_parasite_result.get('detail', error_msg)
                
                QMessageBox.critical(
                    self.view,
                    "ข้อผิดพลาด",
                    f"บันทึกข้อมูลไม่สำเร็จ\n\n{error_msg}"
                )
            
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "ข้อผิดพลาด",
                f"เกิดข้อผิดพลาดในการบันทึก: {str(e)}"
            )
    
    def clear_parasite_information(self):
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