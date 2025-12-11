from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QCheckBox, QLineEdit, QMessageBox
# Ensure this import matches where you save the generated file 'molecular.py'
from View.template_from_ui.molecular_biology import Ui_molecular_biology_MainWindow as Ui_MolecularBiologyPage

class MolecularBiologyPageWidget(QWidget):

    def __init__(self, parent=None):
        super(MolecularBiologyPageWidget, self).__init__(parent)
        self.ui = Ui_MolecularBiologyPage()
        
        dummy_main_window = QMainWindow()
        self.ui.setupUi(dummy_main_window)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.centralwidget)
        self.setLayout(layout)
        
        # Setup checkbox-lineEdit connections
        self._setup_checkbox_linedit_connections()
        
        # Clear summary on initialization
        self.set_summary(0, 0)

    def _setup_checkbox_linedit_connections(self):
        def connect_checkbox_to_lineedit(checkbox, lineedit):
            # Disable lineEdit by default
            lineedit.setEnabled(False)
            lineedit.setStyleSheet("background-color: #E0E0E0;")
            
            def on_checkbox_changed(state):
                if state:  # Checked
                    lineedit.setEnabled(True)
                    lineedit.setStyleSheet("background-color: #FFFFFF;")  # Reset to default style
                    lineedit.setFocus()  # Auto-focus for convenience
                else:  # Unchecked
                    lineedit.setEnabled(False)
                    lineedit.setStyleSheet("background-color: #E0E0E0;")
                    lineedit.clear()  # Clear text when unchecked
                
            checkbox.stateChanged.connect(on_checkbox_changed)
            # Note: No auto-update - summary updates only when Calculate button is pressed
        
        # --- Avian (1-12) ---
        for i in range(1, 13):
            cb = getattr(self.ui, f'c_av{i}', None)
            ed = getattr(self.ui, f'e_av{i}', None)
            if cb and ed:
                connect_checkbox_to_lineedit(cb, ed)

        # --- Blood Parasite 1 (1-8) ---
        for i in range(1, 9):
            cb = getattr(self.ui, f'c_bp1_{i}', None)
            ed = getattr(self.ui, f'e_bp1_{i}', None)
            if cb and ed:
                connect_checkbox_to_lineedit(cb, ed)

        # --- Blood Parasite 2 (1-8) ---
        for i in range(1, 9):
            cb = getattr(self.ui, f'c_bp2_{i}', None)
            ed = getattr(self.ui, f'e_bp2_{i}', None)
            if cb and ed:
                connect_checkbox_to_lineedit(cb, ed)

        # --- Feline (1-4) ---
        for i in range(1, 5):
            cb = getattr(self.ui, f'c_fe{i}', None)
            ed = getattr(self.ui, f'e_fe{i}', None)
            if cb and ed:
                connect_checkbox_to_lineedit(cb, ed)

        # --- Bovine (1-4) ---
        for i in range(1, 5):
            cb = getattr(self.ui, f'c_bv{i}', None)
            ed = getattr(self.ui, f'e_bv{i}', None)
            if cb and ed:
                connect_checkbox_to_lineedit(cb, ed)

        # --- Canine (1-2) ---
        for i in range(1, 3):
            cb = getattr(self.ui, f'c_cn{i}', None)
            ed = getattr(self.ui, f'e_cn{i}', None)
            if cb and ed:
                connect_checkbox_to_lineedit(cb, ed)

        # --- Elephant (1-5) ---
        for i in range(1, 6):
            cb = getattr(self.ui, f'c_el{i}', None)
            ed = getattr(self.ui, f'e_el{i}', None)
            if cb and ed:
                connect_checkbox_to_lineedit(cb, ed)

        # --- Aquatic (1-3) ---
        for i in range(1, 4):
            cb = getattr(self.ui, f'c_aq{i}', None)
            ed = getattr(self.ui, f'e_aq{i}', None)
            if cb and ed:
                connect_checkbox_to_lineedit(cb, ed)

        # --- Equine (1-2) ---
        for i in range(1, 3):
            cb = getattr(self.ui, f'c_eq{i}', None)
            ed = getattr(self.ui, f'e_eq{i}', None)
            if cb and ed:
                connect_checkbox_to_lineedit(cb, ed)

        # --- Others (1-11) ---
        for i in range(1, 12):
            cb = getattr(self.ui, f'c_ot{i}', None)
            ed = getattr(self.ui, f'e_ot{i}', None)
            if cb and ed:
                connect_checkbox_to_lineedit(cb, ed)
                
        if hasattr(self.ui, 'c_ot12'):
            cb = self.ui.c_ot12
            for lineedit_name in ['e_ot12_n', 'e_ot11_2', 'e_ot12_p']:
                ed = getattr(self.ui, lineedit_name, None)
                if ed:
                    ed.setEnabled(False)
                    ed.setStyleSheet("background-color: #E0E0E0;")
                    
            def on_ot12_changed(state):
                for lineedit_name in ['e_ot12_n', 'e_ot11_2', 'e_ot12_p']:
                    ed = getattr(self.ui, lineedit_name, None)
                    if ed:
                        if state:
                            ed.setEnabled(True)
                            ed.setStyleSheet("background-color: #FFFFFF;")
                        else:
                            ed.setEnabled(False)
                            ed.setStyleSheet("background-color: #E0E0E0;")
                            ed.clear()
                if state and hasattr(self.ui, 'e_ot12_n'):
                    self.ui.e_ot12_n.setFocus()
            
            cb.stateChanged.connect(on_ot12_changed)
            
        if hasattr(self.ui, 'c_ot13'):
            cb = self.ui.c_ot13
            for lineedit_name in ['e_ot13_n', 'e_ot11_3', 'e_ot13_p']:
                ed = getattr(self.ui, lineedit_name, None)
                if ed:
                    ed.setEnabled(False)
                    ed.setStyleSheet("background-color: #E0E0E0;")
                    
            def on_ot13_changed(state):
                for lineedit_name in ['e_ot13_n', 'e_ot11_3', 'e_ot13_p']:
                    ed = getattr(self.ui, lineedit_name, None)
                    if ed:
                        if state:
                            ed.setEnabled(True)
                            ed.setStyleSheet("background-color: #FFFFFF;")
                        else:
                            ed.setEnabled(False)
                            ed.setStyleSheet("background-color: #E0E0E0;")
                            ed.clear()
                if state and hasattr(self.ui, 'e_ot13_n'):
                    self.ui.e_ot13_n.setFocus()
            cb.stateChanged.connect(on_ot13_changed)

    def get_data(self):
        """
        Retrieves data from ALL checkboxes (selected and unselected).
        - Selected: quantity from input, total_price = unit_price (NOT calculated)
        - Unselected: quantity = 0, total_price = unit_price
        NOTE: total_price is ALWAYS unit_price, calculation will be done in database
        """
        all_items = []
        
        # Helper function to check a row - ALWAYS returns data
        def check_row(checkbox, entry_sample, price=0):
            # Get unit price from checkbox text
            unit_price = price if price > 0 else self._extract_price(checkbox.text())
            
            if checkbox.isChecked():
                # SELECTED: Get quantity from input
                sample_id = entry_sample.text().strip()
                quantity = 0
                if sample_id:
                    try:
                        quantity = int(sample_id)
                        if quantity < 0:
                            quantity = 0
                    except ValueError:
                        quantity = 0
            else:
                # UNSELECTED: quantity = 0
                sample_id = ""
                quantity = 0
            
            return {
                'name': checkbox.text(),
                'sample_id': sample_id,
                'unit_price': unit_price,
                'quantity': quantity,           # 0 if not selected, or from input
                'total_price': unit_price       # ALWAYS unit_price (will calculate in DB)
            }

        # --- Avian (1-12) ---
        for i in range(1, 13):
            cb = getattr(self.ui, f'c_av{i}')
            ed = getattr(self.ui, f'e_av{i}')
            all_items.append(check_row(cb, ed))

        # --- Blood Parasite 1 (1-8) ---
        for i in range(1, 9):
            cb = getattr(self.ui, f'c_bp1_{i}')
            ed = getattr(self.ui, f'e_bp1_{i}')
            all_items.append(check_row(cb, ed))

        # --- Blood Parasite 2 (1-8) ---
        for i in range(1, 9):
            cb = getattr(self.ui, f'c_bp2_{i}')
            ed = getattr(self.ui, f'e_bp2_{i}')
            all_items.append(check_row(cb, ed))

        # --- Feline (1-4) ---
        for i in range(1, 5):
            cb = getattr(self.ui, f'c_fe{i}')
            ed = getattr(self.ui, f'e_fe{i}')
            all_items.append(check_row(cb, ed))

        # --- Bovine (1-4) ---
        for i in range(1, 5):
            cb = getattr(self.ui, f'c_bv{i}')
            ed = getattr(self.ui, f'e_bv{i}')
            all_items.append(check_row(cb, ed))

        # --- Canine (1-2) ---
        for i in range(1, 3):
            cb = getattr(self.ui, f'c_cn{i}')
            ed = getattr(self.ui, f'e_cn{i}')
            all_items.append(check_row(cb, ed))

        # --- Elephant (1-5) ---
        for i in range(1, 6):
            cb = getattr(self.ui, f'c_el{i}')
            ed = getattr(self.ui, f'e_el{i}')
            all_items.append(check_row(cb, ed))

        # --- Aquatic (1-3) ---
        for i in range(1, 4):
            cb = getattr(self.ui, f'c_aq{i}')
            ed = getattr(self.ui, f'e_aq{i}')
            all_items.append(check_row(cb, ed))

        # --- Equine (1-2) ---
        for i in range(1, 3):
            cb = getattr(self.ui, f'c_eq{i}')
            ed = getattr(self.ui, f'e_eq{i}')
            all_items.append(check_row(cb, ed))

        # --- Others (1-11) ---
        for i in range(1, 12):
            cb = getattr(self.ui, f'c_ot{i}')
            ed = getattr(self.ui, f'e_ot{i}')
            all_items.append(check_row(cb, ed))

        # --- Custom Others 1 (c_ot12) ---
        # Get unit price
        price_text = self.ui.e_ot12_p.text().strip()
        try:
            unit_price = int(price_text) if price_text else 0
        except ValueError:
            unit_price = 0
        
        if self.ui.c_ot12.isChecked():
            # Selected: get quantity from input
            sample_id = self.ui.e_ot11_2.text().strip()
            quantity = 0
            if sample_id:
                try:
                    quantity = int(sample_id)
                    if quantity < 0:
                        quantity = 0
                except ValueError:
                    quantity = 0
        else:
            # Unselected: quantity = 0
            sample_id = ""
            quantity = 0
        
        all_items.append({
            'name': self.ui.e_ot12_n.text() or "Custom Test 1",
            'sample_id': sample_id,
            'unit_price': unit_price,
            'quantity': quantity,
            'total_price': unit_price  # ALWAYS unit_price
        })

        # --- Custom Others 2 (c_ot13) ---
        # Get unit price
        price_text = self.ui.e_ot13_p.text().strip()
        try:
            unit_price = int(price_text) if price_text else 0
        except ValueError:
            unit_price = 0
        
        if self.ui.c_ot13.isChecked():
            # Selected: get quantity from input
            sample_id = self.ui.e_ot11_3.text().strip()
            quantity = 0
            if sample_id:
                try:
                    quantity = int(sample_id)
                    if quantity < 0:
                        quantity = 0
                except ValueError:
                    quantity = 0
        else:
            # Unselected: quantity = 0
            sample_id = ""
            quantity = 0
        
        all_items.append({
            'name': self.ui.e_ot13_n.text() or "Custom Test 2",
            'sample_id': sample_id,
            'unit_price': unit_price,
            'quantity': quantity,
            'total_price': unit_price  # ALWAYS unit_price
        })

        return all_items

    def calculate_summary(self):
        # Validate: Check if any checkbox is selected but LineEdit is empty or invalid
        validation_errors = []
        
        # Helper function to validate a row
        def validate_row(checkbox, entry_sample, field_name):
            if checkbox.isChecked():
                sample_text = entry_sample.text().strip()
                if not sample_text:
                    validation_errors.append(f"{field_name}: กรุณาใส่จำนวน sample")
                else:
                    try:
                        quantity = int(sample_text)
                        if quantity <= 0:
                            validation_errors.append(f"{field_name}: จำนวน sample ต้องมากกว่า 0")
                    except ValueError:
                        validation_errors.append(f"{field_name}: กรุณาใส่ตัวเลขเท่านั้น")
        
        # Validate all fields
        for i in range(1, 13):
            cb = getattr(self.ui, f'c_av{i}', None)
            ed = getattr(self.ui, f'e_av{i}', None)
            if cb and ed:
                validate_row(cb, ed, f"Avian {i}")
        
        for i in range(1, 9):
            cb = getattr(self.ui, f'c_bp1_{i}', None)
            ed = getattr(self.ui, f'e_bp1_{i}', None)
            if cb and ed:
                validate_row(cb, ed, f"Blood Parasite 1-{i}")
        
        for i in range(1, 9):
            cb = getattr(self.ui, f'c_bp2_{i}', None)
            ed = getattr(self.ui, f'e_bp2_{i}', None)
            if cb and ed:
                validate_row(cb, ed, f"Blood Parasite 2-{i}")
        
        for i in range(1, 5):
            cb = getattr(self.ui, f'c_fe{i}', None)
            ed = getattr(self.ui, f'e_fe{i}', None)
            if cb and ed:
                validate_row(cb, ed, f"Feline {i}")
        
        for i in range(1, 5):
            cb = getattr(self.ui, f'c_bv{i}', None)
            ed = getattr(self.ui, f'e_bv{i}', None)
            if cb and ed:
                validate_row(cb, ed, f"Bovine {i}")
        
        for i in range(1, 3):
            cb = getattr(self.ui, f'c_cn{i}', None)
            ed = getattr(self.ui, f'e_cn{i}', None)
            if cb and ed:
                validate_row(cb, ed, f"Canine {i}")
        
        for i in range(1, 6):
            cb = getattr(self.ui, f'c_el{i}', None)
            ed = getattr(self.ui, f'e_el{i}', None)
            if cb and ed:
                validate_row(cb, ed, f"Elephant {i}")
        
        for i in range(1, 4):
            cb = getattr(self.ui, f'c_aq{i}', None)
            ed = getattr(self.ui, f'e_aq{i}', None)
            if cb and ed:
                validate_row(cb, ed, f"Aquatic {i}")
        
        for i in range(1, 3):
            cb = getattr(self.ui, f'c_eq{i}', None)
            ed = getattr(self.ui, f'e_eq{i}', None)
            if cb and ed:
                validate_row(cb, ed, f"Equine {i}")
        
        for i in range(1, 12):
            cb = getattr(self.ui, f'c_ot{i}', None)
            ed = getattr(self.ui, f'e_ot{i}', None)
            if cb and ed:
                validate_row(cb, ed, f"Others {i}")
        
        # Validate custom fields
        if self.ui.c_ot12.isChecked():
            name_text = self.ui.e_ot12_n.text().strip()
            sample_text = self.ui.e_ot11_2.text().strip()
            price_text = self.ui.e_ot12_p.text().strip()
            
            if not name_text:
                validation_errors.append("Custom Test 1: กรุณาใส่ชื่อการตรวจ")
            if not sample_text:
                validation_errors.append("Custom Test 1: กรุณาใส่จำนวน sample")
            elif not sample_text.isdigit() or int(sample_text) <= 0:
                validation_errors.append("Custom Test 1: จำนวน sample ต้องเป็นตัวเลขมากกว่า 0")
            if not price_text:
                validation_errors.append("Custom Test 1: กรุณาใส่ราคา")
            elif not price_text.isdigit() or int(price_text) <= 0:
                validation_errors.append("Custom Test 1: ราคาต้องเป็นตัวเลขมากกว่า 0")
        
        if self.ui.c_ot13.isChecked():
            name_text = self.ui.e_ot13_n.text().strip()
            sample_text = self.ui.e_ot11_3.text().strip()
            price_text = self.ui.e_ot13_p.text().strip()
            
            if not name_text:
                validation_errors.append("Custom Test 2: กรุณาใส่ชื่อการตรวจ")
            if not sample_text:
                validation_errors.append("Custom Test 2: กรุณาใส่จำนวน sample")
            elif not sample_text.isdigit() or int(sample_text) <= 0:
                validation_errors.append("Custom Test 2: จำนวน sample ต้องเป็นตัวเลขมากกว่า 0")
            if not price_text:
                validation_errors.append("Custom Test 2: กรุณาใส่ราคา")
            elif not price_text.isdigit() or int(price_text) <= 0:
                validation_errors.append("Custom Test 2: ราคาต้องเป็นตัวเลขมากกว่า 0")
        
        # Show error message if validation fails
        if validation_errors:
            error_message = "⚠️ กรุณาแก้ไขข้อมูลต่อไปนี้:\n\n" + "\n".join(f"• {err}" for err in validation_errors)
            QMessageBox.warning(self, "ข้อมูลไม่ครบถ้วน", error_message)
            for err in validation_errors:
                print(f"   - {err}")
            return None
        
        # If validation passes, proceed with calculation
        all_items = self.get_data()
        
        # Filter only selected items for summary display
        selected_items = [item for item in all_items if item['quantity'] > 0]
        
        total_count = len(selected_items)  # จำนวนรายการที่เลือก
        # Calculate total cost for DISPLAY only (unit_price * quantity)
        total_cost = sum(item['unit_price'] * item['quantity'] for item in selected_items)
        total_samples = sum(item['quantity'] for item in selected_items)  # จำนวน sample รวม
        
        # Update UI
        self.set_summary(total_count, total_cost)
        
        return {
            'items': all_items,  # Return ALL items (will save to DB)
            'total_count': total_count,
            'total_samples': total_samples,
            'total_cost': total_cost  # For display only
        }

    def _extract_price(self, text):
        try:
            if "(" in text and ")" in text:
                return int(text.split("(")[-1].replace(")", ""))
        except:
            pass
        return 0

    def set_summary(self, count, cost):
        self.ui.e_cnt.setText(str(count))
        self.ui.e_cst.setText(str(cost))

    def clear_page(self):
        """Unchecks all checkboxes and clears text inputs"""
        # Clear all checkboxes
        for widget in self.findChildren(QCheckBox):
            widget.setChecked(False)  # This will also disable and clear LineEdits via signal
        
        # Clear all line edits
        for widget in self.findChildren(QLineEdit):
            if widget.isEnabled():
                widget.clear()
        
        # Clear Laboratory Request radio buttons
        if hasattr(self.ui, 'r_c'):
            self.ui.r_c.setAutoExclusive(False)
            self.ui.r_c.setChecked(False)
            self.ui.r_c.setAutoExclusive(True)
        
        if hasattr(self.ui, 'r_q'):
            self.ui.r_q.setAutoExclusive(False)
            self.ui.r_q.setChecked(False)
            self.ui.r_q.setAutoExclusive(True)
        
        if hasattr(self.ui, 'r_e'):
            self.ui.r_e.setAutoExclusive(False)
            self.ui.r_e.setChecked(False)
            self.ui.r_e.setAutoExclusive(True)
        
        # Reset summary
        self.set_summary(0, 0)