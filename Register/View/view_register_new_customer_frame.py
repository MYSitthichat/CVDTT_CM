from PySide6.QtWidgets import QWidget
from View.template_from_ui.register_new_customer_frame import Ui_register_new_customer_MainWindow


class RegisterNewCustomerWidget(QWidget):
    
    def __init__(self, parent=None):
        super(RegisterNewCustomerWidget, self).__init__(parent)
        self.ui = Ui_register_new_customer_MainWindow()
        from PySide6.QtWidgets import QMainWindow
        dummy_main_window = QMainWindow()
        self.ui.setupUi(dummy_main_window)
        
        from PySide6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.centralwidget)
        self.setLayout(layout)
        self.ui.Add_new_costumer_private_radioButton.setChecked(True)
        # self.ui.mid_name_checkBox.toggled.connect(self.toggle_middle_name)

    def get_radio_button_checked(self):
        if self.ui.Add_new_costumer_private_radioButton.isChecked():
            return "บุคคลธรรมดา"
        elif self.ui.Add_new_costumer_public_radioButton.isChecked():
            return "นิติบุคคล"
        elif self.ui.Add_new_costumer_internal_radioButton.isChecked():
            return "หน่วยงานภายใน"
        elif self.ui.Add_new_costumer_professor_radioButton.isChecked():
            return "อาจารย์ในคณะ"
        elif self.ui.Add_new_costumer_student_radioButton.isChecked():
            return "นักศึกษา"
        else:
            return "ไม่ได้เลือกประเภท"

    # def set_middle_name_status(self, enabled: bool):
        # self.ui.middle_lineEdit.setEnabled(enabled)
    
    # def toggle_middle_name(self, checked):
    #     if checked:
    #         self.set_middle_name_status(True)
    #     else:
    #         self.set_middle_name_status(False)
    #         self.ui.middle_lineEdit.clear()
    
    def clear_all_fields(self):
        self.ui.title_name_lineEdit.clear()
        self.ui.name_lineEdit.clear()
        # self.ui.middle_lineEdit.clear()
        self.ui.sure_name_lineEdit.clear()
        self.ui.tax_id_lineEdit.clear()
        self.ui.email_lineEdit.clear()
        self.ui.line_id_lineEdit.clear()
        self.ui.phone_lineEdit.clear()
        self.ui.address_contact_textEdit.clear()
        self.ui.address_billing_textEdit.clear()
        self.ui.Add_new_costumer_private_radioButton.setChecked(True)
        # self.ui.mid_name_checkBox.setChecked(False)
        # self.set_middle_name_status(False)