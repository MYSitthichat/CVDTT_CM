from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QAbstractItemView, QHeaderView
from View.template_from_ui.barcode_page import Ui_barcode_page_MainWindow 

class BarcodePageWidget(QWidget):
    """ 
    Wrapper view for the Barcode Page. 
    Inherits from QWidget so it can be embedded into the main window's stack.
    """

    def __init__(self, parent=None):
        super(BarcodePageWidget, self).__init__(parent)
        self.ui = Ui_barcode_page_MainWindow()
        
        # 1. Create a dummy window because the generated UI file expects a QMainWindow
        dummy_main_window = QMainWindow()
        self.ui.setupUi(dummy_main_window)
        
        # 2. Extract central widget and place it in this QWidget's layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.centralwidget)
        self.setLayout(layout)

        # 3. Apply decorations (Cosmetic setups)
        self.decorate_view()

    def decorate_view(self):
        """ Setup cosmetic properties for the table widget """
        table = self.ui.tableWidget
        
        # Select full rows when clicking
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # Only allow selecting one row at a time
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # Prevent user from editing cells directly
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Make the last column stretch to fill empty space
        if table.columnCount() > 0:
            header = table.horizontalHeader()
            header.setStretchLastSection(True)
        
        # Add alternating colors for better readability
        table.setAlternatingRowColors(True)

    def clear_inputs(self):
        """ Helper to clear text inputs """
        self.ui.lineEdit_firstname.clear()
        self.ui.lineEdit_lastname.clear()
        self.ui.lineEdit_taxid.clear()
        self.ui.lineEdit_sender.clear()