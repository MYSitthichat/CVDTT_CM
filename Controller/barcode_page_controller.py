from PySide6.QtWidgets import QTableWidgetItem, QMessageBox
from PySide6.QtCore import QObject
from barcode_utils.barcode_generator import BarcodeGenerator

class BarcodePageController(QObject):
    """ Controller for the Barcode/Sticker Page """

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view 
        
        # Bind Events
        self.event_bindings()

    @property
    def ui(self):
        if hasattr(self.view, 'ui'):
            return self.view.ui
        return self.view

    def event_bindings(self):
        """ Bind UI events to controller methods """
        self.ui.btn_search_today.clicked.connect(self.search_today_cases)
        self.ui.btn_search_customer.clicked.connect(self.search_by_customer)
        self.ui.btn_print.clicked.connect(self.print_barcode)

    def search_today_cases(self):
        """ Search all cases registered today """
        self.view.clear_inputs()
        
        raw_data = self.model.get_today_case_detail()
        
        if raw_data is None or len(raw_data) == 0:
            QMessageBox.information(self.view, "Info", "ไม่พบข้อมูลงานในวันนี้")
            self.ui.tableWidget.setRowCount(0)
            return

        self.populate_table(raw_data)

    def search_by_customer(self):
        """ Search cases based on Customer Name/Surname """
        name = self.ui.lineEdit_firstname.text()
        surname = self.ui.lineEdit_lastname.text()

        if name == "" and surname == "":
            QMessageBox.warning(self.view, "Warning", "กรุณากรอกชื่อหรือนามสกุลเพื่อค้นหา")
            return

        raw_data = self.model.get_case_detail_by_customer_name(name, surname)
        
        if raw_data is None or len(raw_data) == 0:
            QMessageBox.information(self.view, "Info", "ไม่พบข้อมูลลูกค้า")
            self.ui.tableWidget.setRowCount(0)
            return
        self.populate_table(raw_data)

    def populate_table(self, data):
        """ Populates the QTableWidget """
        table = self.ui.tableWidget
        table.setRowCount(0) 
        
        for row_idx, item in enumerate(data):
            table.insertRow(row_idx)
            
            date_val = item[0]
            if hasattr(date_val, 'strftime'):
                date_val = date_val.strftime("%d-%m-%Y %H:%M:%S")
            table.setItem(row_idx, 0, QTableWidgetItem(str(date_val)))
            
            # Col 1: Barcode ID
            table.setItem(row_idx, 1, QTableWidgetItem(str(item[1]).zfill(10)))
            
            # Col 2: Species
            table.setItem(row_idx, 2, QTableWidgetItem(str(item[2])))
            
            # Col 3: Lab Name (Already formatted by SQL)
            table.setItem(row_idx, 3, QTableWidgetItem(str(item[3])))
            
            # Col 4: Storage
            table.setItem(row_idx, 4, QTableWidgetItem(str(item[4])))
            
            # Col 5: Urgency
            table.setItem(row_idx, 5, QTableWidgetItem(str(item[5])))
            
            # Col 6: Info (Empty column)
            table.setItem(row_idx, 6, QTableWidgetItem(""))

    def print_barcode(self):
        """ Print barcode for the selected row """
        table = self.ui.tableWidget
        selected_ranges = table.selectedRanges()
        
        if not selected_ranges:
            QMessageBox.critical(self.view, "Error", "กรุณาเลือกรายการเพื่อพิมพ์บาร์โค้ด")
            return

        selected_row = selected_ranges[0].topRow()
        
        row_data = []
        for col in range(6): 
            item = table.item(selected_row, col)
            text = item.text() if item else ""
            row_data.append(text)

        data_to_print = [row_data]

        try:
            barcode_obj = BarcodeGenerator()
            barcode_obj.generate(data_to_print)
            barcode_obj.print_barcode()
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"เกิดข้อผิดพลาดในการพิมพ์: {str(e)}")