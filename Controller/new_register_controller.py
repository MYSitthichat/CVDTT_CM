from PySide6.QtCore import QObject, Qt, QTimer
from PySide6.QtWidgets import QMessageBox
from API.client_app import APIApp
from View.view_register_new_customer_frame import RegisterNewCustomerWidget

class NewRegisterController(QObject):
    def __init__(self, register_widget=None):
        super().__init__()
        if register_widget is None:
            self.main_nr = RegisterNewCustomerWidget()
        else:
            self.main_nr = register_widget
            
        self.api_app = APIApp()
        self.main_nr.ui.Add_new_costumer_save_pushButton.clicked.connect(self.save_register_clicked)
        self.main_nr.ui.Add_new_costumer_cancel_pushButton.clicked.connect(self.cancel_register_clicked)

    def save_register_clicked(self):
        selected_group_name = self.main_nr.get_radio_button_checked()
        self.title_name = self.main_nr.ui.title_name_lineEdit.text()
        self.mid_name = self.main_nr.ui.name_lineEdit.text()
        self.name = self.main_nr.ui.name_lineEdit.text()
        self.surname = self.main_nr.ui.sure_name_lineEdit.text()
        self.tax_id = self.main_nr.ui.tax_id_lineEdit.text()
        self.email = self.main_nr.ui.email_lineEdit.text()
        self.line_ID = self.main_nr.ui.line_id_lineEdit.text()
        self.phone = self.main_nr.ui.phone_lineEdit.text()
        self.address = self.main_nr.ui.address_contact_textEdit.toPlainText()
        self.bill_address = self.main_nr.ui.address_billing_textEdit.toPlainText()
        api_response = self.api_app.get_customer_group_id()
        all_groups_list = []
        if isinstance(api_response, dict) and 'customer_groups' in api_response:
            all_groups_list = api_response['customer_groups']
        elif isinstance(api_response, list):
            all_groups_list = api_response
        group_name_to_id_map = {}
        for item in all_groups_list:
            name = item.get('group_name')
            g_id = item.get('id')
            if name and g_id:
                group_name_to_id_map[name] = g_id
        selected_group_name = self.main_nr.get_radio_button_checked()
        final_group_id = group_name_to_id_map.get(selected_group_name)
        if final_group_id is None:
            pass
        customer_data = {
            "group_id": str(final_group_id),
            "title_name": self.title_name,
            "name": self.name,
            "mid_name": self.mid_name,       
            "surname": self.surname,
            "tax_id": self.tax_id,
            "phone": self.phone,
            "email": self.email,
            "line_ID": self.line_ID,         
            "address": self.address,
            "bill_address": self.bill_address
        }
        result = self.api_app.add_new_customer(customer_data)
        if result:
            QMessageBox.information(
            self.main_nr, 
            "Success", 
            "Customer added successfully!"
            )
            self.main_nr.clear_all_fields()
        else:
            QMessageBox.warning(
            self.main_nr, 
            "Error", 
            "Failed to add customer."
            )

    def cancel_register_clicked(self):
        self.main_nr.clear_all_fields()