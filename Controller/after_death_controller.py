from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox

class AfterDeathPageController(QObject):
    """ Controller for the After Death Service Page """

    def __init__(self, model, view, main_controller):
        super().__init__()
        self.model = model
        self.view = view # AfterDeathPageWidget
        self.main_controller = main_controller
        
        self.event_bindings()

    def event_bindings(self):
        self.view.ui.btn_save.clicked.connect(self.save_data)
        self.view.ui.btn_cancel.clicked.connect(self.go_back)

    def save_data(self):
        print("--- ACTION: Save After Death Data ---")
        
        # 1. Get Sample ID (From Specimen Page via MainWindow)
        try:
            # Check if specimen widget exists and has the label
            if hasattr(self.main_controller, 'specimen_widget'):
                sample_id_text = self.main_controller.specimen_widget.ui.specimen_page_label.text()
                if ":" in sample_id_text:
                    sample_id = sample_id_text.split(":")[1].strip()
                else:
                    QMessageBox.critical(self.view, "Error", "ไม่พบรหัสตัวอย่าง (Sample ID Not Found)")
                    return
            else:
                # Fallback for testing
                sample_id = "TEST_ID" 
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Error getting Sample ID: {e}")
            return

        # 2. Get User ID
        if self.main_controller.user_login_info:
            user_id = self.main_controller.user_login_info[0][1]
        else:
            user_id = 0 # Fallback or Error

        # 3. Get Data
        data = self.view.get_data()
        print(f"Saving Data for ID {sample_id}: {data}")

        # 4. Call Model
        # Assuming model.save_after_death_information exists
        if self.model.save_after_death_information(sample_id, data, user_id):
            QMessageBox.information(self.view, "Success", "บันทึกข้อมูลเรียบร้อย")
            
            # Track status
            self.model.save_tracking_information(sample_id, user_id, user_id, f"After Death Service: {data['service_type']}")
            
            self.view.clear_page()
            self.go_back()
        else:
             QMessageBox.critical(self.view, "Error", "ไม่สามารถบันทึกข้อมูลได้")

    def go_back(self):
        if hasattr(self.main_controller, 'specimen_widget'):
            self.main_controller.ui.stackedWidget.setCurrentWidget(self.main_controller.specimen_widget)