from PySide6.QtWidgets import QWidget, QHeaderView
from View.template_from_ui.new_work_frame import Ui_add_new_work_MainWindow
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QMainWindow

class AddNewWorkWidget(QWidget):

    def __init__(self, parent=None):
        super(AddNewWorkWidget, self).__init__(parent)
        self.ui = Ui_add_new_work_MainWindow()
        dummy_main_window = QMainWindow()
        self.ui.setupUi(dummy_main_window)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.centralwidget)
        self.setLayout(layout)
        self.setup_table_columns()
        self.ui.nw_owner_same_sender_checkBox.stateChanged.connect(self.same_as_sender_checked)

    def setup_table_columns(self):
        if hasattr(self.ui, 'nw_work_register_treeWidget'):
            table = self.ui.nw_work_register_treeWidget
            table.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def set_dettail_to_sender(self, detail):
        name = detail[0]
        surname = detail[1]
        tax_id = detail[2]
        self.ui.nw_name_sender_lineEdit.setText(name)
        self.ui.nw_sure_name_sender_lineEdit.setText(surname)
        self.ui.nw_tex_id_sender_lineEdit.setText(tax_id)
    
    def set_dettail_to_owner(self, detail):
        name = detail[0]
        surname = detail[1]
        tax_id = detail[2]
        self.ui.nw_name_owner_lineEdit.setText(name)
        self.ui.nw_sure_name_owner_lineEdit.setText(surname)
        self.ui.nw_tex_id_owner_lineEdit.setText(tax_id)

    def same_as_sender_checked(self, checked):
        if checked:
            self.ui.nw_name_owner_lineEdit.setText(self.ui.nw_name_sender_lineEdit.text())
            self.ui.nw_sure_name_owner_lineEdit.setText(self.ui.nw_sure_name_sender_lineEdit.text())
            self.ui.nw_tex_id_owner_lineEdit.setText(self.ui.nw_tex_id_sender_lineEdit.text())
        else:
            self.ui.nw_name_owner_lineEdit.clear()
            self.ui.nw_sure_name_owner_lineEdit.clear()
            self.ui.nw_tex_id_owner_lineEdit.clear()
            
    def check_data_input(self):
        # Implement data validation logic here
        if not self.ui.nw_name_sender_lineEdit.text():
            return False
        if not self.ui.nw_sure_name_sender_lineEdit.text():
            return False
        if not self.ui.nw_tex_id_sender_lineEdit.text():
            return False
        if not self.ui.nw_name_owner_lineEdit.text():
            return False
        if not self.ui.nw_sure_name_owner_lineEdit.text():
            return False
        if not self.ui.nw_tex_id_owner_lineEdit.text():
            return False
        return True

    def check_project_name_input(self):
        if not self.ui.nw_project_name_lineEdit.text():
            return False
        return True
    
    def lock_all_input(self):
        self.ui.nw_name_sender_lineEdit.setDisabled(True)
        self.ui.nw_sure_name_sender_lineEdit.setDisabled(True)
        self.ui.nw_tex_id_sender_lineEdit.setDisabled(True)
        self.ui.nw_name_owner_lineEdit.setDisabled(True)
        self.ui.nw_sure_name_owner_lineEdit.setDisabled(True)
        self.ui.nw_tex_id_owner_lineEdit.setDisabled(True)
        self.ui.nw_project_name_lineEdit.setDisabled(True)
        self.ui.nw_save_pushButton.setDisabled(True)
        self.ui.nw_id_lineEdit.setDisabled(True)
        self.ui.nw_owner_same_sender_checkBox.setDisabled(True)
        self.ui.nw_cancel_pushButton.setDisabled(False)
        self.ui.nw_add_result_pushButton.setDisabled(False)
        self.ui.new_delete_result_pushButton.setDisabled(False)
        self.ui.nw_print_bracode_pushButton.setDisabled(False)
        self.ui.nw_print_sned_lab_pushButton.setDisabled(False)
        self.ui.nw_work_register_treeWidget.setDisabled(False)
    
    def unlock_all_input(self):
        self.ui.nw_name_sender_lineEdit.setDisabled(False)
        self.ui.nw_sure_name_sender_lineEdit.setDisabled(False)
        self.ui.nw_tex_id_sender_lineEdit.setDisabled(False)
        self.ui.nw_name_owner_lineEdit.setDisabled(False)
        self.ui.nw_sure_name_owner_lineEdit.setDisabled(False)
        self.ui.nw_tex_id_owner_lineEdit.setDisabled(False)
        self.ui.nw_project_name_lineEdit.setDisabled(False)
        self.ui.nw_save_pushButton.setDisabled(False)
        self.ui.nw_id_lineEdit.setDisabled(False)
        self.ui.nw_owner_same_sender_checkBox.setDisabled(False)
        self.ui.nw_cancel_pushButton.setDisabled(True)
        self.ui.nw_add_result_pushButton.setDisabled(True)
        self.ui.new_delete_result_pushButton.setDisabled(True)
        self.ui.nw_print_bracode_pushButton.setDisabled(True)
        self.ui.nw_print_sned_lab_pushButton.setDisabled(True)
        self.ui.nw_work_register_treeWidget.setDisabled(True)