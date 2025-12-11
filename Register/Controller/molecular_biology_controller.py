from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox
# from API.client_app import APIApp
from SERVICES_REGISTER.lab_service import LabService

class MolecularBiologyController(QObject):
    """ Controller for the Molecular Biology Page """

    def __init__(self, model, view, main_window_view):
        super().__init__()
        self.model = model
        self.view = view # MolecularBiologyPageWidget
        self.main_window = main_window_view
        self.api_client = LabService()
        
        self.event_bindings()

    def event_bindings(self):
        """ Bind UI events """
        # Using button names found in your molecular.py file
        self.view.ui.cal_pushButton.clicked.connect(self.compute_summary)
        self.view.ui.save_pushButton.clicked.connect(self.save_data)
        self.view.ui.back_pushButton.clicked.connect(self.go_to_specimen)

    def compute_summary(self):
        # Let the view calculate and display the summary
        summary = self.view.calculate_summary()
        if summary is None:
            return


    def save_data(self):
        summary = self.view.calculate_summary()
        if summary is None:
            return
        all_test_items = self.view.get_data()
        selected_items = summary['items']
        
        if not selected_items:
            QMessageBox.warning(self.view, "Warning", "กรุณาเลือกรายการที่ต้องการส่งตรวจ (Please select items)")
            return
        
        sample_id = None
        
        if hasattr(self.main_window, 'specimen_controller'):
            specimen_ctrl = self.main_window.specimen_controller
            if hasattr(specimen_ctrl, 'specimen_id') and specimen_ctrl.specimen_id:
                sample_id = str(specimen_ctrl.specimen_id)  # ✅ Convert to string
        if not sample_id:
            if hasattr(self.main_window, 'specimen_widget') and hasattr(self.main_window.specimen_widget, 'ui'):
                if hasattr(self.main_window.specimen_widget.ui, 'specimen_ID_lineEdit'):
                    sample_id_text = self.main_window.specimen_widget.ui.specimen_ID_lineEdit.text().strip()
                    if sample_id_text:
                        sample_id = str(sample_id_text)
        
        if not sample_id:
            QMessageBox.warning(
                self.view, 
                "ไม่พบหมายเลข Sample ID", 
                "กรุณาบันทึกข้อมูล Specimen ในหน้าก่อนหน้านี้ก่อน\n"
                "แล้วจึงกลับมาเลือกรายการตรวจ Molecular Biology"
            )
            return

        # Get user_id from main controller
        user_id = None 
        if hasattr(self.main_window, 'main_controller'):
            main_ctrl = self.main_window.main_controller
            if hasattr(main_ctrl, 'logged_in_user_id') and main_ctrl.logged_in_user_id:
                user_id = main_ctrl.logged_in_user_id
            else:
                pass
        else:
            pass
        
        if not user_id:
            QMessageBox.warning(
                self.view,
                "ไม่พบข้อมูลผู้ใช้",
                "กรุณา Login ใหม่อีกครั้ง"
            )
            return
        
        total_cost = 0
        total_samples = 0
        
        for idx, item in enumerate(selected_items, 1):
            unit_price = item.get('unit_price', 0)
            quantity = item.get('quantity', 0)
            total_price = item.get('total_price', 0)
            
            total_cost += total_price
            total_samples += quantity
        
        # Get room_id from specimen_controller's room mapping
        room_id = "8"  # Default room_id for Molecular Biology (อณูชีววิทยา)
        if hasattr(self.main_window, 'specimen_controller'):
            specimen_ctrl = self.main_window.specimen_controller
            if hasattr(specimen_ctrl, 'room_mapping') and 'molecular_biology' in specimen_ctrl.room_mapping:
                room_id = specimen_ctrl.room_mapping['molecular_biology']
        
        # Get Laboratory Request values (cPCR, qPCR, Extraction)
        cPCR_req = 1 if self.view.ui.r_c.isChecked() else 0
        qPCR_req = 1 if self.view.ui.r_q.isChecked() else 0
        extraction_req = 1 if self.view.ui.r_e.isChecked() else 0
        
        # Prepare data for API
        molecular_data = {
            "sample_id": sample_id,
            "tests": all_test_items,
            "cPCR_req": cPCR_req,
            "qPCR_req": qPCR_req,
            "extraction_req": extraction_req,
            "updater": user_id
        }
        
        lab_order_data = {
            "sample_id": sample_id,
            "room_id": str(room_id),
            "comments": "",
            "state": "0",
            "status": "1",
            "updater": user_id
        }
        
        first_update_tracking_lab_order_data = {
            "sample_id": sample_id,
            "tracking_info": "รับงานเข้าระบบ",
            "receiver": str(user_id),
            "updater": str(user_id)
        }
        
        # Call API to save data
        save_molecular_result = self.api_client.save_molecular_biology(molecular_data)
        insert_lab_order = self.api_client.add_new_lab_order(lab_order_data)
        first_update_tracking_lab_order = self.api_client.update_tracking_lab_order(first_update_tracking_lab_order_data)

        if save_molecular_result and insert_lab_order and first_update_tracking_lab_order.get("status") == "success":
            selected_count = len(selected_items)
            total_count = len(all_test_items)
            
            # Create Laboratory Request info text
            lab_req_info = []
            if cPCR_req:
                lab_req_info.append("cPCR")
            if qPCR_req:
                lab_req_info.append("qPCR")
            if extraction_req:
                lab_req_info.append("Extraction")
            
            lab_req_text = ", ".join(lab_req_info) if lab_req_info else "ไม่ระบุ"
            
            QMessageBox.information(
                self.view, 
                "Success", 
                f"บันทึกข้อมูลเรียบร้อย (Saved Successfully)\n\n"
                f"Sample ID: {sample_id}\n"
                f"รายการที่เลือก: {selected_count} รายการ\n"
                f"Laboratory Request: {lab_req_text}"
            )
            # Clear the page after successful save
            self.view.clear_page()
            # Go back to specimen page
            
            self.go_back()
        else:
            error_msg = save_molecular_result.get('detail', 'Unknown error') if save_molecular_result else "Cannot connect to server"
            QMessageBox.critical(
                self.view,
                "Error",
                f"บันทึกข้อมูลไม่สำเร็จ (Save Failed)\n\n{error_msg}"
            )

    def go_back(self):
        if hasattr(self.main_window, 'add_work_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.add_work_widget)
            
            # Refresh/update treewidget data when returning to New Work page
            if hasattr(self.main_window, 'new_work_controller') and self.main_window.new_work_controller:
                self.main_window.new_work_controller.update_treewidget_data()
        else:
            print("Error: Add Work Widget not found in Main Window")
            
    def go_to_specimen(self):
        reply = QMessageBox.question(
            self.view,
            "ยืนยันการยกเลิก",
            "คุณต้องการยกเลิกและล้างข้อมูลหรือไม่?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            QMessageBox.information(self.view, "ยกเลิก", "ยกเลิกการกรอกข้อมูลแล้ว")
        if hasattr(self.main_window, 'specimen_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.specimen_widget)
        else:
            print("Error: Specimen Widget not found in Main Window")
            