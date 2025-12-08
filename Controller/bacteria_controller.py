from View.view_bacteria_frame import bacterieFrameView
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox
import pyodbc
from datetime import datetime
from SERVICES_REGISTER.lab_service import LabService

class BacteriaController(QObject):
    """Controller for Bacteria Biology Page - mimicking lab_manager structure"""
    
    def __init__(self, view: bacterieFrameView, parent=None):
        super().__init__(parent)
        self.view = view
        self.main_window = parent  # Store reference to main window
        self.api_client = LabService()  # Initialize API client
        
        # Test prices for Laboratory Request
        self.lab_request_prices = {
            'fungal': 250,
            'identification_sensitive': 250,
            'VITEK2_MIC': 950,
            'VITEK2': 550,
            'MIC': 550
        }
        
        # Bacterial Identification price (per item)
        self.bacterial_identification_price = 250
        
        self.init_sample_line_edits()  # Initialize sample line edits as disabled
        self.bind_bacteria_events()
        self.bind_sample_checkbox_events()  # Bind checkbox events for sample line edits
    
    def bind_bacteria_events(self):
        """Bind all bacteria page button events"""
        # Main buttons - CORRECTED NAMES
        self.view.ui.bacteria_cal_pushButton.clicked.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_save_pushButton.clicked.connect(self.save_all_bacteria_data)
        self.view.ui.bacteria_cancel_pushButton.clicked.connect(self.cancel_bacteria)
        
        # Bind Laboratory Request checkboxes to auto-calculate summary
        self.view.ui.bacteria_fungal_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_Identification_and_sensitive__checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_VITEK2_MIC_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_VITEK2_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_MIC_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        
        # Bind Bacterial Identification checkboxes to auto-calculate summary
        self.view.ui.bacteria_actinobacillus_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_corynebacterium_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_klebsiella_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_streptococcus_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_aeromonas_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_enterobacter_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_pasteurella_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_staphylococcus_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_bordetella_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_escherichia_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_salmonella_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_other_iden_checkBox.stateChanged.connect(self.calculate_bacteria_summary)
    
    def init_sample_line_edits(self):
        """Initialize all sample line edits as disabled (locked)"""
        # Disable all sample line edits by default
        self.view.ui.bacteria_swabLT_lineEdit.setEnabled(False)
        self.view.ui.bacteria_swabRT_lineEdit.setEnabled(False)
        self.view.ui.bacteria_wound_lineEdit.setEnabled(False)
        self.view.ui.bacteria_aspirateLT_lineEdit.setEnabled(False)
        self.view.ui.bacteria_aspirateRT_lineEdit.setEnabled(False)
        self.view.ui.bacteria_urine_lineEdit.setEnabled(False)
        self.view.ui.bacteria_midstream_lineEdit.setEnabled(False)
        self.view.ui.bacteria_catheterization_lineEdit.setEnabled(False)
        self.view.ui.bacteria_cystocentesis_lineEdit.setEnabled(False)
        self.view.ui.bacteria_tissuesLT_lineEdit.setEnabled(False)
        self.view.ui.bacteria_tissuesRT_lineEdit.setEnabled(False)
        self.view.ui.bacteria_biopsyLT_lineEdit.setEnabled(False)
        self.view.ui.bacteria_biopsyRT_lineEdit.setEnabled(False)
        self.view.ui.bacteria_bodyFluidLT_lineEdit.setEnabled(False)
        self.view.ui.bacteria_bodyFluidRT_lineEdit.setEnabled(False)
        self.view.ui.bacteria_csf_lineEdit.setEnabled(False)
        self.view.ui.bacteria_feces_lineEdit.setEnabled(False)
        self.view.ui.bacteria_pus_lineEdit.setEnabled(False)
        self.view.ui.bacteria_blood_lineEdit.setEnabled(False)
        self.view.ui.bacteria_bloodAgar_lineEdit.setEnabled(False)
        self.view.ui.bacteria_skinScaping_lineEdit.setEnabled(False)
    
    def bind_sample_checkbox_events(self):
        """Bind checkbox stateChanged signals to enable/disable corresponding line edits"""
        # Connect each checkbox to its corresponding line edit
        self.view.ui.bacteria_swabLT_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_swabLT_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_swabRT_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_swabRT_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_wound_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_wound_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_aspirateLT_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_aspirateLT_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_aspirateRT_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_aspirateRT_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_urine_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_urine_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_midstream_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_midstream_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_catheterization_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_catheterization_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_cystocentesis_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_cystocentesis_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_tissuesLT_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_tissuesLT_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_tissuesRT_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_tissuesRT_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_biopsyLT_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_biopsyLT_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_biopsyRT_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_biopsyRT_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_bodyFluidLT_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_bodyFluidLT_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_bodyFluidRT_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_bodyFluidRT_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_csf_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_csf_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_feces_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_feces_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_pus_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_pus_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_blood_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_blood_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_bloodAgar_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_bloodAgar_lineEdit.setEnabled(state == 2))
        self.view.ui.bacteria_skinScaping_checkBox.stateChanged.connect(
            lambda state: self.view.ui.bacteria_skinScaping_lineEdit.setEnabled(state == 2))
    
    # ========== SAMPLE PREPARATION FUNCTIONS ==========
    
    def get_sample_preparation_data(self):
        """
        Get sample preparation data in format for database.
        Returns a list of dictionaries with name, state, and amount.
        """
        # Define all 21 sample preparation items in order
        prep_configs = [
            {'name': 'Swab [LT]', 'checkbox': self.view.ui.bacteria_swabLT_checkBox, 'lineedit': self.view.ui.bacteria_swabLT_lineEdit},
            {'name': 'Swab [RT]', 'checkbox': self.view.ui.bacteria_swabRT_checkBox, 'lineedit': self.view.ui.bacteria_swabRT_lineEdit},
            {'name': 'Wound', 'checkbox': self.view.ui.bacteria_wound_checkBox, 'lineedit': self.view.ui.bacteria_wound_lineEdit},
            {'name': 'Aspirate [LT]', 'checkbox': self.view.ui.bacteria_aspirateLT_checkBox, 'lineedit': self.view.ui.bacteria_aspirateLT_lineEdit},
            {'name': 'Aspirate [RT]', 'checkbox': self.view.ui.bacteria_aspirateRT_checkBox, 'lineedit': self.view.ui.bacteria_aspirateRT_lineEdit},
            {'name': 'Urine', 'checkbox': self.view.ui.bacteria_urine_checkBox, 'lineedit': self.view.ui.bacteria_urine_lineEdit},
            {'name': 'Midstream', 'checkbox': self.view.ui.bacteria_midstream_checkBox, 'lineedit': self.view.ui.bacteria_midstream_lineEdit},
            {'name': 'Catheterization', 'checkbox': self.view.ui.bacteria_catheterization_checkBox, 'lineedit': self.view.ui.bacteria_catheterization_lineEdit},
            {'name': 'Cystocentesis', 'checkbox': self.view.ui.bacteria_cystocentesis_checkBox, 'lineedit': self.view.ui.bacteria_cystocentesis_lineEdit},
            {'name': 'Tissues [LT]', 'checkbox': self.view.ui.bacteria_tissuesLT_checkBox, 'lineedit': self.view.ui.bacteria_tissuesLT_lineEdit},
            {'name': 'Tissues [RT]', 'checkbox': self.view.ui.bacteria_tissuesRT_checkBox, 'lineedit': self.view.ui.bacteria_tissuesRT_lineEdit},
            {'name': 'Biopsy [LT]', 'checkbox': self.view.ui.bacteria_biopsyLT_checkBox, 'lineedit': self.view.ui.bacteria_biopsyLT_lineEdit},
            {'name': 'Biopsy [RT]', 'checkbox': self.view.ui.bacteria_biopsyRT_checkBox, 'lineedit': self.view.ui.bacteria_biopsyRT_lineEdit},
            {'name': 'Body fluid [LT]', 'checkbox': self.view.ui.bacteria_bodyFluidLT_checkBox, 'lineedit': self.view.ui.bacteria_bodyFluidLT_lineEdit},
            {'name': 'Body fluid [RT]', 'checkbox': self.view.ui.bacteria_bodyFluidRT_checkBox, 'lineedit': self.view.ui.bacteria_bodyFluidRT_lineEdit},
            {'name': 'CSF', 'checkbox': self.view.ui.bacteria_csf_checkBox, 'lineedit': self.view.ui.bacteria_csf_lineEdit},
            {'name': 'Feces', 'checkbox': self.view.ui.bacteria_feces_checkBox, 'lineedit': self.view.ui.bacteria_feces_lineEdit},
            {'name': 'PUS', 'checkbox': self.view.ui.bacteria_pus_checkBox, 'lineedit': self.view.ui.bacteria_pus_lineEdit},
            {'name': 'Blood', 'checkbox': self.view.ui.bacteria_blood_checkBox, 'lineedit': self.view.ui.bacteria_blood_lineEdit},
            {'name': 'Blood agar', 'checkbox': self.view.ui.bacteria_bloodAgar_checkBox, 'lineedit': self.view.ui.bacteria_bloodAgar_lineEdit},
            {'name': 'Skin scraping', 'checkbox': self.view.ui.bacteria_skinScaping_checkBox, 'lineedit': self.view.ui.bacteria_skinScaping_lineEdit},
        ]
        
        prep_items = []
        for config in prep_configs:
            is_checked = config['checkbox'].isChecked()
            amount_text = config['lineedit'].text().strip() if is_checked else ''
            try:
                amount = int(amount_text) if amount_text else 0
            except ValueError:
                amount = 0
            
            prep_items.append({
                'name': config['name'],
                'state': 1 if is_checked else 0,
                'amount': amount
            })
        
        return prep_items
    
    def save_sample_preparation(self):
        """Save sample preparation data"""
        try:
            samples = self.get_sample_preparation_data()
            
            if not samples:
                QMessageBox.warning(self.view, "คำเตือน", "กรุณาเลือกตัวอย่างอย่างน้อย 1 รายการ!")
                return
            
            connection = self.connect_database()
            cursor = connection.cursor()
            
            # Convert samples dict to JSON or save individually
            import json
            samples_json = json.dumps(samples)
            
            sql = """
            INSERT INTO bacteria_sample_preparation 
            (samples_data, created_date)
            VALUES (?, ?)
            """
            
            cursor.execute(sql, (samples_json, datetime.now()))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            QMessageBox.information(self.view, "สำเร็จ", "บันทึกข้อมูลการเตรียมตัวอย่างสำเร็จ!")
            
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
    
    def clear_sample_preparation(self):
        """Clear sample preparation fields - CORRECTED"""
        # Clear all checkboxes
        self.view.ui.bacteria_swabLT_checkBox.setChecked(False)
        self.view.ui.bacteria_swabRT_checkBox.setChecked(False)
        self.view.ui.bacteria_wound_checkBox.setChecked(False)
        self.view.ui.bacteria_aspirateLT_checkBox.setChecked(False)
        self.view.ui.bacteria_aspirateRT_checkBox.setChecked(False)
        self.view.ui.bacteria_urine_checkBox.setChecked(False)
        self.view.ui.bacteria_midstream_checkBox.setChecked(False)
        self.view.ui.bacteria_catheterization_checkBox.setChecked(False)
        self.view.ui.bacteria_cystocentesis_checkBox.setChecked(False)
        self.view.ui.bacteria_tissuesLT_checkBox.setChecked(False)
        self.view.ui.bacteria_tissuesRT_checkBox.setChecked(False)
        self.view.ui.bacteria_biopsyLT_checkBox.setChecked(False)
        self.view.ui.bacteria_biopsyRT_checkBox.setChecked(False)
        self.view.ui.bacteria_bodyFluidLT_checkBox.setChecked(False)
        self.view.ui.bacteria_bodyFluidRT_checkBox.setChecked(False)
        self.view.ui.bacteria_csf_checkBox.setChecked(False)
        self.view.ui.bacteria_feces_checkBox.setChecked(False)
        self.view.ui.bacteria_pus_checkBox.setChecked(False)
        self.view.ui.bacteria_blood_checkBox.setChecked(False)
        self.view.ui.bacteria_bloodAgar_checkBox.setChecked(False)
        self.view.ui.bacteria_skinScaping_checkBox.setChecked(False)
        
        # Clear all lineEdits
        self.view.ui.bacteria_swabLT_lineEdit.clear()
        self.view.ui.bacteria_swabRT_lineEdit.clear()
        self.view.ui.bacteria_wound_lineEdit.clear()
        self.view.ui.bacteria_aspirateLT_lineEdit.clear()
        self.view.ui.bacteria_aspirateRT_lineEdit.clear()
        self.view.ui.bacteria_urine_lineEdit.clear()
        self.view.ui.bacteria_midstream_lineEdit.clear()
        self.view.ui.bacteria_catheterization_lineEdit.clear()
        self.view.ui.bacteria_cystocentesis_lineEdit.clear()
        self.view.ui.bacteria_tissuesLT_lineEdit.clear()
        self.view.ui.bacteria_tissuesRT_lineEdit.clear()
        self.view.ui.bacteria_biopsyLT_lineEdit.clear()
        self.view.ui.bacteria_biopsyRT_lineEdit.clear()
        self.view.ui.bacteria_bodyFluidLT_lineEdit.clear()
        self.view.ui.bacteria_bodyFluidRT_lineEdit.clear()
        self.view.ui.bacteria_csf_lineEdit.clear()
        self.view.ui.bacteria_feces_lineEdit.clear()
        self.view.ui.bacteria_pus_lineEdit.clear()
        self.view.ui.bacteria_blood_lineEdit.clear()
        self.view.ui.bacteria_bloodAgar_lineEdit.clear()
        self.view.ui.bacteria_skinScaping_lineEdit.clear()
        
        # Re-disable all line edits after clearing
        self.init_sample_line_edits()
    
    # ========== DRUG SENSITIVITY FUNCTIONS ==========
    
    def get_drug_sensitivity_data(self):
        """
        Get drug sensitivity test data in format for database.
        Returns a list of dictionaries with name and state.
        Database has 41 drug sensitivity columns.
        """
        # Define all 41 drug sensitivity items in order
        drug_configs = [
            {'name': 'Amikacin(AK)', 'checkbox': self.view.ui.bacteria_amikacin_checkBox},
            {'name': 'Ampicillin(AMP)', 'checkbox': self.view.ui.bacteria_ampicillin_checkBox},
            {'name': 'Ceftazidime(CAZ)', 'checkbox': self.view.ui.bacteria_ceftazidime_checkBox},
            {'name': 'Cephalexin(CL)', 'checkbox': self.view.ui.bacteria_cephalexin_checkBox},
            {'name': 'Chloramphenicol(C)', 'checkbox': self.view.ui.bacteria_chloramphenicol_checkBox},
            {'name': 'Cloxacillin(OB)', 'checkbox': self.view.ui.bacteria_cloxacillin_checkBox},
            {'name': 'Enrofloxacin(ENR)', 'checkbox': self.view.ui.bacteria_enrofloxacin_checkBox},
            {'name': 'Gentamycin(CN)', 'checkbox': self.view.ui.bacteria_gentamycin_checkBox},
            {'name': 'Lincomycin(MY)', 'checkbox': self.view.ui.bacteria_lincomycin_checkBox},
            {'name': 'Norfloxacin(NOR)', 'checkbox': self.view.ui.bacteria_norfloxacin_checkBox},
            {'name': 'Oxacillin(OX)', 'checkbox': self.view.ui.bacteria_oxacillin_checkBox},
            {'name': 'PolymyxcinB(PB)', 'checkbox': self.view.ui.bacteria_polymyxcinB_checkBox},
            {'name': 'Sulfa-Trimetroprom(SXT)', 'checkbox': self.view.ui.bacteria_sulfa_trimetroprom_checkBox},
            {'name': 'Vancomycin(VA)', 'checkbox': self.view.ui.bacteria_vancomycin_checkBox},
            # Column 2
            {'name': 'Amoxycillin(AML)', 'checkbox': self.view.ui.bacteria_amoxycillin_checkBox},
            {'name': 'Bactracin(B)', 'checkbox': self.view.ui.bacteria_bactracin_checkBox},
            {'name': 'Ceftiofur(EFT)', 'checkbox': self.view.ui.bacteria_ceftiofur_checkBox},
            {'name': 'Cephalothin(KF)', 'checkbox': self.view.ui.bacteria_cephalothin_checkBox},
            {'name': 'Ciprofloxacin(CIP)', 'checkbox': self.view.ui.bacteria_ciprofloxacin_checkBox},
            {'name': 'Colistin(CT)', 'checkbox': self.view.ui.bacteria_colistin_checkBox},
            {'name': 'Erythromycin(E)', 'checkbox': self.view.ui.bacteria_erythromycin_checkBox},
            {'name': 'Imipenem(IPM)', 'checkbox': self.view.ui.bacteria_imipenem_checkBox},
            {'name': 'Neomycin(N)', 'checkbox': self.view.ui.bacteria_neomycin_checkBox},
            {'name': 'Novobiocin(NV)', 'checkbox': self.view.ui.bacteria_novobiocin_checkBox},
            {'name': 'Oxytetracycline(OT)', 'checkbox': self.view.ui.bacteria_oxytetracycline_checkBox},
            {'name': 'Rifampicin(RD)', 'checkbox': self.view.ui.bacteria_rifampicin_checkBox},
            {'name': 'Tetracycline(TE)', 'checkbox': self.view.ui.bacteria_tetracycline_checkBox},
            # Column 3
            {'name': 'Amoxy(AMC)', 'checkbox': self.view.ui.bacteria_amoxy_checkBox},
            {'name': 'Clav(AMC)', 'checkbox': self.view.ui.bacteria_clav_checkBox},
            {'name': 'Ceftriaxone(CRO)', 'checkbox': self.view.ui.bacteria_ceftriaxone_checkBox},
            {'name': 'Cephazolin(KZ)', 'checkbox': self.view.ui.bacteria_cephazolin_checkBox},
            {'name': 'Clindamicin(DA)', 'checkbox': self.view.ui.bacteria_clindamicin_checkBox},
            {'name': 'Doxycycline(DO)', 'checkbox': self.view.ui.bacteria_doxycycline_checkBox},
            {'name': 'Fosfomycin(FOS)', 'checkbox': self.view.ui.bacteria_fosfomycin_checkBox},
            {'name': 'Kanamycin(K)', 'checkbox': self.view.ui.bacteria_kanamycin_checkBox},
            {'name': 'Nitrofurantoin(F)', 'checkbox': self.view.ui.bacteria_nitrofurantoin_checkBox},
            {'name': 'Optocin(OP)', 'checkbox': self.view.ui.bacteria_optocin_checkBox},
            {'name': 'Penicillin(P)', 'checkbox': self.view.ui.bacteria_penicillin_checkBox},
            {'name': 'Streptomycin(S)', 'checkbox': self.view.ui.bacteria_streptomycin_checkBox},
            {'name': 'Tobramycin(TOB)', 'checkbox': self.view.ui.bacteria_tobramycin_checkBox},
            # Other (slot 41)
            {'name': 'Other', 'checkbox': self.view.ui.bacteria_other_sen_checkBox, 'lineedit': self.view.ui.bacteria_other_sen_lineEdit},
        ]
        
        drug_items = []
        for config in drug_configs:
            is_checked = config['checkbox'].isChecked()
            name = config['name']
            
            # Handle "Other" with custom text
            if 'lineedit' in config and is_checked:
                other_text = config['lineedit'].text().strip()
                if other_text:
                    name = f"Other: {other_text}"
            
            drug_items.append({
                'name': name,
                'state': 1 if is_checked else 0
            })
        
        return drug_items
    
    def save_drug_sensitivity(self):
        """Save drug sensitivity test data"""
        try:
            drugs = self.get_drug_sensitivity_data()
            
            if not drugs:
                QMessageBox.warning(self.view, "คำเตือน", "กรุณาเลือกยาปฏิชีวนะอย่างน้อย 6-8 รายการ!")
                return
            
            if len(drugs) < 6:
                QMessageBox.warning(self.view, "คำเตือน", "กรุณาเลือกยาปฏิชีวนะอย่างน้อย 6 รายการ!")
                return
            
            connection = self.connect_database()
            cursor = connection.cursor()
            
            import json
            drugs_json = json.dumps(drugs)
            
            sql = """
            INSERT INTO bacteria_drug_sensitivity 
            (drugs_data, drug_count, created_date)
            VALUES (?, ?, ?)
            """
            
            cursor.execute(sql, (drugs_json, len(drugs), datetime.now()))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            QMessageBox.information(self.view, "สำเร็จ", f"บันทึกข้อมูลการทดสอบความไวต่อยาสำเร็จ! (เลือก {len(drugs)} รายการ)")
            
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
    
    def clear_drug_sensitivity(self):
        """Clear drug sensitivity fields - CORRECTED"""
        # Clear all drug checkboxes
        self.view.ui.bacteria_amikacin_checkBox.setChecked(False)
        self.view.ui.bacteria_ampicillin_checkBox.setChecked(False)
        self.view.ui.bacteria_ceftazidime_checkBox.setChecked(False)
        self.view.ui.bacteria_cephalexin_checkBox.setChecked(False)
        self.view.ui.bacteria_chloramphenicol_checkBox.setChecked(False)
        self.view.ui.bacteria_cloxacillin_checkBox.setChecked(False)
        self.view.ui.bacteria_enrofloxacin_checkBox.setChecked(False)
        self.view.ui.bacteria_gentamycin_checkBox.setChecked(False)
        self.view.ui.bacteria_lincomycin_checkBox.setChecked(False)
        self.view.ui.bacteria_norfloxacin_checkBox.setChecked(False)
        self.view.ui.bacteria_oxacillin_checkBox.setChecked(False)
        self.view.ui.bacteria_polymyxcinB_checkBox.setChecked(False)
        self.view.ui.bacteria_sulfa_trimetroprom_checkBox.setChecked(False)
        self.view.ui.bacteria_vancomycin_checkBox.setChecked(False)
        self.view.ui.bacteria_amoxycillin_checkBox.setChecked(False)
        self.view.ui.bacteria_bactracin_checkBox.setChecked(False)
        self.view.ui.bacteria_ceftiofur_checkBox.setChecked(False)
        self.view.ui.bacteria_cephalothin_checkBox.setChecked(False)
        self.view.ui.bacteria_ciprofloxacin_checkBox.setChecked(False)
        self.view.ui.bacteria_colistin_checkBox.setChecked(False)
        self.view.ui.bacteria_erythromycin_checkBox.setChecked(False)
        self.view.ui.bacteria_imipenem_checkBox.setChecked(False)
        self.view.ui.bacteria_neomycin_checkBox.setChecked(False)
        self.view.ui.bacteria_novobiocin_checkBox.setChecked(False)
        self.view.ui.bacteria_oxytetracycline_checkBox.setChecked(False)
        self.view.ui.bacteria_rifampicin_checkBox.setChecked(False)
        self.view.ui.bacteria_tetracycline_checkBox.setChecked(False)
        self.view.ui.bacteria_amoxy_checkBox.setChecked(False)
        self.view.ui.bacteria_clav_checkBox.setChecked(False)
        self.view.ui.bacteria_ceftriaxone_checkBox.setChecked(False)
        self.view.ui.bacteria_cephazolin_checkBox.setChecked(False)
        self.view.ui.bacteria_clindamicin_checkBox.setChecked(False)
        self.view.ui.bacteria_doxycycline_checkBox.setChecked(False)
        self.view.ui.bacteria_fosfomycin_checkBox.setChecked(False)
        self.view.ui.bacteria_kanamycin_checkBox.setChecked(False)
        self.view.ui.bacteria_nitrofurantoin_checkBox.setChecked(False)
        self.view.ui.bacteria_optocin_checkBox.setChecked(False)
        self.view.ui.bacteria_penicillin_checkBox.setChecked(False)
        self.view.ui.bacteria_streptomycin_checkBox.setChecked(False)
        self.view.ui.bacteria_tobramycin_checkBox.setChecked(False)
        self.view.ui.bacteria_other_sen_checkBox.setChecked(False)
        self.view.ui.bacteria_other_sen_lineEdit.clear()
    
    # ========== BACTERIAL IDENTIFICATION FUNCTIONS ==========
    
    def get_bacterial_identification_data(self):
        """
        Get bacterial identification data in format for database.
        Returns a list of dictionaries with name and state.
        Database has 12 bacterial identification columns.
        """
        test_configs = [
            {'name': 'Actinobacillus spp.', 'checkbox': self.view.ui.bacteria_actinobacillus_checkBox},
            {'name': 'Corynebacterium spp.', 'checkbox': self.view.ui.bacteria_corynebacterium_checkBox},
            {'name': 'Klebsiella spp.', 'checkbox': self.view.ui.bacteria_klebsiella_checkBox},
            {'name': 'Streptococcus spp.', 'checkbox': self.view.ui.bacteria_streptococcus_checkBox},
            {'name': 'Aeromonas spp.', 'checkbox': self.view.ui.bacteria_aeromonas_checkBox},
            {'name': 'Enterobacter spp.', 'checkbox': self.view.ui.bacteria_enterobacter_checkBox},
            {'name': 'Pasteurella spp.', 'checkbox': self.view.ui.bacteria_pasteurella_checkBox},
            {'name': 'Staphylococcus spp.', 'checkbox': self.view.ui.bacteria_staphylococcus_checkBox},
            {'name': 'Bordetella spp.', 'checkbox': self.view.ui.bacteria_bordetella_checkBox},
            {'name': 'Escherichia coli', 'checkbox': self.view.ui.bacteria_escherichia_checkBox},
            {'name': 'Salmonella spp.', 'checkbox': self.view.ui.bacteria_salmonella_checkBox},
            # Other (slot 12)
            {'name': 'Other', 'checkbox': self.view.ui.bacteria_other_iden_checkBox, 'lineedit': self.view.ui.bacteria_other_iden_lineEdit},
        ]
        
        bacteria_items = []
        for config in test_configs:
            is_checked = config['checkbox'].isChecked()
            name = config['name']
            
            # Handle "Other" with custom text
            if 'lineedit' in config and is_checked:
                other_text = config['lineedit'].text().strip()
                if other_text:
                    name = f"Other: {other_text}"
            
            bacteria_items.append({
                'name': name,
                'state': 1 if is_checked else 0
            })
        
        return bacteria_items
    
    def save_bacterial_identification(self):
        """Save bacterial identification data - DEPRECATED: Use save_all_bacteria_data instead"""
        pass
    
    def clear_bacterial_identification(self):
        """Clear bacterial identification fields - CORRECTED"""
        self.view.ui.bacteria_actinobacillus_checkBox.setChecked(False)
        self.view.ui.bacteria_corynebacterium_checkBox.setChecked(False)
        self.view.ui.bacteria_klebsiella_checkBox.setChecked(False)
        self.view.ui.bacteria_streptococcus_checkBox.setChecked(False)
        self.view.ui.bacteria_aeromonas_checkBox.setChecked(False)
        self.view.ui.bacteria_enterobacter_checkBox.setChecked(False)
        self.view.ui.bacteria_pasteurella_checkBox.setChecked(False)
        self.view.ui.bacteria_staphylococcus_checkBox.setChecked(False)
        self.view.ui.bacteria_bordetella_checkBox.setChecked(False)
        self.view.ui.bacteria_escherichia_checkBox.setChecked(False)
        self.view.ui.bacteria_salmonella_checkBox.setChecked(False)
        self.view.ui.bacteria_other_iden_checkBox.setChecked(False)
        self.view.ui.bacteria_other_iden_lineEdit.clear()
    
    # ========== LABORATORY REQUEST FUNCTIONS ==========
    
    def get_laboratory_request_data(self):
        """
        Get laboratory request data in format for database.
        Returns a list of dictionaries with name, state, and price.
        Database has 5 lab request columns.
        """
        test_configs = [
            {'name': 'Fungal culture and identification', 'price': self.lab_request_prices['fungal'], 
             'checkbox': self.view.ui.bacteria_fungal_checkBox},
            {'name': 'Bacterial identification and drug sensitivity', 'price': self.lab_request_prices['identification_sensitive'], 
             'checkbox': self.view.ui.bacteria_Identification_and_sensitive__checkBox},
            {'name': 'VITEK2 with MIC', 'price': self.lab_request_prices['VITEK2_MIC'], 
             'checkbox': self.view.ui.bacteria_VITEK2_MIC_checkBox},
            {'name': 'VITEK2 iden', 'price': self.lab_request_prices['VITEK2'], 
             'checkbox': self.view.ui.bacteria_VITEK2_checkBox},
            {'name': 'MIC', 'price': self.lab_request_prices['MIC'], 
             'checkbox': self.view.ui.bacteria_MIC_checkBox},
        ]
        
        lab_items = []
        for config in test_configs:
            is_checked = config['checkbox'].isChecked()
            name_with_price = f"{config['name']} ({config['price']})"
            lab_items.append({
                'name': name_with_price,
                'state': 1 if is_checked else 0,
                'price': config['price']
            })
        
        return lab_items
    
    def save_laboratory_request(self):
        """Save laboratory request data - DEPRECATED: Use save_all_bacteria_data instead"""
        pass
    
    def clear_laboratory_request(self):
        """Clear laboratory request fields - CORRECTED"""
        self.view.ui.bacteria_fungal_checkBox.setChecked(False)
        self.view.ui.bacteria_Identification_and_sensitive__checkBox.setChecked(False)
        self.view.ui.bacteria_VITEK2_MIC_checkBox.setChecked(False)
        self.view.ui.bacteria_VITEK2_checkBox.setChecked(False)
        self.view.ui.bacteria_MIC_checkBox.setChecked(False)
    
    # ========== SUMMARY FUNCTIONS ==========
    
    def calculate_bacteria_summary(self):
        """Calculate and display bacteria test summary - auto updates when checkbox changes"""
        # Get all test data
        bacteria_items = self.get_bacterial_identification_data()
        lab_request_items = self.get_laboratory_request_data()
        
        # Calculate totals from selected items (state > 0)
        total_tests = 0
        total_cost = 0.0
        
        # Count selected bacterial identification items (price = 250 per item)
        for item in bacteria_items:
            if item['state'] > 0:
                total_tests += 1
                total_cost += self.bacterial_identification_price
        
        # Count selected laboratory request items
        for item in lab_request_items:
            if item['state'] > 0:
                total_tests += 1
                total_cost += item['price']
        
        # Update display - CORRECTED WIDGET NAMES
        self.view.ui.bacteria_num_lineEdit.setText(str(total_tests))
        self.view.ui.bacteria_cost_lineEdit.setText(f"{total_cost:.2f}")
    
    def get_bacteria_data(self):
        """
        Get all bacteria test data in the same format as molecular biology and parasite.
        Returns a dictionary containing laboratory requests and bacterial identification tests.
        """
        lab_request_items = self.get_laboratory_request_data()
        bacteria_items = self.get_bacterial_identification_data()
        
        # Combine all tests into one list
        all_tests = lab_request_items + bacteria_items
        
        return all_tests
    
    def get_bacteria_summary_data(self):
        """Get summary data - CORRECTED"""
        return {
            'total_tests': self.view.ui.bacteria_num_lineEdit.text(),
            'total_cost': self.view.ui.bacteria_cost_lineEdit.text(),
            'remark': self.view.ui._bacteria_remark_plainTextEdit.toPlainText()  # CORRECTED
        }
    
    # ========== SAVE ALL & CANCEL FUNCTIONS ==========
    
    def save_all_bacteria_data(self):
        """Save all bacteria page data at once using API"""
        try:
            # Get all data in proper format for API
            sample_prep_data = self.get_sample_preparation_data()
            drug_sensitivity_data = self.get_drug_sensitivity_data()
            bacteria_id_data = self.get_bacterial_identification_data()
            lab_request_data = self.get_laboratory_request_data()
            
            # Validate - check if at least one lab request is selected
            selected_lab_requests = [item for item in lab_request_data if item['state'] > 0]
            
            if not selected_lab_requests:
                QMessageBox.warning(
                    self.view, 
                    "Warning", 
                    "กรุณาเลือกรายการที่ต้องการส่งตรวจใน Laboratory Request\n(Please select at least one test)"
                )
                return
            
            # Get sample_id from specimen_controller
            sample_id = None
            if hasattr(self.main_window, 'specimen_controller'):
                specimen_ctrl = self.main_window.specimen_controller
                if hasattr(specimen_ctrl, 'specimen_id') and specimen_ctrl.specimen_id:
                    sample_id = str(specimen_ctrl.specimen_id)
            
            if not sample_id:
                QMessageBox.warning(
                    self.view,
                    "ไม่พบหมายเลข Sample ID",
                    "กรุณาบันทึกข้อมูล Specimen ในหน้าก่อนหน้านี้ก่อน\n"
                    "แล้วจึงกลับมาเลือกรายการตรวจ Bacteria"
                )
                return
            
            # Get user_id from main controller
            user_id = None
            if hasattr(self.main_window, 'main_controller'):
                main_ctrl = self.main_window.main_controller
                if hasattr(main_ctrl, 'logged_in_user_id') and main_ctrl.logged_in_user_id:
                    user_id = main_ctrl.logged_in_user_id
            
            if not user_id:
                QMessageBox.warning(
                    self.view,
                    "ไม่พบข้อมูลผู้ใช้",
                    "กรุณา Login ใหม่อีกครั้ง"
                )
                return
            
            # Get room_id for bacteria lab
            room_id = "2"  # Default room_id for Microbiology (จุลชีววิทยา)
            if hasattr(self.main_window, 'specimen_controller'):
                specimen_ctrl = self.main_window.specimen_controller
                # Try both 'bacteriology' and 'microbiology' keys
                if hasattr(specimen_ctrl, 'room_mapping'):
                    if 'bacteriology' in specimen_ctrl.room_mapping:
                        room_id = specimen_ctrl.room_mapping['bacteriology']
                    elif 'microbiology' in specimen_ctrl.room_mapping:
                        room_id = specimen_ctrl.room_mapping['microbiology']
            
            # Prepare data for bacteria biology API - matching database structure
            bacteria_data = {
                "sample_id": sample_id,
                "sample_preparation": sample_prep_data,  # 21 items
                "drug_sensitivity": drug_sensitivity_data,  # 41 items
                "bacteria_identification": bacteria_id_data,  # 12 items
                "lab_request": lab_request_data,  # 5 items
                "remark": self.view.ui._bacteria_remark_plainTextEdit.toPlainText(),
                "updater": user_id
            }
            
            # Prepare data for lab order API
            lab_order_data = {
                "sample_id": sample_id,
                "room_id": str(room_id),
                "comments": "",
                "state": "0",
                "status": "1",
                "updater": user_id
            }
            
            # Prepare first tracking entry
            first_update_tracking_lab_order_data = {
                "sample_id": sample_id,
                "tracking_info": "รับงานเข้าระบบ",
                "receiver": str(user_id),
                "updater": str(user_id)
            }
            
            # Call APIs
            save_bacteria_result = self.api_client.save_bacteria_biology(bacteria_data)
            insert_lab_order = self.api_client.add_new_lab_order(lab_order_data)
            first_update_tracking = self.api_client.update_tracking_lab_order(first_update_tracking_lab_order_data)
            
            # Check results
            if (save_bacteria_result and save_bacteria_result.get("status") == "success" and
                insert_lab_order and first_update_tracking and 
                first_update_tracking.get("status") == "success"):
                
                # Calculate summary for display
                total_tests = len(selected_lab_requests)
                selected_bacteria = [item for item in bacteria_id_data if item['state'] > 0]
                total_tests += len(selected_bacteria)
                
                total_cost = sum(item['price'] for item in selected_lab_requests)
                total_cost += len(selected_bacteria) * self.bacterial_identification_price
                
                QMessageBox.information(
                    self.view,
                    "สำเร็จ",
                    f"บันทึกข้อมูลการตรวจแบคทีเรียเรียบร้อย\n\n"
                    f"Sample ID: {sample_id}\n"
                    f"รายการที่เลือก: {total_tests} รายการ\n"
                    f"ราคารวม: {total_cost:.2f} บาท"
                )
                
                self.clear_all_bacteria_information()
                self.go_back_to_new_work()
            else:
                error_msg = "Unknown error"
                if save_bacteria_result and isinstance(save_bacteria_result, dict):
                    error_msg = save_bacteria_result.get('detail', error_msg)
                
                QMessageBox.critical(
                    self.view,
                    "ข้อผิดพลาด",
                    f"บันทึกข้อมูลไม่สำเร็จ\n\n{error_msg}"
                )
            
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "ข้อผิดพลาด",
                f"เกิดข้อผิดพลาดในการบันทึก: {str(e)}"
            )
    
    def clear_all_bacteria_information(self):
        """Clear all bacteria form fields"""
        self.clear_sample_preparation()
        self.clear_drug_sensitivity()
        self.clear_bacterial_identification()
        self.clear_laboratory_request()
        self.view.ui.bacteria_num_lineEdit.clear()
        self.view.ui.bacteria_cost_lineEdit.clear()
        self.view.ui._bacteria_remark_plainTextEdit.clear()  # CORRECTED
    
    def cancel_bacteria(self):
        """Cancel and clear all bacteria forms"""
        reply = QMessageBox.question(
            self.view,
            "ยืนยันการยกเลิก",
            "คุณต้องการยกเลิกและล้างข้อมูลทั้งหมดหรือไม่?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.clear_all_bacteria_information()
            QMessageBox.information(self.view, "ยกเลิก", "ยกเลิกและล้างข้อมูลแล้ว")
            self.go_back_to_specimen()
    
    def go_back_to_specimen(self):
        """Navigate back to Specimen page"""
        if self.main_window and hasattr(self.main_window, 'specimen_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.specimen_widget)
        else:
            print("Warning: Cannot navigate back to specimen page")
    
    def go_back_to_new_work(self):
        """Navigate back to New Work page and refresh data"""
        if self.main_window and hasattr(self.main_window, 'add_work_widget'):
            self.main_window.ui.stackedWidget.setCurrentWidget(self.main_window.add_work_widget)
            
            # ✅ Refresh/update treewidget data when returning to New Work page
            if hasattr(self.main_window, 'new_work_controller') and self.main_window.new_work_controller:
                self.main_window.new_work_controller.update_treewidget_data()
        else:
            print("Warning: Cannot navigate back to new work page")
    
    # ========== ENABLE/DISABLE FUNCTIONS ==========
    
    def enable_bacteria_widgets(self):
        """Enable all bacteria widgets"""
        self.view.ui.bacteria_sample_frame.setEnabled(True)
        self.view.ui.bacteria_sensitivity_frame.setEnabled(True)
        self.view.ui.bacteria_identification_frame.setEnabled(True)
        self.view.ui.bacteria_request_frame.setEnabled(True)
        self.view.ui.bacteria_remark_frame.setEnabled(True)
        self.view.ui.bacteria_pay_frame.setEnabled(True)
    
    def disable_bacteria_widgets(self):
        """Disable all bacteria widgets"""
        self.view.ui.bacteria_sample_frame.setEnabled(False)
        self.view.ui.bacteria_sensitivity_frame.setEnabled(False)
        self.view.ui.bacteria_identification_frame.setEnabled(False)
        self.view.ui.bacteria_request_frame.setEnabled(False)
        self.view.ui.bacteria_remark_frame.setEnabled(False)
        self.view.ui.bacteria_pay_frame.setEnabled(False)
    
    # ========== DATABASE CONNECTION ==========
    
    def connect_database(self):
        """Connect to SQL Server database"""
        connection_string = (
            "DRIVER={SQL Server};"
            "SERVER=your_server_name;"
            "DATABASE=your_database_name;"
            "UID=your_username;"
            "PWD=your_password;"
        )
        return pyodbc.connect(connection_string)