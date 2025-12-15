from PySide6.QtWidgets import QWidget
from View.template_from_ui.receive_lab_frame import Ui_receive_lab_Form

class ReceiveLabFormView(QWidget):
    def __init__(self, parent=None):
        super(ReceiveLabFormView, self).__init__(parent)
        self.ui = Ui_receive_lab_Form()
        self.ui.setupUi(self)
        # Signal connection moved to controller
        self.ui.bacteria_radioButton.setChecked(True)
        self.hide_radio_buttons()
    
    def get_type_search(self) -> str:
        if self.ui.bacteria_radioButton.isChecked():
            type_select = 2
        elif self.ui.molecular_radioButton.isChecked():
            type_select = 8
        elif self.ui.parasite_radioButton.isChecked():
            type_select = 5
        elif self.ui.after_radioButton.isChecked():
            type_select = 13

        return type_select
    
    def hide_radio_buttons(self):
        self.ui.bacteria_radioButton.hide()
        self.ui.molecular_radioButton.hide()
        self.ui.parasite_radioButton.hide()
        self.ui.after_radioButton.hide()
    
    def show_radio_buttons(self):
        self.ui.bacteria_radioButton.show()
        self.ui.molecular_radioButton.show()
        self.ui.parasite_radioButton.show()
        self.ui.after_radioButton.show()
    
    def clear_radio_buttons(self):
        self.ui.bacteria_radioButton.setAutoExclusive(False)
        self.ui.molecular_radioButton.setAutoExclusive(False)
        self.ui.parasite_radioButton.setAutoExclusive(False)
        self.ui.after_radioButton.setAutoExclusive(False)

        self.ui.bacteria_radioButton.setChecked(False)
        self.ui.molecular_radioButton.setChecked(False)
        self.ui.parasite_radioButton.setChecked(False)
        self.ui.after_radioButton.setChecked(False)

        self.ui.bacteria_radioButton.setAutoExclusive(True)
        self.ui.molecular_radioButton.setAutoExclusive(True)
        self.ui.parasite_radioButton.setAutoExclusive(True)
        self.ui.after_radioButton.setAutoExclusive(True)

    def clear_all_table(self):
        if self.ui.tableView.model():
            self.ui.tableView.model().removeRows(0, self.ui.tableView.model().rowCount())
        self.ui.tableView.scrollToTop()
        self.ui.barcode_lineEdit.clear()