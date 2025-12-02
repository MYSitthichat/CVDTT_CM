from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QAbstractItemView
from View.template_from_ui.lab_received_sample import Ui_lab_received_MainWindow

class LabReceivedSampleWidget(QWidget):
    """ 
    Wrapper view for the Lab Received Sample Page. 
    """

    def __init__(self, parent=None):
        super(LabReceivedSampleWidget, self).__init__(parent)
        self.ui = Ui_lab_received_MainWindow()
        
        dummy_main_window = QMainWindow()
        self.ui.setupUi(dummy_main_window)
        
        self.ui.setupUi(self) 

        self.decorate_view()

    def decorate_view(self):
        """ Setup cosmetic properties for the table widget """
        table = self.ui.table_staff
        
        # Select full rows when clicking
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # Only allow selecting one row at a time
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # Prevent user from editing cells directly
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Add alternating colors for better readability
        table.setAlternatingRowColors(True)

    def clear_inputs(self):
        """ Helper to clear input fields """
        self.ui.le_search.clear()
        self.ui.table_staff.setRowCount(0)
        self.ui.le_barcode.clear()
        self.ui.le_receiver.clear()
        self.ui.le_receiver_id.clear()
        
        from PySide6.QtCore import QDateTime
        self.ui.dt_received.setDateTime(QDateTime.currentDateTime())