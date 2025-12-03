from View.view_specimen_frame import SpecimenWidget
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox
import pyodbc
from datetime import datetime
from API.client_app import APIApp


class SpecimenController(QObject):
    """Controller for Specimen Page - copied from lab_manager"""
    
    def __init__(self, view: SpecimenWidget, parent=None):
        super().__init__(parent)
        self.view = view
        self.main_window = parent  # Store reference to main window
        self.case_registration_id = None  # Store the case registration ID
        self.specimen_id = None  # Store the specimen ID after saving
        self.api = APIApp()  # Initialize API client
        self.room_mapping = {}  # Store dynamic room mapping
        self.bind_specimen_events()
        self.load_room_mapping()  # Load room mapping on initialization
        # print("SpecimenController initialized")
    
    def bind_specimen_events(self):
        # Save and cancel buttons
        self.view.ui.specimen_save_pushButton.clicked.connect(self.save_specimen_information)
        self.view.ui.specimen_cancel_pushButton.clicked.connect(self.cancel_specimen)
        
        # Lab navigation buttons
        self.view.ui.specimen_molecular_biology_pushButton.clicked.connect(self.goto_molecular_biology)
        self.view.ui.specimen_microbiology_pushButton.clicked.connect(self.goto_microbiology)
        self.view.ui.specimen_parasitology_pushButton.clicked.connect(self.goto_parasitology)
        self.view.ui.specimen_service_after_death_pushButton.clicked.connect(self.goto_after_death)
    
    def save_specimen_information(self):
        self.view.save_button_clicked()
        print(f"save_specimen_information called - Case ID: {self.case_registration_id}")
    
        result_data_on_page = self.get_specimen_data()

        result = self.api.add_sample_registration(result_data_on_page)

        if result and isinstance(result, dict):
            if result.get('status') == 'success':
                specimen_id = result.get('specimen_id')
                self.specimen_id = specimen_id  # Store specimen_id for use in other controllers
                QMessageBox.information(
                    self.view,
                    "SUCCESS",
                    f"บันทึกข้อมูลตัวอย่างเรียบร้อย\nรหัสตัวอย่าง: {specimen_id}"
                )
                self.get_room_details()
            else:
                error_detail = result.get('detail', 'Unknown error')
                QMessageBox.warning(
                    self.view,
                    "ERROR",
                    f"บันทึกข้อมูลไม่สำเร็จ\n{error_detail}"
                )
        else:
            QMessageBox.warning(
                self.view,
                "ERROR",
                "ไม่สามารถบันทึกข้อมูลได้ กรุณาลองใหม่อีกครั้ง"
            )

    def load_room_mapping(self):
        try:
            room_details = self.api.get_room_details()
            
            if room_details and 'lab_rooms' in room_details:
                rooms = room_details['lab_rooms']
                button_keywords = {
                    'microbiology': [
                        'microbiology', 'bacteria', 'bact', 'จุลชีววิทยา', 
                        'แบคทีเรีย', 'bacterial', 'micro', 'เชื้อ','D403',
                        'แบคทีเรีย'
                    ],
                    'parasitology': [
                        'parasitology', 'parasite', 'para', 'ปรสิตวิทยา', 
                        'ปรสิต', 'parasitic', 'พยาธิ', 'worm'
                    ],
                    'molecular_biology': [
                        'molecular', 'pcr', 'อณูชีววิทยา', 'molecular biology',
                        'gene', 'dna', 'rna', 'พันธุกรรม', 'เจเนติก'
                    ],
                    'after_death': [
                        'unclassified', 'ไม่ระบุ', 'after death', 'หลังความตาย',
                        'ชันสูตร', 'autopsy', 'necropsy', 'post-mortem', 'ไม่จำแนก'
                    ]
                }
                
                for button_key, keywords in button_keywords.items():
                    for room in rooms:
                        room_id = room.get('id')
                        name = room.get('name', '').lower()
                        thai_name = room.get('thai_name', '').lower()
                        nickname = room.get('nickname', '').lower()
                        code = room.get('code', '').lower()
                        searchable_text = f"{name} {thai_name} {nickname} {code}"
                        
                        for keyword in keywords:
                            if keyword.lower() in searchable_text:
                                self.room_mapping[button_key] = room_id
                                break 
                        if button_key in self.room_mapping:
                            break
                
                button_names = {
                    'microbiology': 'จุลชีววิทยา (MICROBIOLOGY)',
                    'parasitology': 'ปรสิตวิทยา (PARASITOLOGY)',
                    'molecular_biology': 'อณูชีววิทยา (MOLECULAR BIOLOGY)',
                    'after_death': 'งานบริการหลังความตาย (AFTER DEATH)'
                }
                
                unmapped_buttons = []
                
                for button_key, button_name in button_names.items():
                    if button_key in self.room_mapping:
                        room_id = self.room_mapping[button_key]
                        # Find room details
                        room = next((r for r in rooms if r['id'] == room_id), None)
                        # if room:
                        #     print(f"✓ {button_name}")
                        #     print(f"  → Room ID: {room_id}")
                        #     print(f"  → Room: [{room.get('code', '')}] {room.get('thai_name', '')}")
                    else:
                        unmapped_buttons.append(button_name)
            else:
                print("⚠️ Failed to load room mapping from database")
        except Exception as e:
            print(f"⚠️ Error loading room mapping: {e}")



    def get_room_details(self):
        """Fetch and display lab room details with dynamic button mapping"""
        room_details = self.api.get_room_details()
        
        if room_details and 'lab_rooms' in room_details:
            rooms = sorted(room_details['lab_rooms'], key=lambda x: x.get('id', 0))
            room_lookup = {room['id']: room for room in rooms}
            
            for room in rooms:
                room_id = room.get('id')
                code = room.get('code', '').strip()
                eng_name = room.get('name', '').strip()
                thai_name = room.get('thai_name', '').strip()
                nickname = room.get('nickname', '').strip()
                
                if code:
                    display = f"{room_id:2d}. [{code}] {thai_name}"
                else:
                    display = f"{room_id:2d}. {thai_name}"
                if eng_name:
                    display += f" ({eng_name})"
                if nickname:
                    display += f" [{nickname}]"
                # print(display)
            
            
            button_names = {
                'microbiology': ' จุลชีววิทยา (MICROBIOLOGY)',
                'parasitology': ' ปรสิตวิทยา (PARASITOLOGY)',
                'molecular_biology': 'อณูชีววิทยา (MOLECULAR BIOLOGY)',
                'after_death': 'งานบริการหลังความตาย'
            }
            
            for button_key, button_name in button_names.items():
                room_id = self.room_mapping.get(button_key)
                
                if room_id and room_id in room_lookup:
                    room = room_lookup[room_id]
                    code = room.get('code', '').strip()
                    thai_name = room.get('thai_name', '').strip()
                    eng_name = room.get('name', '').strip()
                else:
                    pass
            
            return rooms
        else:
            print("⚠️ ไม่สามารถดึงข้อมูลห้องปฏิบัติการได้")
            return None


    def get_specimen_data(self):
        animal_type = ""
        if self.view.ui.specimen_swine_radioButton.isChecked():
            animal_type = "สุกร (Swine)"
        elif self.view.ui.specimen_avian_radioButton.isChecked():
            animal_type = "สัตว์ปีก (Avian)"
        elif self.view.ui.specimen_bovine_radioButton.isChecked():
            animal_type = "โค (Bovine)"
        elif self.view.ui.specimen_equine_radioButton.isChecked():
            animal_type = "ม้า (Equine)"
        elif self.view.ui.specimen_conine_radioButton.isChecked():
            animal_type = "สุนัข (Canine)"
        elif self.view.ui.specimen_elephant_radioButton.isChecked():
            animal_type = "ช้าง (Elephant)"
        elif self.view.ui.specimen_felin_radioButton.isChecked():
            animal_type = "แมว (Feline)"
        elif self.view.ui.specimen_unknown_radioButton.isChecked():
            animal_type = "Unknown"
        elif self.view.ui.specimen_animal_other_radioButton.isChecked():
            other_text = self.view.ui.specimen_animal_other_lineEdit.text().strip()
            animal_type = f"อื่นๆ: {other_text}" if other_text else "อื่นๆ"

        speed = "ปกติ" if self.view.ui.specimen_normal_radioButton.isChecked() else "ปกติ"

        keeping = ""
        if self.view.ui.specimen_chill_radioButton.isChecked():
            keeping = "แช่เย็น (Chill)"
        elif self.view.ui.specimen_freeze_radioButton.isChecked():
            keeping = "แช่แข็ง (Freeze)"
        elif self.view.ui.specimen_room_temperature_radioButton.isChecked():
            keeping = "ไม่แช่ (Room Temperature)"

        demise = self.view.ui.specimen_death_comboBox.currentText() or ""
        
        sample_inspection = self.view.ui.specimen_sample_comboBox.currentText() or ""
        if self.view.ui.specimen_sample_other_radioButton.isChecked():
            other_sample = self.view.ui.specimen_sample_other_lineEdit.text().strip()
            sample_inspection = f"อื่นๆ: {other_sample}" if other_sample else sample_inspection
            
        def safe_int(value):
            try:
                if isinstance(value, str):
                    value = value.strip()
                return int(value) if value else None
            except (ValueError, AttributeError):
                return None
        
        def safe_float(value):
            try:
                if isinstance(value, str):
                    value = value.strip()
                return float(value) if value else None
            except (ValueError, AttributeError):
                return None
            
        if self.view.ui.specimen_ageUnknown_checkBox.isChecked():
            age_year = 0
            age_month = 0
            age_day = 0
        else:
            age_year = safe_int(self.view.ui.specimen_ageYear_lineEdit.text())
            age_month = safe_int(self.view.ui.specimen_ageMonth_lineEdit.text())
            age_day = safe_int(self.view.ui.specimen_ageDay_lineEdit.text())
            age_year = age_year if age_year is not None else 0
            age_month = age_month if age_month is not None else 0
            age_day = age_day if age_day is not None else 0
        
        # Get case_id from stored value
        case_id = self.case_registration_id
        
        dead_date_str = self.view.ui.specimen_day_of_death_dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        collect_date_str = self.view.ui.specimen_day_keep_sample_dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        weight_value = safe_float(self.view.ui.specimen_weight_lineEdit.text())
        weight_value = weight_value if weight_value is not None else 0.0
        
        data = {
            'case_id': int(case_id) if case_id else None,
            'name': self.view.ui.specimen_name_lineEdit.text().strip() or "",  # Optional
            'opd_number': self.view.ui.specimen_ID_lineEdit.text().strip() or "",  # Optional
            'sex': self.view.ui.specimen_sex_comboBox.currentText() or "",  # Optional
            'age_year': age_year,  # Default: 0
            'age_month': age_month,  # Default: 0
            'age_day': age_day,  # Default: 0
            'demise': demise,  # Optional
            'species': animal_type,  # REQUIRED - ชนิดสัตว์
            'breed': self.view.ui.specimen_breed_lineEdit.text().strip() or "",  # Optional
            'sample_type': speed,
            'weight': weight_value,  # Default: 0.0
            'dead_date': dead_date_str if dead_date_str else None,  # Optional
            'collect_date': collect_date_str if collect_date_str else None,  # Optional
            'keep_method': keeping,  # Optional
            'speed': speed,  # Status: ปกติ/ด่วนที่สุด
            'medical_record': self.view.ui.specimen_record_heal_textEdit.toPlainText().strip() or "",  # Optional
            'dosage_record': self.view.ui.specimen_record_antibiotics_textEdit.toPlainText().strip() or "",  # Optional
            'sample_inspection': sample_inspection,  # Optional
            'updater': self.main_window.get_logged_in_user_id() if self.main_window else None
        }
        
        return data
    
    
    def clear_specimen_information(self):
        print("Clearing specimen information")
    
    def cancel_specimen(self):
        self.view.cancel_button_clicked()
        if self.main_window and hasattr(self.main_window, 'add_work_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.add_work_widget)
            
            # ✅ Refresh/update treewidget data when returning to New Work page
            if hasattr(self.main_window, 'new_work_controller') and self.main_window.new_work_controller:
                self.main_window.new_work_controller.update_treewidget_data()
        else:
            print("Warning: Cannot navigate back to new work page")
    
    def goto_molecular_biology(self):
        room_id = self.room_mapping.get('molecular_biology')
        # print(room_id)
        if self.main_window and hasattr(self.main_window, 'molecular_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.molecular_widget)
            if hasattr(self.main_window.molecular_widget, 'clear_page'):
                self.main_window.molecular_widget.clear_page()
        else:
            print("⚠️ Error: Cannot navigate to molecular biology page")

    def goto_microbiology(self):
        print("Navigate to Microbiology page")
        if self.main_window and hasattr(self.main_window, 'bacteria_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.bacteria_widget)
        else:
            print("Warning: Cannot navigate to microbiology page")
    
    def goto_parasitology(self):
        print("Navigate to Parasitology page")
        if self.main_window and hasattr(self.main_window, 'parasite_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.parasite_widget)
        else:
            print("Warning: Cannot navigate to parasitology page")
    
    def goto_after_death(self):
        print("Navigate to After Death Service page")
        if self.main_window and hasattr(self.main_window, 'after_death_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.after_death_widget)
            if hasattr(self.main_window.after_death_widget, 'clear_page'):
                self.main_window.after_death_widget.clear_page()
        else:
            print("Warning: Cannot navigate to after death page")
    
        # room_id = self.room_mapping.get('microbiology')
        room_id = 2
        print(room_id)
        # if self.main_window and hasattr(self.main_window, 'bacteria_widget'):
        #     self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.bacteria_widget)
        # else:
        #     print("⚠️ Error: Cannot navigate to microbiology page")
    
    def goto_parasitology(self):
        room_id = self.room_mapping.get('parasitology')
        print(room_id)
        # if self.main_window and hasattr(self.main_window, 'parasite_widget'):
        #     self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.parasite_widget)
        # else:
        #     print("⚠️ Error: Cannot navigate to parasitology page")
    
    def goto_after_death(self):
        room_id = self.room_mapping.get('after_death')
        print(room_id)
        # if self.main_window and hasattr(self.main_window, 'after_death_widget'):
        #     self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.after_death_widget)
        #     if hasattr(self.main_window.after_death_widget, 'clear_page'):
        #         self.main_window.after_death_widget.clear_page()
        # else:
        #     print("⚠️ Error: Cannot navigate to after death page")


    def set_case_registration_id(self, case_id):
        """Set the case registration ID from new work page"""
        self.case_registration_id = case_id
        # print(f"case_registration_id: {case_id}")
    
    def get_case_registration_id(self):
        """Get the current case registration ID"""
        return self.case_registration_id

