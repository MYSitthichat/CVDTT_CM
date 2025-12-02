from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QAbstractItemView, QHeaderView
from View.template_from_ui.check_job_progress import Ui_Check_job_MainWindow 

class CheckJobProgressWidget(QWidget):
    """ 
    Wrapper view for the Check Job Progress Page. 
    Inherits from QWidget so it can be embedded into the main window's stack.
    """

    def __init__(self, parent=None):
        super(CheckJobProgressWidget, self).__init__(parent)
        # UPDATED: Using the new class name
        self.ui = Ui_Check_job_MainWindow()
        
        # 1. Create a dummy window because the generated UI file expects a QMainWindow
        dummy_main_window = QMainWindow()
        self.ui.setupUi(dummy_main_window)
        
        # 2. Extract central widget and place it in this QWidget's layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.centralwidget)
        self.setLayout(layout)

        # 3. Apply decorations (Cosmetic setups for tables)
        self.decorate_view()

    def decorate_view(self):
        """ Setup cosmetic properties for the table widgets """
        
        # Setup Top Table (Jobs List)
        table_top = self.ui.tableTop
        table_top.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_top.setSelectionMode(QAbstractItemView.SingleSelection)
        table_top.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Add alternating colors
        table_top.setAlternatingRowColors(True)
        
        # Setup Bottom Table (Job Details)
        table_bottom = self.ui.tableBottom
        table_bottom.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_bottom.setSelectionMode(QAbstractItemView.SingleSelection)
        table_bottom.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table_bottom.setAlternatingRowColors(True)

    def clear_tables(self):
        """ Helper to clear both tables """
        self.ui.tableTop.setRowCount(0)
        self.ui.tableBottom.setRowCount(0)