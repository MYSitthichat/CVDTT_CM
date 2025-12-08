from PySide6.QtCore import QObject,QStringListModel, Qt, QTimer, Slot
from PySide6.QtWidgets import (QCompleter, QMessageBox, QTreeWidgetItem)
from View.view_new_work_frame import AddNewWorkWidget
from SERVICES_REGISTER.work_service import WorkService
from SERVICES_REGISTER.customer_service import CustomerService
from barcode_utils.barcode_generator import BarcodeGenerator


class NewWorkController(QObject):
    def __init__(self, new_work_widget = None, main_window = None, main_controller = None):
        super().__init__()
        if new_work_widget is None:
            self.main_nw = AddNewWorkWidget()
        else:
            self.main_nw = new_work_widget
        self.main_window = main_window
        self.main_controller = main_controller
        self.API_new_work = WorkService()
        self.API_customer = CustomerService()

        self.last_sender_search_text = ""
        self.sender_search_timer = QTimer(self)
        self.sender_search_timer.setSingleShot(True)
        self.sender_search_timer.timeout.connect(self.perform_search_sender)
        self.sender_search_delay = 350
        self.sender_completer = QCompleter()
        self.sender_model = QStringListModel()
        self.sender_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.sender_completer.setFilterMode(Qt.MatchContains)
        self.sender_completer.setModel(self.sender_model)
        self.sender_completer.activated.connect(self.on_item_selected_sender)

        self.last_owner_search_text = ""
        self.owner_search_timer = QTimer(self)
        self.owner_search_timer.setSingleShot(True)
        self.owner_search_timer.timeout.connect(self.perform_search_owner)
        self.owner_search_delay = 350

        self.owner_completer = QCompleter()
        self.owner_model = QStringListModel()
        self.owner_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.owner_completer.setFilterMode(Qt.MatchContains)
        self.owner_completer.setModel(self.owner_model)
        self.owner_completer.activated.connect(self.on_item_selected_owner)
        
        self.main_nw.ui.nw_name_sender_lineEdit.setCompleter(self.sender_completer)
        self.main_nw.ui.nw_name_sender_lineEdit.textChanged.connect(self.update_search_results_sender)

        self.main_nw.ui.nw_name_owner_lineEdit.setCompleter(self.owner_completer)
        self.main_nw.ui.nw_name_owner_lineEdit.textChanged.connect(self.update_search_results_owner)
        
        self.is_selecting_sender = False
        self.is_selecting_owner = False
        
        # --- Lock flags to prevent clearing ID right after selection ---
        self.lock_sender_id = False
        self.lock_owner_id = False

        # --- Initialize selected IDs ---
        self.selected_sender_id = None
        self.selected_owner_id = None
        
        self.main_nw.ui.nw_save_pushButton.clicked.connect(self.save_clicked)
        self.main_nw.ui.nw_cancel_pushButton.clicked.connect(self.cancel_clicked_button)
        self.main_nw.ui.nw_add_result_pushButton.clicked.connect(self.add_result_clicked)
        self.main_nw.ui.new_delete_result_pushButton.clicked.connect(self.delete_result_clicked)
        self.main_nw.ui.nw_print_bracode_pushButton.clicked.connect(self.print_sticker_clicked)
        self.main_nw.ui.nw_print_sned_lab_pushButton.clicked.connect(self.send_report_clicked)

        # --- Connect signals to clear IDs on manual edit ---
        self.main_nw.ui.nw_sure_name_sender_lineEdit.textChanged.connect(lambda: self.clear_selected_id('sender'))
        self.main_nw.ui.nw_tex_id_sender_lineEdit.textChanged.connect(lambda: self.clear_selected_id('sender'))
        self.main_nw.ui.nw_sure_name_owner_lineEdit.textChanged.connect(lambda: self.clear_selected_id('owner'))
        self.main_nw.ui.nw_tex_id_owner_lineEdit.textChanged.connect(lambda: self.clear_selected_id('owner'))
            
        checkbox = self.main_nw.ui.nw_owner_same_sender_checkBox
        checkbox.stateChanged.connect(self.on_owner_same_as_sender_changed)
        self.is_printing = False
        
        
    
    
    
    def send_report_clicked(self):
        print("Send report button clicked")
    
    
    
    
    
    
    
    
    
    
    
    def delete_result_clicked(self):
        """Delete selected item from tree widget and database"""
        tree = self.main_nw.ui.nw_work_register_treeWidget
        selected_items = tree.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self.main_nw, "เตือน", "กรุณาเลือกรายการที่ต้องการลบ")
            return
        order_id = selected_items[0].text(1).lstrip('0') or '0'
        
        reply = QMessageBox.question(
            self.main_nw,
            "ยืนยันการลบ",
            f"คุณต้องการลบรายการหมายเลข {order_id} หรือไม่?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        try:
            result = self.API_new_work.delete_sample_registration(order_id)
            
            if result and result.get('status') == 'success':
                QMessageBox.information(self.main_nw, "สำเร็จ", "ลบข้อมูลเรียบร้อยแล้ว")
                self.update_treewidget_data()
            else:
                error_detail = result.get('detail', 'ไม่ทราบสาเหตุ') if result else 'ไม่ได้รับการตอบกลับจาก API'
                QMessageBox.warning(self.main_nw, "ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการลบข้อมูล\n{error_detail}")
                print(f"Error result: {result}")
                
        except Exception as e:
            QMessageBox.critical(self.main_nw, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
            print(f"Exception in delete_result_clicked: {e}")
    
    def print_sticker_clicked(self):
        if self.is_printing:
            return
        self.is_printing = True
        try:
            tree = self.main_nw.ui.nw_work_register_treeWidget
            selected_items = tree.selectedItems()
            
            if not selected_items:
                QMessageBox.critical(self.main_nw, "Error", "กรุณาเลือกรายการในตารางเพื่อพิมพ์สติกเกอร์")
                return
            item = selected_items[0]
            row_data = []
            for col in range(6): 
                text = item.text(col)
                row_data.append(text)
            data_to_print = [row_data]

            try:
                barcode_obj = BarcodeGenerator()
                barcode_obj.generate(data_to_print)
                barcode_obj.print_barcode()
            except Exception as e:
                QMessageBox.critical(self.main_nw, "Error", f"เกิดข้อผิดพลาดในการพิมพ์: {str(e)}")
                
        except Exception as e:
            print(f"Print Error: {e}")
        finally:
            self.is_printing = False
    
    @Slot(int)
    def on_owner_same_as_sender_changed(self, state):
        if state == Qt.Checked or state == 2:
            sender_name = self.main_nw.ui.nw_name_sender_lineEdit.text()
            sender_surname = self.main_nw.ui.nw_sure_name_sender_lineEdit.text()
            sender_tax_id = self.main_nw.ui.nw_tex_id_sender_lineEdit.text()
            self.main_nw.ui.nw_name_owner_lineEdit.setText(sender_name)
            self.main_nw.ui.nw_sure_name_owner_lineEdit.setText(sender_surname)
            self.main_nw.ui.nw_tex_id_owner_lineEdit.setText(sender_tax_id)
            self.selected_owner_id = self.selected_sender_id
        else:
            self.main_nw.ui.nw_sure_name_owner_lineEdit.clear()
            self.main_nw.ui.nw_tex_id_owner_lineEdit.clear()
            self.main_nw.ui.nw_name_owner_lineEdit.clear()
            self.selected_owner_id = None


    def update_id_sample(self):
        try:
            max_id = self.API_new_work.get_max_sample_id()
            if max_id is not None:
                new_id = max_id
                self.main_nw.ui.nw_id_lineEdit.setText(str(new_id))
            else:
                QMessageBox.warning(self.main_nw, "API Error", "ไม่สามารถดึงเลขที่งานล่าสุดได้")
                self.main_nw.ui.nw_id_lineEdit.setText("1") 
        except Exception as e:
            print(f"Error updating sample ID: {e}")
            QMessageBox.warning(self.main_nw, "Error", f"เกิดข้อผิดพลาดในการอัปเดตเลขที่งาน: {e}")
            

    def save_clicked(self):
        if self.main_nw.check_data_input() == True:
            if self.main_nw.check_project_name_input() == False:
                reply = QMessageBox.question(
                    self.main_nw, 
                    "CONFIRMATION", 
                    "คุณแน่ใจหรือไม่ว่าจะไม่ใส่ชื่อโครงการ?", 
                    QMessageBox.Yes | QMessageBox.No, 
                    QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
            
            # Lock input fields
            self.main_nw.lock_all_input()
            
            # Get user ID
            user_id = None
            if self.main_controller:
                user_id = self.main_controller.get_user_login_id()
            elif self.main_window and hasattr(self.main_window, 'get_user_login_id'):
                user_id = self.main_window.get_user_login_id()
            
            # Get project name (ensure it's not None)
            project_name = self.main_nw.ui.nw_project_name_lineEdit.text().strip()
            if not project_name:
                project_name = ""  # Convert None/empty to empty string
            # Validate sender and owner IDs
            if self.selected_sender_id is None:
                QMessageBox.warning(
                    self.main_nw,
                    "ERROR",
                    "กรุณาเลือกผู้ส่งตัวอย่าง"
                )
                self.main_nw.unlock_all_input()
                return
            
            if self.selected_owner_id is None:
                QMessageBox.warning(
                    self.main_nw,
                    "ERROR",
                    "กรุณาเลือกเจ้าของสัตว์"
                )
                self.main_nw.unlock_all_input()
                return
            
            # Call API
            save_result = self.API_new_work.add_new_work(
                self.selected_sender_id,
                self.selected_owner_id,
                project_name,
                user_id
            )

            if save_result and isinstance(save_result, dict):
                if save_result.get('status') == 'success':
                    work_id = save_result.get('work_id')
                    self.update_id_sample()
                    QMessageBox.information(
                        self.main_nw, 
                        "SUCCESS", 
                        f"บันทึกข้อมูลเรียบร้อย\nเลขที่งาน: {work_id}"
                    )
                else:
                    error_msg = save_result.get('detail', 'Unknown error')
                    QMessageBox.warning(
                        self.main_nw, 
                        "ERROR", 
                        f"บันทึกข้อมูลไม่สำเร็จ\n{error_msg}"
                    )
                    self.main_nw.unlock_all_input()
            else:
                QMessageBox.warning(
                    self.main_nw, 
                    "ERROR", 
                    "ไม่สามารถบันทึกข้อมูลได้ กรุณาลองใหม่อีกครั้ง"
                )
                self.main_nw.unlock_all_input()
        else:
            QMessageBox.warning(self.main_nw, "DATA ERROR", "กรุณากรอกข้อมูลให้ครบถ้วน")

    def cancel_clicked_button(self):
        reply = QMessageBox.question(self.main_nw, "CONFIRMATION", "คุณแน่ใจหรือไม่ว่ายกเลิกการบันทึกข้อมูล?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        # self.cancel_clicked() #comment for debug 


    def cancel_clicked(self):
        self.main_nw.ui.nw_name_sender_lineEdit.clear()
        self.main_nw.ui.nw_sure_name_sender_lineEdit.clear()
        self.main_nw.ui.nw_tex_id_sender_lineEdit.clear()
        self.main_nw.ui.nw_name_owner_lineEdit.clear()
        self.main_nw.ui.nw_sure_name_owner_lineEdit.clear()
        self.main_nw.ui.nw_tex_id_owner_lineEdit.clear()
        self.main_nw.ui.nw_project_name_lineEdit.clear()
        self.main_nw.ui.nw_id_lineEdit.clear()
        self.main_nw.ui.nw_id_lineEdit.setReadOnly(True)
        self.main_nw.ui.nw_owner_same_sender_checkBox.setChecked(False)
        self.selected_sender_id = None
        self.selected_owner_id = None
        self.lock_sender_id = False
        self.lock_owner_id = False
        self.main_nw.ui.nw_work_register_treeWidget.clear()
        self.main_nw.unlock_all_input()

    def setup_ui(self):
        # self.cancel_clicked() #comment for debug 
        pass

    def add_result_clicked(self):
        case_id = self.main_nw.ui.nw_id_lineEdit.text()
        if self.main_window and hasattr(self.main_window, 'specimen_widget'):
            if hasattr(self.main_window, 'specimen_controller'):
                self.main_window.specimen_controller.set_case_registration_id(case_id)
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.specimen_widget)
            
        else:
            print("Warning: main_window or specimen_widget not available")
            

# SENDER SEARCH
    def clear_selected_id(self, user_type):
        if user_type == 'sender':
            if self.lock_sender_id or self.is_selecting_sender:
                return
        elif user_type == 'owner':
            if self.lock_owner_id or self.is_selecting_owner:
                return
            
    def update_search_results_sender(self, text):
        if self.is_selecting_sender:
            return
        self.last_sender_search_text = text
        self.sender_search_timer.start(self.sender_search_delay)

    def perform_search_sender(self):
        text = self.last_sender_search_text.strip()
        if len(text) < 2:
            self.sender_model.setStringList([])
            return
        try:
            sender_results = self.API_customer.search_customer(text)
            if not sender_results:
                self.sender_model.setStringList([])
                return

            names = [f"{r.get('name','').strip()} {r.get('surname','').strip()}" for r in sender_results]
            self.sender_records_map = {}
            for r, name in zip(sender_results, names):
                self.sender_records_map.setdefault(name, []).append(r)

            self.sender_model.setStringList(names)
            if sender_results:
                self.sender_completer.complete()
        except Exception as e:
            print(f"Sender Search Error: {e}")
            self.sender_model.setStringList([])

    def on_item_selected_sender(self, text):
        self.is_selecting_sender = True
        self.lock_sender_id = True  # Lock to prevent clearing
        
        records = self.sender_records_map.get(text, []) if hasattr(self, 'sender_records_map') else []
        if records:
            r = records[0]
            
            # Get values with default "-" for empty fields
            name = r.get('name', '').strip() or '-'
            surname = r.get('surname', '').strip() or '-'
            tax_id = r.get('tax_id', '').strip() or '-'
            
            # Block signals temporarily to prevent clearing ID
            self.main_nw.ui.nw_name_sender_lineEdit.blockSignals(True)
            self.main_nw.ui.nw_sure_name_sender_lineEdit.blockSignals(True)
            self.main_nw.ui.nw_tex_id_sender_lineEdit.blockSignals(True)
            
            # Set values
            self.main_nw.ui.nw_name_sender_lineEdit.setText(name)
            self.main_nw.ui.nw_sure_name_sender_lineEdit.setText(surname)
            self.main_nw.ui.nw_tex_id_sender_lineEdit.setText(tax_id)
            self.selected_sender_id = r.get('id')
            
            # Unblock signals
            self.main_nw.ui.nw_name_sender_lineEdit.blockSignals(False)
            self.main_nw.ui.nw_sure_name_sender_lineEdit.blockSignals(False)
            self.main_nw.ui.nw_tex_id_sender_lineEdit.blockSignals(False)
        
        try:
            self.sender_completer.popup().hide()
        except Exception:
            pass
        
        self.main_nw.ui.nw_name_sender_lineEdit.clearFocus()
        
        # Use QTimer to delay resetting the flags to avoid race conditions with delayed signals
        QTimer.singleShot(100, lambda: setattr(self, 'is_selecting_sender', False))
        QTimer.singleShot(500, lambda: setattr(self, 'lock_sender_id', False))  # Keep locked for 500ms

# OWNER SEARCH
    def update_search_results_owner(self, text):
        if self.is_selecting_owner:
            return
        self.last_owner_search_text = text
        self.owner_search_timer.start(self.owner_search_delay)

    def perform_search_owner(self):
        text = self.last_owner_search_text.strip()
        if len(text) < 2:
            self.owner_model.setStringList([])
            return
        try:
            owner_results = self.API_customer.search_customer(text)
            if not owner_results:
                self.owner_model.setStringList([])
                return
            names = [f"{r.get('name','').strip()} {r.get('surname','').strip()}" for r in owner_results]
            self.owner_records_map = {}
            for r, name in zip(owner_results, names):
                self.owner_records_map.setdefault(name, []).append(r)

            self.owner_model.setStringList(names)
            if owner_results:
                self.owner_completer.complete()
        except Exception as e:
            print(f"Owner Search Error: {e}")
            self.owner_model.setStringList([])

    def on_item_selected_owner(self, text):
        self.is_selecting_owner = True
        self.lock_owner_id = True  # Lock to prevent clearing
        
        records = self.owner_records_map.get(text, []) if hasattr(self, 'owner_records_map') else []
        if records:
            r = records[0]
            
            # Get values with default "-" for empty fields
            name = r.get('name', '').strip() or '-'
            surname = r.get('surname', '').strip() or '-'
            tax_id = r.get('tax_id', '').strip() or '-'
            
            # Block signals temporarily to prevent clearing ID
            self.main_nw.ui.nw_name_owner_lineEdit.blockSignals(True)
            self.main_nw.ui.nw_sure_name_owner_lineEdit.blockSignals(True)
            self.main_nw.ui.nw_tex_id_owner_lineEdit.blockSignals(True)
            
            # Set values
            self.main_nw.ui.nw_name_owner_lineEdit.setText(name)
            self.main_nw.ui.nw_sure_name_owner_lineEdit.setText(surname)
            self.main_nw.ui.nw_tex_id_owner_lineEdit.setText(tax_id)
            self.selected_owner_id = r.get('id')
            
            # Unblock signals
            self.main_nw.ui.nw_name_owner_lineEdit.blockSignals(False)
            self.main_nw.ui.nw_sure_name_owner_lineEdit.blockSignals(False)
            self.main_nw.ui.nw_tex_id_owner_lineEdit.blockSignals(False)
            
        
        try:
            self.owner_completer.popup().hide()
        except Exception:
            pass
        
        self.main_nw.ui.nw_name_owner_lineEdit.clearFocus()
        
        # Use QTimer to delay resetting the flags to avoid race conditions with delayed signals
        QTimer.singleShot(100, lambda: setattr(self, 'is_selecting_owner', False))
        QTimer.singleShot(500, lambda: setattr(self, 'lock_owner_id', False))  # Keep locked for 500ms

# UPDATE DATA TO TREEWIDGET
    def update_treewidget_data(self):
        case_id = self.main_nw.ui.nw_id_lineEdit.text().strip()
        if not case_id:
            return
        result = self.API_new_work.get_case_details(case_id)
        
        if result and result.get('status') == 'success':
            data = result.get('data', [])
            self.populate_treewidget(data)
        else:
            print(f"Failed to get case details: {result}")
    
    def populate_treewidget(self, data):
        self.main_nw.ui.nw_work_register_treeWidget.clear()
        
        if not data:
            return
        for row in data:
            try:
                dtime = str(row[0]) if row[0] else ""
                if 'T' in dtime:
                    dtime = dtime.replace('T', ' ')
                # --------------------------------
                
                order_id_raw = str(row[1]) if row[1] else ""
                species = str(row[2]) if row[2] else ""
                room_code = str(row[3]) if row[3] else ""
                room_nickname = str(row[4]) if row[4] else ""
                keep_method = str(row[5]) if row[5] else ""
                speed = str(row[6]) if row[6] else ""
                
                if order_id_raw:
                    order_id = order_id_raw.zfill(12)
                else:
                    order_id = ""
                
                if room_code and room_nickname:
                    lab_room = f"{room_code} ({room_nickname})"
                elif room_code:
                    lab_room = room_code
                elif room_nickname:
                    lab_room = room_nickname
                else:
                    lab_room = ""
                
                item = QTreeWidgetItem([
                    dtime,           # วันที่รับเคส (แก้ไขแล้ว ไม่มี T)
                    order_id,        # หมายเลขการตรวจ
                    species,         # ชนิดสัตว์
                    lab_room,        # ห้องปฏิบัติการ
                    keep_method,     # การเก็บรักษา
                    speed,           # ระดับความด่วน
                    ""               # ข้อมูลเพิ่มเติม
                ])
                
                for col in range(7):
                    item.setTextAlignment(col, Qt.AlignmentFlag.AlignCenter)
                
                self.main_nw.ui.nw_work_register_treeWidget.addTopLevelItem(item)
                
            except Exception as e:
                print(f"⚠️ Error adding row to treewidget: {e}")
                print(f"   Row data: {row}")
