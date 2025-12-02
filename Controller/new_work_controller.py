from PySide6.QtCore import QObject,QStringListModel, Qt, QTimer, Slot
from PySide6.QtWidgets import (QCompleter, QMessageBox)
import mariadb
from API.client_app import APIApp
from View.view_new_work_frame import AddNewWorkWidget


class NewWorkController(QObject):
    def __init__(self, new_work_widget = None, main_window = None, main_controller = None):
        super().__init__()
        if new_work_widget is None:
            self.main_nw = AddNewWorkWidget()
        else:
            self.main_nw = new_work_widget
        self.main_window = main_window
        self.main_controller = main_controller
        self.API_new_work = APIApp()

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
        
    @Slot()
        
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
        self.cancel_clicked()


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
        self.main_nw.unlock_all_input()

    def setup_ui(self):
        self.cancel_clicked()

    def add_result_clicked(self):
        case_id = self.main_nw.ui.nw_id_lineEdit.text()
        if self.main_window and hasattr(self.main_window, 'specimen_widget'):
            if hasattr(self.main_window, 'specimen_controller'):
                self.main_window.specimen_controller.set_case_registration_id(case_id)
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.specimen_widget)
        else:
            print("Warning: main_window or specimen_widget not available")
            

    def delete_result_clicked(self):
        print("Delete result button clicked")
        pass
    
    def print_sticker_clicked(self):
        print("Print sticker button clicked")
        pass

    def send_report_clicked(self):
        print("Send report button clicked")
        pass

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
            sender_results = self.API_new_work.fetch_search_results(text)
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
            
            print(f"✓ Selected SENDER - ID: {self.selected_sender_id}, Name: {name} {surname}, Tax ID: {tax_id}")
        
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
            owner_results = self.API_new_work.fetch_search_results(text)
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
            
            print(f"✓ Selected OWNER - ID: {self.selected_owner_id}, Name: {name} {surname}, Tax ID: {tax_id}")
        
        try:
            self.owner_completer.popup().hide()
        except Exception:
            pass
        
        self.main_nw.ui.nw_name_owner_lineEdit.clearFocus()
        
        # Use QTimer to delay resetting the flags to avoid race conditions with delayed signals
        QTimer.singleShot(100, lambda: setattr(self, 'is_selecting_owner', False))
        QTimer.singleShot(500, lambda: setattr(self, 'lock_owner_id', False))  # Keep locked for 500ms

