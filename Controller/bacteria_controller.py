from View.view_bacteria_frame import bacterieFrameView
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox
import pyodbc
from datetime import datetime


class BacteriaController(QObject):
    """Controller for Bacteria Biology Page - mimicking lab_manager structure"""
    
    def __init__(self, view: bacterieFrameView, parent=None):
        super().__init__(parent)
        self.view = view
        self.main_window = parent  # Store reference to main window
        self.bind_bacteria_events()
    
    def bind_bacteria_events(self):
        """Bind all bacteria page button events"""
        # Main buttons - CORRECTED NAMES
        self.view.ui.bacteria_cal_pushButton.clicked.connect(self.calculate_bacteria_summary)
        self.view.ui.bacteria_save_pushButton.clicked.connect(self.save_all_bacteria_data)
        self.view.ui.bacteria_cancel_pushButton.clicked.connect(self.cancel_bacteria)
    
    # ========== SAMPLE PREPARATION FUNCTIONS ==========
    
    def get_sample_preparation_data(self):
        """Get sample preparation data - CORRECTED WIDGET NAMES"""
        samples = {}
        
        # All sample checkboxes and their corresponding lineEdits
        if self.view.ui.bacteria_swabLT_checkBox.isChecked():
            samples['swabLT'] = self.view.ui.bacteria_swabLT_lineEdit.text()
        if self.view.ui.bacteria_swabRT_checkBox.isChecked():
            samples['swabRT'] = self.view.ui.bacteria_swabRT_lineEdit.text()
        if self.view.ui.bacteria_wound_checkBox.isChecked():
            samples['wound'] = self.view.ui.bacteria_wound_lineEdit.text()
        if self.view.ui.bacteria_aspirateLT_checkBox.isChecked():
            samples['aspirateLT'] = self.view.ui.bacteria_aspirateLT_lineEdit.text()
        if self.view.ui.bacteria_aspirateRT_checkBox.isChecked():
            samples['aspirateRT'] = self.view.ui.bacteria_aspirateRT_lineEdit.text()
        if self.view.ui.bacteria_urine_checkBox.isChecked():
            samples['urine'] = self.view.ui.bacteria_urine_lineEdit.text()
        if self.view.ui.bacteria_midstream_checkBox.isChecked():
            samples['midstream'] = self.view.ui.bacteria_midstream_lineEdit.text()
        if self.view.ui.bacteria_catheterization_checkBox.isChecked():
            samples['catheterization'] = self.view.ui.bacteria_catheterization_lineEdit.text()
        if self.view.ui.bacteria_cystocentesis_checkBox.isChecked():
            samples['cystocentesis'] = self.view.ui.bacteria_cystocentesis_lineEdit.text()
        if self.view.ui.bacteria_tissuesLT_checkBox.isChecked():
            samples['tissuesLT'] = self.view.ui.bacteria_tissuesLT_lineEdit.text()
        if self.view.ui.bacteria_tissuesRT_checkBox.isChecked():
            samples['tissuesRT'] = self.view.ui.bacteria_tissuesRT_lineEdit.text()
        if self.view.ui.bacteria_biopsyLT_checkBox.isChecked():
            samples['biopsyLT'] = self.view.ui.bacteria_biopsyLT_lineEdit.text()
        if self.view.ui.bacteria_biopsyRT_checkBox.isChecked():
            samples['biopsyRT'] = self.view.ui.bacteria_biopsyRT_lineEdit.text()
        if self.view.ui.bacteria_bodyFluidLT_checkBox.isChecked():
            samples['bodyFluidLT'] = self.view.ui.bacteria_bodyFluidLT_lineEdit.text()
        if self.view.ui.bacteria_bodyFluidRT_checkBox.isChecked():
            samples['bodyFluidRT'] = self.view.ui.bacteria_bodyFluidRT_lineEdit.text()
        if self.view.ui.bacteria_csf_checkBox.isChecked():
            samples['csf'] = self.view.ui.bacteria_csf_lineEdit.text()
        if self.view.ui.bacteria_feces_checkBox.isChecked():
            samples['feces'] = self.view.ui.bacteria_feces_lineEdit.text()
        if self.view.ui.bacteria_pus_checkBox.isChecked():
            samples['pus'] = self.view.ui.bacteria_pus_lineEdit.text()
        if self.view.ui.bacteria_blood_checkBox.isChecked():
            samples['blood'] = self.view.ui.bacteria_blood_lineEdit.text()
        if self.view.ui.bacteria_bloodAgar_checkBox.isChecked():
            samples['bloodAgar'] = self.view.ui.bacteria_bloodAgar_lineEdit.text()
        if self.view.ui.bacteria_skinScaping_checkBox.isChecked():
            samples['skinScaping'] = self.view.ui.bacteria_skinScaping_lineEdit.text()
        
        return samples
    
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
    
    # ========== DRUG SENSITIVITY FUNCTIONS ==========
    
    def get_drug_sensitivity_data(self):
        """Get drug sensitivity test data - CORRECTED"""
        drugs = []
        
        # All antibiotic checkboxes - CORRECTED NAMES
        if self.view.ui.bacteria_amikacin_checkBox.isChecked():
            drugs.append('Amikacin')
        if self.view.ui.bacteria_ampicillin_checkBox.isChecked():
            drugs.append('Ampicillin')
        if self.view.ui.bacteria_ceftazidime_checkBox.isChecked():
            drugs.append('Ceftazidime')
        if self.view.ui.bacteria_cephalexin_checkBox.isChecked():
            drugs.append('Cephalexin')
        if self.view.ui.bacteria_chloramphenicol_checkBox.isChecked():
            drugs.append('Chloramphenicol')
        if self.view.ui.bacteria_cloxacillin_checkBox.isChecked():
            drugs.append('Cloxacillin')
        if self.view.ui.bacteria_enrofloxacin_checkBox.isChecked():
            drugs.append('Enrofloxacin')
        if self.view.ui.bacteria_gentamycin_checkBox.isChecked():
            drugs.append('Gentamycin')
        if self.view.ui.bacteria_lincomycin_checkBox.isChecked():
            drugs.append('Lincomycin')
        if self.view.ui.bacteria_norfloxacin_checkBox.isChecked():
            drugs.append('Norfloxacin')
        if self.view.ui.bacteria_oxacillin_checkBox.isChecked():
            drugs.append('Oxacillin')
        if self.view.ui.bacteria_polymyxcinB_checkBox.isChecked():
            drugs.append('PolymyxcinB')
        if self.view.ui.bacteria_sulfa_trimetroprom_checkBox.isChecked():
            drugs.append('Sulfa-Trimetroprom')
        if self.view.ui.bacteria_vancomycin_checkBox.isChecked():
            drugs.append('Vancomycin')
        
        # Column 2
        if self.view.ui.bacteria_amoxycillin_checkBox.isChecked():
            drugs.append('Amoxycillin')
        if self.view.ui.bacteria_bactracin_checkBox.isChecked():
            drugs.append('Bactracin')
        if self.view.ui.bacteria_ceftiofur_checkBox.isChecked():
            drugs.append('Ceftiofur')
        if self.view.ui.bacteria_cephalothin_checkBox.isChecked():
            drugs.append('Cephalothin')
        if self.view.ui.bacteria_ciprofloxacin_checkBox.isChecked():
            drugs.append('Ciprofloxacin')
        if self.view.ui.bacteria_colistin_checkBox.isChecked():
            drugs.append('Colistin')
        if self.view.ui.bacteria_erythromycin_checkBox.isChecked():
            drugs.append('Erythromycin')
        if self.view.ui.bacteria_imipenem_checkBox.isChecked():
            drugs.append('Imipenem')
        if self.view.ui.bacteria_neomycin_checkBox.isChecked():
            drugs.append('Neomycin')
        if self.view.ui.bacteria_novobiocin_checkBox.isChecked():
            drugs.append('Novobiocin')
        if self.view.ui.bacteria_oxytetracycline_checkBox.isChecked():
            drugs.append('Oxytetracycline')
        if self.view.ui.bacteria_rifampicin_checkBox.isChecked():
            drugs.append('Rifampicin')
        if self.view.ui.bacteria_tetracycline_checkBox.isChecked():
            drugs.append('Tetracycline')
        
        # Column 3
        if self.view.ui.bacteria_amoxy_checkBox.isChecked():
            drugs.append('Amoxy')
        if self.view.ui.bacteria_clav_checkBox.isChecked():
            drugs.append('Clav')
        if self.view.ui.bacteria_ceftriaxone_checkBox.isChecked():
            drugs.append('Ceftriaxone')
        if self.view.ui.bacteria_cephazolin_checkBox.isChecked():
            drugs.append('Cephazolin')
        if self.view.ui.bacteria_clindamicin_checkBox.isChecked():
            drugs.append('Clindamicin')
        if self.view.ui.bacteria_doxycycline_checkBox.isChecked():
            drugs.append('Doxycycline')
        if self.view.ui.bacteria_fosfomycin_checkBox.isChecked():
            drugs.append('Fosfomycin')
        if self.view.ui.bacteria_kanamycin_checkBox.isChecked():
            drugs.append('Kanamycin')
        if self.view.ui.bacteria_nitrofurantoin_checkBox.isChecked():
            drugs.append('Nitrofurantoin')
        if self.view.ui.bacteria_optocin_checkBox.isChecked():
            drugs.append('Optocin')
        if self.view.ui.bacteria_penicillin_checkBox.isChecked():
            drugs.append('Penicillin')
        if self.view.ui.bacteria_streptomycin_checkBox.isChecked():
            drugs.append('Streptomycin')
        if self.view.ui.bacteria_tobramycin_checkBox.isChecked():
            drugs.append('Tobramycin')
        
        # Other
        if self.view.ui.bacteria_other_sen_checkBox.isChecked():
            other_drug = self.view.ui.bacteria_other_sen_lineEdit.text()
            if other_drug:
                drugs.append(f'Other: {other_drug}')
        
        return drugs
    
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
        """Get bacterial identification data - CORRECTED"""
        bacteria = []
        
        if self.view.ui.bacteria_actinobacillus_checkBox.isChecked():
            bacteria.append('Actinobacillus spp.')
        if self.view.ui.bacteria_corynebacterium_checkBox.isChecked():
            bacteria.append('Corynebacterium spp.')
        if self.view.ui.bacteria_klebsiella_checkBox.isChecked():
            bacteria.append('Klebsiella spp.')
        if self.view.ui.bacteria_streptococcus_checkBox.isChecked():
            bacteria.append('Streptococcus spp.')
        if self.view.ui.bacteria_aeromonas_checkBox.isChecked():
            bacteria.append('Aeromonas spp.')
        if self.view.ui.bacteria_enterobacter_checkBox.isChecked():
            bacteria.append('Enterobacter spp.')
        if self.view.ui.bacteria_pasteurella_checkBox.isChecked():
            bacteria.append('Pasteurella spp.')
        if self.view.ui.bacteria_staphylococcus_checkBox.isChecked():
            bacteria.append('Staphylococcus spp.')
        if self.view.ui.bacteria_bordetella_checkBox.isChecked():
            bacteria.append('Bordetella spp.')
        if self.view.ui.bacteria_escherichia_checkBox.isChecked():
            bacteria.append('Escherichia coli')
        if self.view.ui.bacteria_salmonella_checkBox.isChecked():
            bacteria.append('Salmonella spp.')
        if self.view.ui.bacteria_other_iden_checkBox.isChecked():
            other = self.view.ui.bacteria_other_iden_lineEdit.text()
            if other:
                bacteria.append(f'Other: {other}')
        
        return bacteria
    
    def save_bacterial_identification(self):
        """Save bacterial identification data"""
        try:
            bacteria = self.get_bacterial_identification_data()
            
            if not bacteria:
                QMessageBox.warning(self.view, "คำเตือน", "กรุณาเลือกเชื้อแบคทีเรียอย่างน้อย 1 รายการ!")
                return
            
            connection = self.connect_database()
            cursor = connection.cursor()
            
            import json
            bacteria_json = json.dumps(bacteria)
            
            sql = """
            INSERT INTO bacteria_identification 
            (bacteria_data, created_date)
            VALUES (?, ?)
            """
            
            cursor.execute(sql, (bacteria_json, datetime.now()))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            QMessageBox.information(self.view, "สำเร็จ", "บันทึกข้อมูลการระบุเชื้อแบคทีเรียสำเร็จ!")
            
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
    
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
        """Get laboratory request data - CORRECTED"""
        requests = []
        total_cost = 0
        
        if self.view.ui.bacteria_fungal_checkBox.isChecked():
            requests.append('Fungal culture and identification')
            total_cost += 250
        if self.view.ui.bacteria_Identification_and_sensitive__checkBox.isChecked():
            requests.append('Bacterial identification and drug sensitivity')
            total_cost += 250
        if self.view.ui.bacteria_VITEK2_MIC_checkBox.isChecked():
            requests.append('VITEK2 with MIC')
            total_cost += 950
        if self.view.ui.bacteria_VITEK2_checkBox.isChecked():
            requests.append('VITEK2 iden')
            total_cost += 550
        if self.view.ui.bacteria_MIC_checkBox.isChecked():
            requests.append('MIC')
            total_cost += 550
        
        return {'requests': requests, 'total_cost': total_cost}
    
    def save_laboratory_request(self):
        """Save laboratory request data"""
        try:
            data = self.get_laboratory_request_data()
            
            if not data['requests']:
                QMessageBox.warning(self.view, "คำเตือน", "กรุณาเลือกการตรวจอย่างน้อย 1 รายการ!")
                return
            
            connection = self.connect_database()
            cursor = connection.cursor()
            
            import json
            requests_json = json.dumps(data['requests'])
            
            sql = """
            INSERT INTO bacteria_laboratory_request 
            (requests_data, total_cost, created_date)
            VALUES (?, ?, ?)
            """
            
            cursor.execute(sql, (requests_json, data['total_cost'], datetime.now()))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            QMessageBox.information(self.view, "สำเร็จ", "บันทึกข้อมูลคำขอตรวจสำเร็จ!")
            
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
    
    def clear_laboratory_request(self):
        """Clear laboratory request fields - CORRECTED"""
        self.view.ui.bacteria_fungal_checkBox.setChecked(False)
        self.view.ui.bacteria_Identification_and_sensitive__checkBox.setChecked(False)
        self.view.ui.bacteria_VITEK2_MIC_checkBox.setChecked(False)
        self.view.ui.bacteria_VITEK2_checkBox.setChecked(False)
        self.view.ui.bacteria_MIC_checkBox.setChecked(False)
    
    # ========== SUMMARY FUNCTIONS ==========
    
    def calculate_bacteria_summary(self):
        """Calculate and display bacteria test summary - CORRECTED"""
        # Get all data
        samples = self.get_sample_preparation_data()
        drugs = self.get_drug_sensitivity_data()
        bacteria = self.get_bacterial_identification_data()
        lab_requests = self.get_laboratory_request_data()
        
        # Calculate totals
        total_tests = len(samples) + (1 if drugs else 0) + len(bacteria) + len(lab_requests['requests'])
        total_cost = lab_requests['total_cost']
        
        # Update display - CORRECTED WIDGET NAMES
        self.view.ui.bacteria_num_lineEdit.setText(str(total_tests))
        self.view.ui.bacteria_cost_lineEdit.setText(f"{total_cost:.2f}")
        
        QMessageBox.information(self.view, "สรุป", 
                              f"จำนวนการตรวจทั้งหมด: {total_tests}\n"
                              f"ค่าใช้จ่ายรวม: {total_cost:.2f} บาท")
    
    def get_bacteria_summary_data(self):
        """Get summary data - CORRECTED"""
        return {
            'total_tests': self.view.ui.bacteria_num_lineEdit.text(),
            'total_cost': self.view.ui.bacteria_cost_lineEdit.text(),
            'remark': self.view.ui._bacteria_remark_plainTextEdit.toPlainText()  # CORRECTED
        }
    
    # ========== SAVE ALL & CANCEL FUNCTIONS ==========
    
    def save_all_bacteria_data(self):
        """Save all bacteria page data at once"""
        try:
            # Validate
            samples = self.get_sample_preparation_data()
            if not samples:
                QMessageBox.warning(self.view, "คำเตือน", "กรุณาเลือกตัวอย่างอย่างน้อย 1 รายการ!")
                return
            
            # Save each section
            self.save_sample_preparation()
            self.save_drug_sensitivity()
            self.save_bacterial_identification()
            self.save_laboratory_request()
            
            # Save summary
            summary_data = self.get_bacteria_summary_data()
            
            connection = self.connect_database()
            cursor = connection.cursor()
            
            sql = """
            INSERT INTO bacteria_summary 
            (total_tests, total_cost, remark, created_date)
            VALUES (?, ?, ?, ?)
            """
            
            cursor.execute(sql, (
                summary_data['total_tests'],
                summary_data['total_cost'],
                summary_data['remark'],
                datetime.now()
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            QMessageBox.information(self.view, "สำเร็จ", "บันทึกข้อมูลทั้งหมดสำเร็จ!")
            self.clear_all_bacteria_information()
            self.go_back_to_new_work()  # ✅ Go back to New Work page instead of staying
            
        except Exception as e:
            QMessageBox.critical(self.view, "ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
    
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