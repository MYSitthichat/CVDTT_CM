from PySide6.QtWidgets import QTableWidgetItem, QMessageBox
from PySide6.QtCore import QObject

class CheckJobProgressController(QObject):
    """ Controller for the Check Job Progress Page """

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view 
        
        # Bind Events
        self.event_bindings()

    def event_bindings(self):
        """ Bind UI events to controller methods """
        self.view.ui.btn_jobs_in_system.clicked.connect(self.search_jobs_in_system)
        self.view.ui.btn_show_details.clicked.connect(self.show_job_details)

    def search_jobs_in_system(self):
        """ Search active jobs in the system (Top Table) """
        self.view.ui.tableTop.setRowCount(0)
        self.view.ui.tableBottom.setRowCount(0)
        
        job_data = self.model.get_job_detail_in_check_job_progress_page()
        
        if not job_data:
            QMessageBox.information(self.view, "Info", "ไม่พบข้อมูลงานในระบบ")
            return

        self.populate_top_table(job_data)

    def show_job_details(self):
        """ Show details for the selected job (Bottom Table) """
        table_top = self.view.ui.tableTop
        selected_ranges = table_top.selectedRanges()

        if not selected_ranges:
            QMessageBox.critical(self.view, "Error", "กรุณาเลือกงานเพื่อดูรายละเอียด")
            return
        
        selected_row = selected_ranges[0].topRow()
        
        # Get Job ID from column 1. 
        # Note: It might be padded now (0000001434), but int() handles that automatically.
        item_job_id = table_top.item(selected_row, 1)
        
        if not item_job_id:
            return

        try:
            job_id = int(item_job_id.text())
            
            job_details = self.model.get_job_detail_in_check_job_progress_page_by_id(job_id)
            self.populate_bottom_table(job_details)
            
        except ValueError:
            QMessageBox.critical(self.view, "Error", "Invalid Job ID format")

    def populate_top_table(self, data):
        """ Populates the Top Table (Active Jobs) """
        table = self.view.ui.tableTop
        table.setRowCount(0)

        for row_idx, item in enumerate(data):
            table.insertRow(row_idx)
            
            # 0. Date/Time
            date_val = str(item[0]) 
            table.setItem(row_idx, 0, QTableWidgetItem(date_val))
            
            # 1. Barcode ID <--- FIXED HERE
            # Convert to string and pad with zeros to length 10
            barcode_val = str(item[1]).zfill(10)
            table.setItem(row_idx, 1, QTableWidgetItem(barcode_val))
            
            # 2. Status
            status_val = str(item[2])
            table.setItem(row_idx, 2, QTableWidgetItem(status_val))

    def populate_bottom_table(self, data):
        """ Populates the Bottom Table (Job History/Details) """
        table = self.view.ui.tableBottom
        table.setRowCount(0)

        if not data:
            return

        for row_idx, item in enumerate(data):
            table.insertRow(row_idx)
            
            # 0. Time
            time_val = str(item[0])
            table.setItem(row_idx, 0, QTableWidgetItem(time_val))
            
            # 1. Barcode <--- FIXED HERE
            barcode_val = str(item[1]).zfill(10)
            table.setItem(row_idx, 1, QTableWidgetItem(barcode_val))
            
            # 2. Detail
            detail_val = str(item[2])
            table.setItem(row_idx, 2, QTableWidgetItem(detail_val))
            
            # 3. Operator
            operator_val = str(item[3])
            table.setItem(row_idx, 3, QTableWidgetItem(operator_val))