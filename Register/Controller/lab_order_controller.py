import os
import sys
import tempfile
from datetime import datetime
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox
from PySide6.QtCore import QObject, Qt
from Order_Lab_Pdf.pdf_from import parasite_order_from
from Order_Lab_Pdf.pdf_from import bacteria_order_from
from Order_Lab_Pdf.pdf_from import molecular_order_from
from SERVICES_REGISTER.lab_order_service import LabOrderService
from SERVICES_REGISTER.work_service import WorkService
import subprocess
import platform

class LabReportPageController(QObject):
    def __init__(self, model, view, main_window=None):
        super().__init__()
        self.model = model
        self.view = view # LabReportPageWidget
        self.main_window = main_window # Store reference just in case
        self.API_lab_order = LabOrderService()
        self.work_api = WorkService()  # Add WorkService for state changes
        
        # Pagination state
        self.current_offset = 0
        self.limit = 100
        self.has_more = True
        self.is_loading = False
        self.total_count = 0
        self.lab_order_data = []  # Store all loaded data
        self.current_search_type = None  # 'today', 'barcode'
        self.current_search_params = {}  # Store search parameters for pagination
        
        self.event_bindings()

    def event_bindings(self):
        self.view.ui.search_button.clicked.connect(self.search_orders)
        self.view.ui.print_button.clicked.connect(self.print_lab_orders)
        self.view.ui.search_to_day_button.clicked.connect(self.search_to_day_orders)
        
        # Bind scroll event for pagination
        self.view.ui.result_table.verticalScrollBar().valueChanged.connect(self.on_scroll)


    def search_to_day_orders(self):
        """ค้นหารายการในวันนี้ พร้อม Pagination"""
        # Reset pagination state
        self.current_offset = 0
        self.lab_order_data = []
        self.has_more = True
        self.current_search_type = 'today'
        self.current_search_params = {}
        
        self.view.ui.result_table.setRowCount(0)
        self.load_more_data()


    def search_orders(self):
        """ค้นหารายการตาม barcode พร้อม Pagination"""
        barcode = self.view.get_search_text()
        
        if not barcode:
            QMessageBox.warning(
                self.view, 
                "แจ้งเตือน", 
                "กรุณากรอกหมายเลข barcode ที่ต้องการค้นหา"
            )
            return
        
        # Reset pagination state
        self.current_offset = 0
        self.lab_order_data = []
        self.has_more = True
        self.current_search_type = 'barcode'
        self.current_search_params = {'barcode': barcode}
        
        self.view.ui.result_table.setRowCount(0)
        self.load_more_data()

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
            
            result = self.work_api.get_lab_order_pdf_data(order_id)
            
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
                # Update state to "2" (printed lab form) after successful PDF creation
                try:
                    state_result = self.work_api.change_state_work(order_id, 2)
                    if state_result and state_result.get('status') == 'success':
                        # print(f"State updated to '2' (printed lab form) for order_id: {order_id}")
                        pass
                    else:
                        print(f"Failed to update state for order_id {order_id}: {state_result}")
                except Exception as e:
                    print(f"Error updating state: {e}")
                
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

    def load_more_data(self):
        """โหลดข้อมูลเพิ่มเติมตามประเภทการค้นหา"""
        if self.is_loading or not self.has_more:
            return
        
        self.is_loading = True
        
        try:
            response_data = None
            
            if self.current_search_type == 'today':
                response_data = self.API_lab_order.search_today_orders(
                    offset=self.current_offset,
                    limit=self.limit
                )
            elif self.current_search_type == 'barcode':
                response_data = self.API_lab_order.search_by_barcode(
                    barcode=self.current_search_params.get('barcode'),
                    offset=self.current_offset,
                    limit=self.limit
                )
            
            if not response_data or response_data.get('status') != 'success':
                if self.current_offset == 0:
                    QMessageBox.information(self.view, "Info", "ไม่พบข้อมูล (No data found)")
                self.has_more = False
                return
            
            # Handle response format
            new_data = response_data.get('data', [])
            self.total_count = response_data.get('total', 0)
            self.has_more = response_data.get('has_more', False)
            
            if len(new_data) == 0:
                if self.current_offset == 0:
                    QMessageBox.information(self.view, "Info", "ไม่พบข้อมูล (No data found)")
                self.has_more = False
                return
            
            # Add new data to existing data
            self.lab_order_data.extend(new_data)
            self.update_table()
            self.current_offset += len(new_data)
            
        except Exception as e:
            print(f"[ERROR] Exception in load_more_data: {e}")
            import traceback
            traceback.print_exc()
            if self.current_offset == 0:
                QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
            self.has_more = False
        finally:
            self.is_loading = False
    
    def on_scroll(self, value):
        """ตรวจจับการเลื่อน scroll bar"""
        scrollbar = self.view.ui.result_table.verticalScrollBar()
        # When scroll reaches 90% of maximum, load more data
        if value >= scrollbar.maximum() * 0.9:
            if self.has_more and not self.is_loading and len(self.lab_order_data) > 0:
                self.load_more_data()
    
    def update_table(self):
        """อัพเดตตารางด้วยข้อมูลทั้งหมด"""
        table = self.view.ui.result_table
        table.setRowCount(len(self.lab_order_data))
        
        for row_idx, row_data in enumerate(self.lab_order_data):
            try:
                # 0. Date/Time
                dtime = str(row_data[0]) if row_data[0] else ""
                if 'T' in dtime:
                    dtime = dtime.replace('T', ' ')
                
                # 1. Order ID (Barcode)
                order_id_raw = str(row_data[1]) if row_data[1] else ""
                order_id = order_id_raw.zfill(12) if order_id_raw else ""
                
                # 2. Species
                species = str(row_data[2]) if row_data[2] else ""
                
                # 3. Lab Room (Code + Nickname)
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
                
                # 4. Keep Method (Storage)
                keep_method = str(row_data[5]) if row_data[5] else ""
                
                # 5. Speed (Urgency)
                speed = str(row_data[6]) if row_data[6] else ""
                
                # 6. Additional Info (Sample Name)
                # additional = str(row_data[7]) if len(row_data) > 7 and row_data[7] else ""
                additional = ""
                
                # Create items
                items = [
                    QTableWidgetItem(dtime),
                    QTableWidgetItem(order_id),
                    QTableWidgetItem(species),
                    QTableWidgetItem(lab_room),
                    QTableWidgetItem(keep_method),
                    QTableWidgetItem(speed),
                    QTableWidgetItem(additional)
                ]
                
                # Set items in table
                for col, item in enumerate(items):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row_idx, col, item)
                    
            except Exception as e:
                print(f"Error adding row {row_idx} to table: {e}")
                continue