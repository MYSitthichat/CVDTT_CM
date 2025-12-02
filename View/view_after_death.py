from PySide6.QtWidgets import QWidget, QLineEdit, QPlainTextEdit
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

    def get_data(self):
        """
        Extracts data from the UI based on the selected service.
        Returns a dictionary.
        """
        data = {}
        
        # Determine which main service is selected to tag the data
        if self.ui.rb_waste.isChecked():
            data['service_type'] = 'Infectious Waste'
        elif self.ui.rb_cremation.isChecked():
            data['service_type'] = 'Cremation'
        elif self.ui.rb_jewelry.isChecked():
            data['service_type'] = 'Jewelry'
        else:
            data['service_type'] = 'Unknown'

        # Collect data from ALL sections (since they are all visible now)
        data['waste_details'] = self._get_waste_data()
        data['cremation_details'] = self._get_cremation_data()
        data['jewelry_details'] = self._get_jewelry_data()
        
        return data

    def _get_waste_data(self):
        """ Extract Infectious Waste Data """
        info = []
        if self.ui.rb_tissues.isChecked():
            info.append(f"Tissues: {self.ui.le_tissues_qty.text()} qty, {self.ui.le_tissues_w.text()} kg")
        if self.ui.rb_needle.isChecked():
            info.append(f"Needle: {self.ui.le_needle_qty.text()} qty, {self.ui.le_needle_w.text()} kg")
        if self.ui.rb_syringe.isChecked():
            info.append(f"Syringe: {self.ui.le_syringe_qty.text()} qty, {self.ui.le_syringe_w.text()} kg")
        if self.ui.rb_inf_other1.isChecked():
            info.append(f"{self.ui.le_inf_other1_name.text()}: {self.ui.le_inf_other1_qty.text()} qty, {self.ui.le_inf_other1_w.text()} kg")
        
        return {
            'items': "; ".join(info),
            'remark': self.ui.le_inf_remark.text()
        }

    def _get_cremation_data(self):
        """ Extract Cremation Data """
        req_type = ""
        if self.ui.rb_incineration.isChecked(): req_type = f"Incineration ({self.ui.le_incineration_kg.text()} kg)"
        elif self.ui.rb_bone_storage.isChecked(): req_type = "Bone Storage"
        elif self.ui.rb_ceremony.isChecked(): req_type = "Ceremony"
        elif self.ui.rb_diamond_mem.isChecked(): req_type = "Diamond Memory"

        condition = ""
        if self.ui.rb_fresh.isChecked(): condition = "Fresh"
        elif self.ui.rb_autolysis.isChecked(): condition = "Autolysis"
        elif self.ui.rb_unknown.isChecked(): condition = "Unknown"
        elif self.ui.rb_other_cond.isChecked(): condition = self.ui.le_other_cond.text()

        place = "Necropsy Hall" if self.ui.rb_necropsy.isChecked() else self.ui.le_place_opt1.text()

        return {
            'request_type': req_type,
            'date': self.ui.dateEdit.text(),
            'time': self.ui.timeEdit.text(),
            'condition': condition,
            'place': place,
            'remark': self.ui.le_remark_lab.text()
        }

    def _get_jewelry_data(self):
        """ Extract Jewelry Data """
        material = ""
        if self.ui.rb_gem_carcass.isChecked(): material = "Carcass"
        elif self.ui.rb_gem_bone.isChecked(): material = "Bone"
        elif self.ui.rb_gem_hair.isChecked(): material = "Hair"
        
        size = "Unknown"
        if self.ui.rb_size_lt1.isChecked(): size = "<1 carat"
        elif self.ui.rb_size_1c.isChecked(): size = "1 carat"
        elif self.ui.rb_size_2c.isChecked(): size = "2 carat"
        
        shape = "Unknown"
        if self.ui.rb_shape_round.isChecked(): shape = "Round"
        elif self.ui.rb_shape_oval.isChecked(): shape = "Oval"

        return {
            'material': material,
            'size': size,
            'shape': shape,
            'color': self.ui.le_color.text(),
            'price': self.ui.le_price.text(),
            'remark': self.ui.pte_remark_gem.toPlainText()
        }

    def clear_page(self):
        """ Reset page fields """
        self.ui.rb_waste.setChecked(True)
        
        # Clear Line Edits
        for le in self.findChildren(QLineEdit):
            le.clear()
        self.ui.pte_remark_gem.clear()