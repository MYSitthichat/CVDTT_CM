from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem, QAbstractItemView, QHeaderView
from View.template_from_ui.lab_report import Ui_lab_report_MainWindow as Ui_LabReportPage

class LabReportPageWidget(QWidget):
    """ 
    Wrapper view for the Lab Report Page. 
    """

    def __init__(self, parent=None):
        super(LabReportPageWidget, self).__init__(parent)
        self.ui = Ui_LabReportPage()
        self.ui.setupUi(self)
        
        # Setup Layout if not already present (since it's a Form)
        if self.layout() is None:
            layout = QVBoxLayout()
            # Add widgets to layout based on your UI structure logic
            # Since your UI is flat on the widget, we might just need to set the layout on self
            # However, often Ui_Form.setupUi(self) sets up direct children. 
            # If the UI doesn't resize correctly, we usually add a main layout.
            pass

        # Cosmetic Setup
        self.decorate_table()

    def decorate_table(self):
        """ Setup table properties """
        table = self.ui.result_table
        
        # Select full rows
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setAlternatingRowColors(True)
        
        # Header stretching
        header = table.horizontalHeader()
        header.setStretchLastSection(True)

    def clear_page(self):
        """ Clear inputs and table """
        self.ui.search_input.clear()
        self.ui.result_table.setRowCount(0)

    def get_search_text(self):
        return self.ui.search_input.text().strip()