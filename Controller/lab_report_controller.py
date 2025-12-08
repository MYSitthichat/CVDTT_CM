import os
import sys
import tempfile
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox
from PySide6.QtCore import QObject
from Order_Lab_Pdf.pdf_from  import parasite_order_from
from Order_Lab_Pdf.pdf_from import bacteria_order_from
from Order_Lab_Pdf.pdf_from import molecular_order_from

class LabReportPageController(QObject):
    """ Controller for the Lab Report Page """

    # UPDATED: Added 'main_window' to the arguments
    def __init__(self, model, view, main_window=None):
        super().__init__()
        self.model = model
        self.view = view # LabReportPageWidget
        self.main_window = main_window # Store reference just in case
        
        self.event_bindings()

    def event_bindings(self):
        """ Bind UI events """
        self.view.ui.search_button.clicked.connect(self.search_reports)
        self.view.ui.print_button.clicked.connect(self.print_report)

    def search_reports(self):
        """ Search for lab reports by barcode """
        barcode = self.view.get_search_text()
        
        # Assuming 'search_lab_report' returns: [Date, Barcode, Sender, Animal, CaseID, LabType]
        # If your model returns empty list for empty search, this works fine.
        data = self.model.search_lab_report(barcode) 
        
        self.populate_table(data)

    def populate_table(self, data):
        table = self.view.ui.result_table
        table.setRowCount(0)
        
        if not data:
            QMessageBox.information(self.view, "Info", "ไม่พบข้อมูล (No Data Found)")
            return

        for row_idx, item in enumerate(data):
            table.insertRow(row_idx)
            
            # 0. Date
            date_val = item[0].strftime("%d-%m-%Y") if hasattr(item[0], 'strftime') else str(item[0])
            table.setItem(row_idx, 0, QTableWidgetItem(date_val))
            
            # 1. Barcode
            barcode_val = str(item[1]).zfill(10)
            table.setItem(row_idx, 1, QTableWidgetItem(barcode_val))
            
            # 2. Sender
            table.setItem(row_idx, 2, QTableWidgetItem(str(item[2])))
            
            # 3. Animal
            table.setItem(row_idx, 3, QTableWidgetItem(str(item[3])))

            # Store hidden data (Case ID and Lab Type)
            # Adjust indices [4] and [5] based on your actual SQL query result
            if len(item) > 5:
                 table.item(row_idx, 0).setData(100, item[4]) # Case ID
                 table.item(row_idx, 0).setData(101, item[5]) # Lab Type

    def print_report(self):
        """ Generate and open PDF report """
        table = self.view.ui.result_table
        selected_ranges = table.selectedRanges()
        
        if not selected_ranges:
            QMessageBox.critical(self.view, "Error", "กรุณาเลือกรายการเพื่อพิมพ์ (Please select a row)")
            return
            
        row = selected_ranges[0].topRow()
        
        # Retrieve hidden data
        case_id = table.item(row, 0).data(100)
        case_lab_type = table.item(row, 0).data(101)
        
        # Fallback if hidden data is missing
        if not case_id:
            try:
                case_id = int(table.item(row, 1).text())
            except:
                QMessageBox.critical(self.view, "Error", "Invalid Case ID")
                return

        self.generate_pdf(case_id, case_lab_type)

    def generate_pdf(self, case_id, case_lab):
        """ Logic extracted from your old main_controller """
        try:
            # Add Order_Lab_Pdf/from to path for dynamic import
            project_root = os.path.dirname(os.path.dirname(__file__))
            pdf_from_path = os.path.join(project_root, "Order_Lab_Pdf", "from")
            if pdf_from_path not in sys.path:
                sys.path.insert(0, pdf_from_path)
            
            # 1. Get Info
            sample_info = self.model.get_sample_information_by_id(case_id)
            
            # 2. Prepare Temp File
            temp_folder = tempfile.mkdtemp()
            temp_pdf_file = os.path.join(temp_folder, "lab_order.pdf")
            
            test_info = []
            
            case_lab_str = str(case_lab)

            # 3. Generate based on Lab Type
            if 'Parasite' in case_lab_str:
                test_info = self.model.get_parasite_test_information_by_id(case_id)
                parasite_order_from.create_parasite_biology(sample_info, test_info, temp_pdf_file)
                os.system(f"start {temp_pdf_file}")

            elif 'Fungal' in case_lab_str or 'Bacteria' in case_lab_str:
                test_info = self.model.get_bacteriology_test_information_by_id(case_id)
                bacteria_order_from.create_bacteriology(sample_info, test_info, temp_pdf_file)
                os.system(f"start {temp_pdf_file}")

            elif 'PCR' in case_lab_str or 'Molecular' in case_lab_str:
                test_info = self.model.get_molecular_test_information_by_id(case_id)
                molecular_order_from.create_molecular_biology(sample_info, test_info, temp_pdf_file)
                os.system(f"start {temp_pdf_file}")
                
            else:
                QMessageBox.warning(self.view, "Warning", f"ไม่รองรับการพิมพ์สำหรับห้องปฏิบัติการนี้: {case_lab}")

        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Failed to generate PDF: {str(e)}")