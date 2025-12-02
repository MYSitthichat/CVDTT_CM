from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QCheckBox, QLineEdit
# Ensure this import matches where you save the generated file 'molecular.py'
from View.template_from_ui.molecular_biology import Ui_molecular_biology_MainWindow as Ui_MolecularBiologyPage

class MolecularBiologyPageWidget(QWidget):
    """ 
    Wrapper view for the Molecular Biology Page. 
    """

    def __init__(self, parent=None):
        super(MolecularBiologyPageWidget, self).__init__(parent)
        self.ui = Ui_MolecularBiologyPage()
        
        # Create a dummy window because the generated UI file expects a QMainWindow
        dummy_main_window = QMainWindow()
        self.ui.setupUi(dummy_main_window)
        
        # Extract central widget and place it in this QWidget's layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.centralwidget)
        self.setLayout(layout)

    def get_data(self):
        """
        Retrieves data from the UI.
        Returns a list of dictionaries for selected items:
        [{'name': 'Test Name', 'sample_id': '123', 'price': 0}, ...]
        """
        selected_items = []
        
        # Helper function to check a row
        def check_row(checkbox, entry_sample, price=0):
            if checkbox.isChecked():
                return {
                    'name': checkbox.text(),
                    'sample_id': entry_sample.text(),
                    # Attempt to extract price from text if not provided, e.g. "Test (700)"
                    'price': price if price > 0 else self._extract_price(checkbox.text())
                }
            return None

        # --- Avian (1-12) ---
        for i in range(1, 13):
            cb = getattr(self.ui, f'c_av{i}')
            ed = getattr(self.ui, f'e_av{i}')
            if res := check_row(cb, ed): selected_items.append(res)

        # --- Blood Parasite 1 (1-8) ---
        for i in range(1, 9):
            cb = getattr(self.ui, f'c_bp1_{i}')
            ed = getattr(self.ui, f'e_bp1_{i}')
            if res := check_row(cb, ed): selected_items.append(res)

        # --- Blood Parasite 2 (1-8) ---
        for i in range(1, 9):
            cb = getattr(self.ui, f'c_bp2_{i}')
            ed = getattr(self.ui, f'e_bp2_{i}')
            if res := check_row(cb, ed): selected_items.append(res)

        # --- Feline (1-4) ---
        for i in range(1, 5):
            cb = getattr(self.ui, f'c_fe{i}')
            ed = getattr(self.ui, f'e_fe{i}')
            if res := check_row(cb, ed): selected_items.append(res)

        # --- Bovine (1-4) ---
        for i in range(1, 5):
            cb = getattr(self.ui, f'c_bv{i}')
            ed = getattr(self.ui, f'e_bv{i}')
            if res := check_row(cb, ed): selected_items.append(res)

        # --- Canine (1-2) ---
        for i in range(1, 3):
            cb = getattr(self.ui, f'c_cn{i}')
            ed = getattr(self.ui, f'e_cn{i}')
            if res := check_row(cb, ed): selected_items.append(res)

        # --- Elephant (1-5) ---
        for i in range(1, 6):
            cb = getattr(self.ui, f'c_el{i}')
            ed = getattr(self.ui, f'e_el{i}')
            if res := check_row(cb, ed): selected_items.append(res)

        # --- Aquatic (1-3) ---
        for i in range(1, 4):
            cb = getattr(self.ui, f'c_aq{i}')
            ed = getattr(self.ui, f'e_aq{i}')
            if res := check_row(cb, ed): selected_items.append(res)

        # --- Equine (1-2) ---
        for i in range(1, 3):
            cb = getattr(self.ui, f'c_eq{i}')
            ed = getattr(self.ui, f'e_eq{i}')
            if res := check_row(cb, ed): selected_items.append(res)

        # --- Others (1-11) ---
        for i in range(1, 12):
            cb = getattr(self.ui, f'c_ot{i}')
            ed = getattr(self.ui, f'e_ot{i}')
            if res := check_row(cb, ed): selected_items.append(res)

        # --- Custom Others 1 (c_ot12) ---
        if self.ui.c_ot12.isChecked():
            price_text = self.ui.e_ot12_p.text()
            price = int(price_text) if price_text.isdigit() else 0
            selected_items.append({
                'name': self.ui.e_ot12_n.text(),
                'sample_id': self.ui.e_ot11_2.text(), # Variable name from your file
                'price': price
            })

        # --- Custom Others 2 (c_ot13) ---
        if self.ui.c_ot13.isChecked():
            price_text = self.ui.e_ot13_p.text()
            price = int(price_text) if price_text.isdigit() else 0
            selected_items.append({
                'name': self.ui.e_ot13_n.text(),
                'sample_id': self.ui.e_ot11_3.text(), # Variable name from your file
                'price': price
            })

        return selected_items

    def _extract_price(self, text):
        """ Extracts price from string like 'Test Name (500)' """
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
        # """ Unchecks all checkboxes and clears text inputs """
        # for widget in self.findChildren(QCheckBox):
        #     widget.setChecked(False)
        # for widget in self.findChildren(QLineEdit):
        #     widget.clear()
        pass