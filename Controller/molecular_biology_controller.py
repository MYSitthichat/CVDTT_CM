from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox

class MolecularBiologyController(QObject):
    """ Controller for the Molecular Biology Page """

    def __init__(self, model, view, main_window_view):
        super().__init__()
        self.model = model
        self.view = view # MolecularBiologyPageWidget
        self.main_window = main_window_view
        
        self.event_bindings()

    def event_bindings(self):
        """ Bind UI events """
        # Using button names found in your molecular.py file
        self.view.ui.cal_pushButton.clicked.connect(self.compute_summary)
        self.view.ui.save_pushButton.clicked.connect(self.save_data)
        self.view.ui.back_pushButton.clicked.connect(self.go_back)

    def compute_summary(self):
        print("--- ACTION: Calculate Button Pressed ---")
        
        # Get data from view
        selected_items = self.view.get_data()
        
        count = len(selected_items)
        total_cost = sum(item['price'] for item in selected_items)
        
        print(f"Calculated: {count} items, Total Cost: {total_cost}")
        
        # Update View
        self.view.set_summary(count, total_cost)

    def save_data(self):
        print("--- ACTION: Save Button Pressed ---")
        
        selected_items = self.view.get_data()
        
        if not selected_items:
            print("Validation: No items selected")
            QMessageBox.warning(self.view, "Warning", "กรุณาเลือกรายการที่ต้องการส่งตรวจ (Please select items)")
            return

        print(f"Saving {len(selected_items)} items...")
        for item in selected_items:
            print(f" - Item: {item['name']}, Sample: {item['sample_id']}, Price: {item['price']}")

        # Simulate Saving to Model
        # success = self.model.save_molecular_data(selected_items)
        success = True 
        
        if success:
            print("Status: Save Successful")
            QMessageBox.information(self.view, "Success", "บันทึกข้อมูลเรียบร้อย (Saved Successfully)")
            self.go_back()
        else:
            print("Status: Save Failed")

    def go_back(self):
        if hasattr(self.main_window, 'specimen_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.specimen_widget)
        else:
            print("Error: Specimen Widget not found in Main Window")