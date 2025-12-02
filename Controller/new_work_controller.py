from PySide6.QtCore import QObject,QStringListModel, Qt, QTimer, Slot
from PySide6.QtWidgets import (QCompleter, QMessageBox)
import mariadb
from API.client_app import APIApp
from View.view_new_work_frame import AddNewWorkWidget


class NewWorkController(QObject):
    def __init__(self, new_work_widget = None, main_window = None):
        super().__init__()
        if new_work_widget is None:
            self.main_nw = AddNewWorkWidget()
        else:
            self.main_nw = new_work_widget
        self.main_window = main_window
        self.api_search_app = APIApp()

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

        # --- Initialize selected IDs ---
        self.selected_sender_id = None
        self.selected_owner_id = None
        
        
        self.main_nw.ui.nw_save_pushButton.clicked.connect(self.save_clicked)
        self.main_nw.ui.nw_cancel_pushButton.clicked.connect(self.cancel_clicked)
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
            max_id = self.api_search_app.get_max_sample_id()
            if max_id is not None:
                new_id = max_id + 1
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
                reply = QMessageBox.question(self.main_nw, "CONFIRMATION", "คุณแน่ใจหรือไม่ว่าจะไม่ใส่ชื่อโครงการ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:
                    return
            self.update_id_sample()
            self.main_nw.lock_all_input()
            
            # --- ที่นี่ คุณสามารถเข้าถึง ID ของผู้ส่งและเจ้าของได้ ---
            print(f"กำลังบันทึกข้อมูล...")
            print(f"Sender ID: {self.selected_sender_id}")
            print(f"Owner ID: {self.selected_owner_id}")
            # คุณสามารถนำ self.selected_sender_id และ self.selected_owner_id
            # ไปใช้ในการสร้าง API request เพื่อบันทึกข้อมูลลง database ต่อไป

            QMessageBox.information(self.main_nw, "SUCCESS", "บันทึกข้อมูลเรียบร้อย")
            
        else:
            QMessageBox.warning(self.main_nw, "DATA ERROR", "กรุณากรอกข้อมูลให้ครบถ้วน")
            print("Data is invalid, cannot save.")

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
        self.main_nw.unlock_all_input()

    def setup_ui(self):
        self.cancel_clicked()

    def add_result_clicked(self):
        # print("Add result button clicked")
        
        # Get the case registration ID
        case_id = self.main_nw.ui.nw_id_lineEdit.text()
        
        # Navigate to Specimen Page and pass case_registration_id
        if self.main_window and hasattr(self.main_window, 'specimen_widget'):
            # Pass the case_registration_id to specimen controller
            if hasattr(self.main_window, 'specimen_controller'):
                self.main_window.specimen_controller.set_case_registration_id(case_id)
            
            # Switch to specimen page
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
        if user_type == 'sender' and not self.is_selecting_sender:
            if self.selected_sender_id is not None:
                self.selected_sender_id = None
        elif user_type == 'owner' and not self.is_selecting_owner:
            if self.selected_owner_id is not None:
                self.selected_owner_id = None
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
            sender_results = self.api_search_app.fetch_search_results(text)
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
        records = self.sender_records_map.get(text, []) if hasattr(self, 'sender_records_map') else []
        if records:
            r = records[0]
            self.main_nw.ui.nw_name_sender_lineEdit.setText(r.get('name',''))
            self.main_nw.ui.nw_sure_name_sender_lineEdit.setText(r.get('surname',''))
            self.main_nw.ui.nw_tex_id_sender_lineEdit.setText(r.get('tax_id',''))
            self.selected_sender_id = r.get('id')
            # print(f"Selected sender - Name: {r.get('name','')}, Surname: {r.get('surname','')}, ID: {self.selected_sender_id}")
        
        try:
            self.sender_completer.popup().hide()
        except Exception:
            pass
        self.main_nw.ui.nw_name_sender_lineEdit.clearFocus()
        self.is_selecting_sender = False

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
            owner_results = self.api_search_app.fetch_search_results(text)
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
        records = self.owner_records_map.get(text, []) if hasattr(self, 'owner_records_map') else []
        if records:
            r = records[0]
            self.main_nw.ui.nw_name_owner_lineEdit.setText(r.get('name',''))
            self.main_nw.ui.nw_sure_name_owner_lineEdit.setText(r.get('surname',''))
            self.main_nw.ui.nw_tex_id_owner_lineEdit.setText(r.get('tax_id',''))
            self.selected_owner_id = r.get('id')
            # print(f"Selected owner - Name: {r.get('name','')}, Surname: {r.get('surname','')}, ID: {self.selected_owner_id}")
        try:
            self.owner_completer.popup().hide()
        except Exception:
            pass
        self.main_nw.ui.nw_name_owner_lineEdit.clearFocus()
        self.is_selecting_owner = False
