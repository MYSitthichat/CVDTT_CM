from PySide6.QtWidgets import QWidget, QLineEdit, QPlainTextEdit
from PySide6.QtCore import Qt, QDate, QTime
from datetime import datetime, timezone, timedelta
# Ensure this import matches your folder structure
from View.template_from_ui.after_death import Ui_after_death_MainWindow as Ui_AfterDeathPage

class AfterDeathPageWidget(QWidget):
    """ 
    Wrapper view for the After Death Service Page. 
    """

    def __init__(self, parent=None):
        super(AfterDeathPageWidget, self).__init__(parent)
        self.ui = Ui_AfterDeathPage()
        self.ui.setupUi(self)

        # --- CHANGED ---
        # I removed the QVBoxLayout code. 
        # Now it will use the exact positions (geometry) you set in Qt Designer.
        
        # I also removed the "update_ui_state" logic.
        # Now all group boxes will remain visible, exactly like your design.
    
    def hideEvent(self, event):
        """Called when widget is hidden - clear the form"""
        super().hideEvent(event)
        self.clear_page()
    
    def closeEvent(self, event):
        """Called when widget is closed - clear the form"""
        super().closeEvent(event)
        self.clear_page()

    def get_data(self):
        """
        Extracts ONLY filled data from the UI.
        Returns a dictionary with non-empty values only.
        NOW SUPPORTS MULTIPLE SERVICE TYPES (CheckBoxes instead of RadioButtons)
        """
        data = {}
        
        # Collect all checked service types
        service_types = []
        
        # Check Infectious Waste
        if self.ui.rb_waste.isChecked():
            service_types.append('Infectious Waste')
            waste_details = self._get_waste_data()
            if waste_details:  # Only add if there's actual data
                data['waste_details'] = waste_details
        
        # Check Cremation
        if self.ui.rb_cremation.isChecked():
            service_types.append('Cremation')
            cremation_details = self._get_cremation_data()
            if cremation_details:  # Only add if there's actual data
                data['cremation_details'] = cremation_details
        
        # Check Jewelry (note: rb_jewelrya is the actual widget name from UI)
        if self.ui.rb_jewelrya.isChecked():
            service_types.append('Jewelry')
            jewelry_details = self._get_jewelry_data()
            if jewelry_details:  # Only add if there's actual data
                data['jewelry_details'] = jewelry_details
        
        # Set service_type as comma-separated list of selected services
        if service_types:
            data['service_type'] = ', '.join(service_types)
        else:
            data['service_type'] = 'Unknown'
        
        # CRITICAL: Old system ALWAYS reads field3-8 for ALL service types (lines 313-331)
        # This includes date/time/weight/checkboxes regardless of which service is selected
        if 'cremation_details' not in data:
            data['cremation_details'] = {}
        
        # field2: Incineration checkbox - ACTUALLY conditional in old system? But database shows always filled
        # Let's make it conditional: IF checked THEN text ELSE ''
        data['cremation_details']['incineration'] = self.ui.cb_incineration.text() if self.ui.cb_incineration.isChecked() else ''
        
        # field3: Weight - ALWAYS (old system line 314)
        data['cremation_details']['weight'] = self.ui.le_incineration_kg.text().strip()
        
        # field4: Bone storage checkbox - IF checked THEN text ELSE '' (old system lines 316-319)
        data['cremation_details']['bone_storage'] = self.ui.cb_bone_storage.text() if self.ui.cb_bone_storage.isChecked() else ''
        
        # field5: Ceremony checkbox - IF checked THEN text ELSE '' (old system lines 321-324)
        data['cremation_details']['ceremony'] = self.ui.cb_ceremony.text() if self.ui.cb_ceremony.isChecked() else ''
        
        # field6-7: Date/time - ALWAYS (old system lines 325-326)
        # Format: DD/MM/YYYY for date, HH:mm for time (24-hour)
        data['cremation_details']['date'] = self.ui.dateEdit.date().toString('dd/MM/yyyy')
        data['cremation_details']['time'] = self.ui.timeEdit.time().toString('HH:mm')
        
        # field8: Diamond checkbox - IF checked THEN text ELSE '' (old system lines 328-331)
        data['cremation_details']['diamond'] = self.ui.cb_diamond_mem.text() if self.ui.cb_diamond_mem.isChecked() else ''
        
        # field9-11: Carcass condition checkboxes - IF checked THEN text ELSE '' (old system lines 333-346)
        data['cremation_details']['carcass_fresh'] = self.ui.rb_fresh.text() if self.ui.rb_fresh.isChecked() else ''
        data['cremation_details']['carcass_autolysis'] = self.ui.rb_autolysis.text() if self.ui.rb_autolysis.isChecked() else ''
        data['cremation_details']['carcass_unknown'] = self.ui.rb_unknown.text() if self.ui.rb_unknown.isChecked() else ''
        
        # field12: Other carcass condition - ALWAYS (old system line 348)
        data['cremation_details']['carcass_other'] = self.ui.le_other_cond.text().strip()
        
        # field13: Necropsy hall checkbox - IF checked THEN text ELSE '' (old system lines 350-353)
        data['cremation_details']['place_necropsy'] = self.ui.cb_necropsy.text() if self.ui.cb_necropsy.isChecked() else ''
        
        # field14: le_place_opt1 - Extract from the line edit widget (it exists in UI)
        data['cremation_details']['place_other1'] = self.ui.le_place_opt1.text().strip()
        
        # field15: le_remark_lab - ALWAYS extract (for all service types)
        data['cremation_details']['remark'] = self.ui.le_remark_lab.text().strip()
        
        return data

    def _get_waste_data(self):
        """Extract ONLY filled Infectious Waste Data"""
        data = {}
        items = []
        
        # Tissues - USE CHECKBOX .text() PROPERTY (matches old system)
        if self.ui.cb_tissues.isChecked():
            qty = self.ui.le_tissues_qty.text().strip()
            weight = self.ui.le_tissues_w.text().strip()
            if qty or weight:  # Only add if at least one field is filled
                # Store checkbox text (e.g., "เนื้อเยื่อติดเชื้อ(Infectious Tissues)")
                item_str = self.ui.cb_tissues.text() + ":"
                if qty:
                    item_str += f" {qty} qty"
                if weight:
                    item_str += f" {weight} kg"
                items.append(item_str)
        
        # Needle - USE CHECKBOX .text() PROPERTY
        if self.ui.cb_needle.isChecked():
            qty = self.ui.le_needle_qty.text().strip()
            weight = self.ui.le_needle_w.text().strip()
            if qty or weight:
                item_str = self.ui.cb_needle.text() + ":"
                if qty:
                    item_str += f" {qty} qty"
                if weight:
                    item_str += f" {weight} kg"
                items.append(item_str)
        
        # Syringe - USE CHECKBOX .text() PROPERTY
        if self.ui.cb_syringe.isChecked():
            qty = self.ui.le_syringe_qty.text().strip()
            weight = self.ui.le_syringe_w.text().strip()
            if qty or weight:
                item_str = self.ui.cb_syringe.text() + ":"
                if qty:
                    item_str += f" {qty} qty"
                if weight:
                    item_str += f" {weight} kg"
                items.append(item_str)
        
        # Other 1 - USE LINE EDIT TEXT (since checkbox has no text)
        if self.ui.cb_inf_other1.isChecked():
            name = self.ui.le_inf_other1_name.text().strip()
            qty = self.ui.le_inf_other1_qty.text().strip()
            weight = self.ui.le_inf_other1_w.text().strip()
            if name or qty or weight:
                item_str = f"{name if name else 'Other'}:"
                if qty:
                    item_str += f" {qty} qty"
                if weight:
                    item_str += f" {weight} kg"
                items.append(item_str)
        
        # Other 2 - USE LINE EDIT TEXT (since checkbox has no text)
        if self.ui.cb_inf_other2.isChecked():
            name = self.ui.le_inf_other2_name.text().strip()
            qty = self.ui.le_inf_other2_qty.text().strip()
            weight = self.ui.le_inf_other2_w.text().strip()
            if name or qty or weight:
                item_str = f"{name if name else 'Other2'}:"
                if qty:
                    item_str += f" {qty} qty"
                if weight:
                    item_str += f" {weight} kg"
                items.append(item_str)
        
        # Only add items if there are any
        if items:
            data['items'] = items
        
        # Remark (only if not empty)
        remark = self.ui.le_inf_remark.text().strip()
        if remark:
            data['remark'] = remark
        
        return data if data else None  # Return None if no data at all

    def _get_cremation_data(self):
        """Extract ONLY filled Cremation Data"""
        data = {}
        
        # Request types (can now have multiple checked)
        req_types = []
        if self.ui.cb_incineration.isChecked():
            req_type = "Incineration"
            # Get weight if filled
            weight = self.ui.le_incineration_kg.text().strip()
            if weight:
                req_type += f" ({weight} kg)"
            req_types.append(req_type)
        
        if self.ui.cb_bone_storage.isChecked():
            req_types.append("Bone Storage")
        
        if self.ui.cb_ceremony.isChecked():
            req_types.append("Ceremony")
        
        if self.ui.cb_diamond_mem.isChecked():
            req_types.append("Diamond Memory")
        
        # Join multiple request types or use first one
        if req_types:
            data['request_type'] = ", ".join(req_types)
        
        # Date and Time (only if filled and not default)
        date = self.ui.dateEdit.text().strip()
        time = self.ui.timeEdit.text().strip()
        if date and date not in ["", "01/01/2000"]:  # Skip default date
            data['date'] = date
        if time and time not in ["", "00:00:00", "00:00"]:  # Skip default time
            data['time'] = time
        
        # Carcass condition
        condition = None
        if self.ui.rb_fresh.isChecked():
            condition = "Fresh"
        elif self.ui.rb_autolysis.isChecked():
            condition = "Autolysis"
        elif self.ui.rb_unknown.isChecked():
            condition = "Unknown"
        elif self.ui.rb_other_cond.isChecked():
            other_cond = self.ui.le_other_cond.text().strip()
            if other_cond:
                condition = other_cond
            else:
                condition = "Other"
        
        if condition:
            data['condition'] = condition
        
        # Place (can now have multiple)
        places = []
        if self.ui.cb_necropsy.isChecked():
            places.append("Necropsy Hall")
        
        if self.ui.cb_place_opt1.isChecked():
            custom_place = self.ui.le_place_opt1.text().strip()
            if custom_place:
                places.append(custom_place)
            else:
                places.append("Custom Location")
        
        if places:
            data['place'] = ", ".join(places)
        
        # Remark (only if not empty)
        remark = self.ui.le_remark_lab.text().strip()
        if remark:
            data['remark'] = remark
        
        return data if data else None

    def _get_jewelry_data(self):
        """Extract ONLY filled Jewelry Data"""
        data = {}
        
        # Store materials with separate checkbox text and qty/weight
        materials = {}
        
        # Carcass
        if self.ui.cb_gem_carcass.isChecked():
            materials['carcass'] = {
                'text': self.ui.cb_gem_carcass.text(),
                'qty': self.ui.le_gem_carcass_qty.text().strip(),
                'weight': self.ui.le_gem_carcass_w.text().strip()
            }
        
        # Bone
        if self.ui.cb_gem_bone.isChecked():
            materials['bone'] = {
                'text': self.ui.cb_gem_bone.text(),
                'qty': self.ui.le_gem_bone_qty.text().strip(),
                'weight': self.ui.le_gem_bone_w.text().strip()
            }
        
        # Hair
        if self.ui.cb_gem_hair.isChecked():
            materials['hair'] = {
                'text': self.ui.cb_gem_hair.text(),
                'qty': self.ui.le_gem_hair_qty.text().strip(),
                'weight': self.ui.le_gem_hair_w.text().strip()
            }
        
        # Other1
        if self.ui.cb_gem_other1.isChecked():
            materials['other1'] = {
                'text': self.ui.le_gem_other1_name.text().strip() or 'Other1',
                'qty': self.ui.le_gem_other1_qty.text().strip(),
                'weight': self.ui.le_gem_other1_w.text().strip()
            }
        
        # Other2
        if self.ui.cb_gem_other2.isChecked():
            materials['other2'] = {
                'text': self.ui.le_gem_other2_name.text().strip() or 'Other2',
                'qty': self.ui.le_gem_other2_qty.text().strip(),
                'weight': self.ui.le_gem_other2_w.text().strip()
            }
        
        if materials:
            data['materials'] = materials
        
        # Sizes (can now have multiple checked) - USE CHECKBOX .text() PROPERTY
        sizes = []
        if self.ui.cb_size_lt1.isChecked():
            sizes.append(self.ui.cb_size_lt1.text())  # "<1 carat (4700)"
        if self.ui.cb_size_1c.isChecked():
            sizes.append(self.ui.cb_size_1c.text())  # "1 carat 6.4 mm (5800)"
        if self.ui.cb_size_2c.isChecked():
            sizes.append(self.ui.cb_size_2c.text())  # "2 carat 8.1 mm (6800)"
        if self.ui.cb_size_3c.isChecked():
            sizes.append(self.ui.cb_size_3c.text())  # "3 carat 9.3 mm (7900)"
        if self.ui.cb_size_4c.isChecked():
            sizes.append(self.ui.cb_size_4c.text())  # "4 carat 10.2 mm (9000)"
        if self.ui.cb_size_5c.isChecked():
            sizes.append(self.ui.cb_size_5c.text())  # "5 carat 11.0 mm (10100)"
        
        if sizes:
            data['size'] = ", ".join(sizes)
        
        # Shapes (can now have multiple checked) - USE CHECKBOX .text() PROPERTY
        shapes = []
        if self.ui.cb_shape_round.isChecked():
            shapes.append(self.ui.cb_shape_round.text())  # "กลม(round)"
        if self.ui.cb_shape_oval.isChecked():
            shapes.append(self.ui.cb_shape_oval.text())  # "รี(oval)"
        if self.ui.cb_shape_cushion.isChecked():
            shapes.append(self.ui.cb_shape_cushion.text())  # "ทรงหมอน(cushion)"
        if self.ui.cb_shape_princess.isChecked():
            shapes.append(self.ui.cb_shape_princess.text())  # "สี่เหลี่ยม(princess)"
        if self.ui.cb_shape_radiant.isChecked():
            shapes.append(self.ui.cb_shape_radiant.text())  # "สี่เหลี่ยมผืนผ้า(radiant)"
        if self.ui.cb_shape_marquise.isChecked():
            shapes.append(self.ui.cb_shape_marquise.text())  # "ทรงมาร์คีย์(marquise)"
        if self.ui.cb_shape_other.isChecked():
            other_shape = self.ui.le_shape_other.text().strip()
            if other_shape:
                shapes.append(other_shape)
            else:
                shapes.append(self.ui.cb_shape_other.text())  # "อื่นๆ"
        
        if shapes:
            data['shape'] = ", ".join(shapes)
        
        # Jewelry types (can now have multiple checked) - USE CHECKBOX .text() PROPERTY
        jewelry_types = []
        if self.ui.cb_acc_ring.isChecked():
            code = self.ui.le_acc_code1.text().strip()
            # Use checkbox text: "แหวน (ring)"
            jewelry_str = self.ui.cb_acc_ring.text()
            if code:
                jewelry_str += f" (Code: {code})"
            jewelry_types.append(jewelry_str)
        
        if self.ui.cb_acc_necklace.isChecked():
            code = self.ui.le_acc_code2.text().strip()
            # Use checkbox text: "สร้อยคอ (necklace)"
            jewelry_str = self.ui.cb_acc_necklace.text()
            if code:
                jewelry_str += f" (Code: {code})"
            jewelry_types.append(jewelry_str)
        
        if self.ui.cb_acc_earing.isChecked():
            code = self.ui.le_acc_code3.text().strip()
            # Use checkbox text: "ต่างหู (earing)"
            jewelry_str = self.ui.cb_acc_earing.text()
            if code:
                jewelry_str += f" (Code: {code})"
            jewelry_types.append(jewelry_str)
        
        if jewelry_types:
            data['jewelry_type'] = ", ".join(jewelry_types)
        
        # Color (only if not empty)
        color = self.ui.le_color.text().strip()
        if color:
            data['color'] = color
        
        # Price (only if not empty)
        price = self.ui.le_price.text().strip()
        if price:
            data['price'] = price
        
        # Remark (only if not empty)
        remark = self.ui.pte_remark_gem.toPlainText().strip()
        if remark:
            data['remark'] = remark
        
        return data if data else None

    def clear_page(self):
        """ Reset page fields """
        # Reset service type checkboxes - uncheck all (no default)
        self.ui.rb_waste.setChecked(False)
        self.ui.rb_cremation.setChecked(False)
        self.ui.rb_jewelrya.setChecked(False)
        
        # Set current Bangkok date/time (UTC+7)
        bangkok_tz = timezone(timedelta(hours=7))
        now = datetime.now(bangkok_tz)
        
        # Set date to current Bangkok date
        current_date = QDate(now.year, now.month, now.day)
        self.ui.dateEdit.setDate(current_date)
        
        # Set time to current Bangkok time
        current_time = QTime(now.hour, now.minute)
        self.ui.timeEdit.setTime(current_time)
        
        # Clear all line edits
        for le in self.findChildren(QLineEdit):
            le.clear()
        
        # Clear plain text edit
        self.ui.pte_remark_gem.clear()
        
        # Uncheck all checkboxes
        if hasattr(self.ui, 'cb_tissues'):
            self.ui.cb_tissues.setChecked(False)
        if hasattr(self.ui, 'cb_needle'):
            self.ui.cb_needle.setChecked(False)
        if hasattr(self.ui, 'cb_syringe'):
            self.ui.cb_syringe.setChecked(False)
        if hasattr(self.ui, 'cb_inf_other1'):
            self.ui.cb_inf_other1.setChecked(False)
        if hasattr(self.ui, 'cb_inf_other2'):
            self.ui.cb_inf_other2.setChecked(False)
        
        # Gem checkboxes
        if hasattr(self.ui, 'cb_gem_carcass'):
            self.ui.cb_gem_carcass.setChecked(False)
        if hasattr(self.ui, 'cb_gem_bone'):
            self.ui.cb_gem_bone.setChecked(False)
        if hasattr(self.ui, 'cb_gem_hair'):
            self.ui.cb_gem_hair.setChecked(False)
        if hasattr(self.ui, 'cb_gem_other1'):
            self.ui.cb_gem_other1.setChecked(False)
        if hasattr(self.ui, 'cb_gem_other2'):
            self.ui.cb_gem_other2.setChecked(False)
        
        # Lab request checkboxes
        if hasattr(self.ui, 'cb_incineration'):
            self.ui.cb_incineration.setChecked(False)
        if hasattr(self.ui, 'cb_bone_storage'):
            self.ui.cb_bone_storage.setChecked(False)
        if hasattr(self.ui, 'cb_ceremony'):
            self.ui.cb_ceremony.setChecked(False)
        if hasattr(self.ui, 'cb_diamond_mem'):
            self.ui.cb_diamond_mem.setChecked(False)
        if hasattr(self.ui, 'cb_necropsy'):
            self.ui.cb_necropsy.setChecked(False)
        if hasattr(self.ui, 'cb_place_opt1'):
            self.ui.cb_place_opt1.setChecked(False)
        
        # Uncheck radio buttons for condition, size, shape, accessories
        if hasattr(self.ui, 'rb_fresh'):
            self.ui.rb_fresh.setChecked(False)
        if hasattr(self.ui, 'rb_autolysis'):
            self.ui.rb_autolysis.setChecked(False)
        if hasattr(self.ui, 'rb_unknown'):
            self.ui.rb_unknown.setChecked(False)
        if hasattr(self.ui, 'rb_other_cond'):
            self.ui.rb_other_cond.setChecked(False)
        
        # Size checkboxes
        if hasattr(self.ui, 'cb_size_lt1'):
            self.ui.cb_size_lt1.setChecked(False)
        if hasattr(self.ui, 'cb_size_1c'):
            self.ui.cb_size_1c.setChecked(False)
        if hasattr(self.ui, 'cb_size_2c'):
            self.ui.cb_size_2c.setChecked(False)
        if hasattr(self.ui, 'cb_size_3c'):
            self.ui.cb_size_3c.setChecked(False)
        if hasattr(self.ui, 'cb_size_4c'):
            self.ui.cb_size_4c.setChecked(False)
        if hasattr(self.ui, 'cb_size_5c'):
            self.ui.cb_size_5c.setChecked(False)
        
        # Shape checkboxes
        if hasattr(self.ui, 'cb_shape_round'):
            self.ui.cb_shape_round.setChecked(False)
        if hasattr(self.ui, 'cb_shape_oval'):
            self.ui.cb_shape_oval.setChecked(False)
        if hasattr(self.ui, 'cb_shape_cushion'):
            self.ui.cb_shape_cushion.setChecked(False)
        if hasattr(self.ui, 'cb_shape_princess'):
            self.ui.cb_shape_princess.setChecked(False)
        if hasattr(self.ui, 'cb_shape_radiant'):
            self.ui.cb_shape_radiant.setChecked(False)
        if hasattr(self.ui, 'cb_shape_marquise'):
            self.ui.cb_shape_marquise.setChecked(False)
        if hasattr(self.ui, 'cb_shape_other'):
            self.ui.cb_shape_other.setChecked(False)
        
        # Accessories checkboxes
        if hasattr(self.ui, 'cb_acc_ring'):
            self.ui.cb_acc_ring.setChecked(False)
        if hasattr(self.ui, 'cb_acc_necklace'):
            self.ui.cb_acc_necklace.setChecked(False)
        if hasattr(self.ui, 'cb_acc_earing'):
            self.ui.cb_acc_earing.setChecked(False)