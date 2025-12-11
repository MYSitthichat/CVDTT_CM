from PySide6.QtWidgets import QTableWidgetItem, QMessageBox
from PySide6.QtCore import QObject

class LabReceivedSampleController(QObject):
    """ Controller for the Lab Received Sample Page """

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view # This is the LabReceivedSampleWidget instance
        
        self.event_bindings()

    @property
    def ui(self):
        # Helper to access UI elements easily
        if hasattr(self.view, 'ui'):
            return self.view.ui
        return self.view

    def event_bindings(self):
        """ Bind UI events to controller methods """
        # 1. Search employee when typing
        self.ui.le_search.textChanged.connect(self.search_employee)
        
        # 2. Select employee button
        self.ui.btn_select.clicked.connect(self.select_employee)
        
        # 3. Save tracking info button
        self.ui.btn_save.clicked.connect(self.save_received_sample)

    def search_employee(self):
        """ Search for employees based on name input """
        search_text = self.ui.le_search.text().strip()
        self.ui.table_staff.setRowCount(0) # Clear table
        
        if not search_text:
            return

        # Fetch data from model
        # Expecting list of [id, name, surname]
        employees = self.model.search_employee_by_name(search_text)
        
        if not employees:
            return

        for row_idx, emp in enumerate(employees):
            self.ui.table_staff.insertRow(row_idx)
            
            # Col 0: Name
            self.ui.table_staff.setItem(row_idx, 0, QTableWidgetItem(str(emp[1])))
            # Col 1: Surname
            self.ui.table_staff.setItem(row_idx, 1, QTableWidgetItem(str(emp[2])))
            # Col 2: ID
            self.ui.table_staff.setItem(row_idx, 2, QTableWidgetItem(str(emp[0])))

    def select_employee(self):
        """ Select the employee from the table and fill the fields """
        selected_ranges = self.ui.table_staff.selectedRanges()
        
        if not selected_ranges:
            QMessageBox.warning(self.view, "Warning", "กรุณาเลือกรายชื่อเจ้าหน้าที่")
            return

        selected_row = selected_ranges[0].topRow()
        
        # Get data from the selected row
        name = self.ui.table_staff.item(selected_row, 0).text()
        surname = self.ui.table_staff.item(selected_row, 1).text()
        emp_id = self.ui.table_staff.item(selected_row, 2).text()
        
        # Fill the bottom fields
        self.ui.le_receiver.setText(f"{name} {surname}")
        self.ui.le_receiver_id.setText(emp_id)

    def save_received_sample(self):
        """ Save the tracking information to the database """
        barcode_id = self.ui.le_barcode.text().strip()
        receiver_id = self.ui.le_receiver_id.text().strip()
        
        
        if not barcode_id:
            QMessageBox.critical(self.view, "Error", "กรุณากรอกรหัสบาร์โค้ด")
            return
            
        if not receiver_id:
            QMessageBox.critical(self.view, "Error", "กรุณาเลือกผู้รับสิ่งส่งตรวจ")
            return

        updater_id = receiver_id 
        
        info_text = "รับสิ่งส่งตรวจแล้ว" 

        # Call Model
        success = self.model.save_tracking_information(barcode_id, receiver_id, updater_id, info_text)
        
        if success:
            QMessageBox.information(self.view, "Success", "บันทึกข้อมูลเรียบร้อย")
            self.view.clear_inputs()
        else:
            QMessageBox.critical(self.view, "Error", "บันทึกข้อมูลล้มเหลว (ตรวจสอบ Barcode)")