import os
import sys
import tempfile
from datetime import datetime
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox
from PySide6.QtCore import QObject, Qt
from Order_Lab_Pdf.pdf_from  import parasite_order_from
from Order_Lab_Pdf.pdf_from import bacteria_order_from
from Order_Lab_Pdf.pdf_from import molecular_order_from
from SERVICES_REGISTER.lab_order_service import LabOrderService
import subprocess
import platform

class LabReportPageController(QObject):
    def __init__(self, model, view, main_window=None):
        super().__init__()
        self.model = model
        self.view = view # LabReportPageWidget
        self.main_window = main_window # Store reference just in case
        self.API_lab_order = LabOrderService()
        
        self.event_bindings()

    def event_bindings(self):
        self.view.ui.search_button.clicked.connect(self.search_orders)
        self.view.ui.print_button.clicked.connect(self.print_lab_orders)
        self.view.ui.search_to_day_button.clicked.connect(self.search_to_day_orders)


    def search_to_day_orders(self):
        try:
            result = self.API_lab_order.search_today_orders()
            
            if result and result.get('status') == 'success':
                data = result.get('data', [])
                if data:
                    self.populate_table(data)
                    QMessageBox.information(
                        self.view, 
                        "สำเร็จ", 
                        f"พบรายการทั้งหมด {len(data)} รายการในวันนี้"
                    )
                else:
                    self.view.ui.result_table.setRowCount(0)
                    QMessageBox.information(
                        self.view, 
                        "แจ้งเตือน", 
                        "ไม่พบรายการในวันนี้"
                    )
            else:
                error_msg = result.get('detail', 'ไม่สามารถค้นหาข้อมูลได้') if result else 'ไม่ได้รับการตอบกลับจาก API'
                QMessageBox.warning(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {error_msg}")
                
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
            print(f"Error in search_to_day_orders: {e}")


    def search_orders(self):
        barcode = self.view.get_search_text()
        
        if not barcode:
            QMessageBox.warning(
                self.view, 
                "แจ้งเตือน", 
                "กรุณากรอกหมายเลข barcode ที่ต้องการค้นหา"
            )
            return
        
        try:
            result = self.API_lab_order.search_by_barcode(barcode)
            
            if result and result.get('status') == 'success':
                data = result.get('data', [])
                if data:
                    self.populate_table(data)
                    QMessageBox.information(
                        self.view, 
                        "สำเร็จ", 
                        f"พบรายการทั้งหมด {len(data)} รายการ"
                    )
                else:
                    self.view.ui.result_table.setRowCount(0)
                    QMessageBox.information(
                        self.view, 
                        "แจ้งเตือน", 
                        f"ไม่พบรายการที่มี barcode: {barcode}"
                    )
            else:
                error_msg = result.get('detail', 'ไม่สามารถค้นหาข้อมูลได้') if result else 'ไม่ได้รับการตอบกลับจาก API'
                QMessageBox.warning(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {error_msg}")
                
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
            print(f"Error in search_orders: {e}")


    def print_lab_orders(self):
        table = self.view.ui.result_table
        selected_rows = table.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.warning(
                self.view, 
                "แจ้งเตือน", 
                "กรุณาเลือกรายการที่ต้องการพิมพ์ใบส่งแลป"
            )
            return
        
        try:
            row = selected_rows[0].row()
            order_id_str = table.item(row, 1).text().strip()
            order_id = int(order_id_str) if order_id_str else 0
            
            if order_id == 0:
                QMessageBox.warning(self.view, "ข้อผิดพลาด", "ไม่พบหมายเลขการตรวจ")
                return
            
            lab_room = table.item(row, 3).text().strip()
            from SERVICES_REGISTER.work_service import WorkService
            work_service = WorkService()
            result = work_service.get_lab_order_pdf_data(order_id)
            
            if not result or result.get('status') != 'success':
                QMessageBox.critical(self.view, "ข้อผิดพลาด", f"ไม่สามารถดึงข้อมูลได้\n{result}")
                return
            
            lab_type = result.get('lab_type')
            sample_detail = result.get('sample_detail')
            test_data = result.get('test_data')
            
            if not sample_detail:
                QMessageBox.warning(self.view, "แจ้งเตือน", 
                    f"ไม่พบข้อมูล sample สำหรับสร้าง PDF")
                return
            if not test_data:
                print("WARNING: test_data is empty, will create PDF with empty test data")
                test_data = []
            
            project_root = os.path.dirname(os.path.dirname(__file__))
            pdf_from_path = os.path.join(project_root, "Order_Lab_Pdf", "pdf_from")
            if pdf_from_path not in sys.path:
                sys.path.insert(0, pdf_from_path)
            
            output_dir = os.path.join(project_root, "Order_Lab_Pdf", "pdf_from", "output")
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(output_dir, f"{lab_type}_order_{order_id}_{timestamp}.pdf")
            
            if lab_type == "parasite":
                parasite_order_from.create_parasite_biology(sample_detail, test_data, output_file)
                
            elif lab_type == "bacteria":
                bacteria_order_from.create_bacteriology(sample_detail, test_data, output_file)
                
            elif lab_type == "molecular":
                molecular_order_from.create_molecular_biology(sample_detail, test_data, output_file)
            else:
                QMessageBox.warning(self.view, "แจ้งเตือน", f"ไม่รองรับประเภทห้องปฏิบัติการ: {lab_type}")
                return
            
            if os.path.exists(output_file):
                if platform.system() == 'Windows':
                    os.startfile(output_file)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.call(['open', output_file])
                else:  # Linux
                    subprocess.call(['xdg-open', output_file])
                
                QMessageBox.information(self.view, "สำเร็จ", f"สร้างใบส่งแลป {lab_type} สำเร็จ")
            else:
                QMessageBox.warning(self.view, "ข้อผิดพลาด", "ไม่สามารถสร้างไฟล์ PDF ได้")
                
        except ValueError as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"รูปแบบข้อมูลไม่ถูกต้อง: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
            print(f"Error in print_lab_orders: {e}")

    def populate_table(self, data):
        table = self.view.ui.result_table
        table.setRowCount(0)
        
        if not data:
            return
        
        for row_data in data:
            try:
                row_position = table.rowCount()
                table.insertRow(row_position)
                dtime = str(row_data[0]) if row_data[0] else ""
                if 'T' in dtime:
                    dtime = dtime.replace('T', ' ')
                order_id_raw = str(row_data[1]) if row_data[1] else ""
                order_id = order_id_raw.zfill(12) if order_id_raw else ""
                species = str(row_data[2]) if row_data[2] else ""
                room_code = str(row_data[3]) if row_data[3] else ""
                room_nickname = str(row_data[4]) if row_data[4] else ""
                
                if room_code and room_nickname:
                    lab_room = f"{room_code} ({room_nickname})"
                elif room_code:
                    lab_room = room_code
                elif room_nickname:
                    lab_room = room_nickname
                else:
                    lab_room = ""
                keep_method = str(row_data[5]) if row_data[5] else ""
                speed = str(row_data[6]) if row_data[6] else ""
                additional = str(row_data[7]) if len(row_data) > 7 and row_data[7] else ""
                items = [
                    QTableWidgetItem(dtime),
                    QTableWidgetItem(order_id),
                    QTableWidgetItem(species),
                    QTableWidgetItem(lab_room),
                    QTableWidgetItem(keep_method),
                    QTableWidgetItem(speed),
                    QTableWidgetItem(additional)
                ]
                for col, item in enumerate(items):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row_position, col, item)
                    
            except Exception as e:
                print(f"Error adding row to table: {e}")
                continue