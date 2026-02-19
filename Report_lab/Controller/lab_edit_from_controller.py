import os
import sys
import shutil
from PySide6.QtWidgets import QMessageBox, QTreeWidgetItem, QFileDialog
from PySide6.QtCore import QObject
from View.view_lab_edite_form_frame import LabEditFormView
from SERVICES_REPORT_LAB.report_information_service import ReportInformationService

class LabEditFormController(QObject):
    """ Controller for the Lab Edit Form Page """

    def __init__(self, view: LabEditFormView, main_controller=None):
        super().__init__()
        self.view: LabEditFormView = view
        self.main_controller = main_controller
        self.report_info_service = ReportInformationService()
        self.user_room_id = None
        self.user_group_id = None
        self.room_name_map = {}
        
        # State variables
        self.pending_file_path = None
        self.editing_report_id = None
        self.current_report_path = None
        self.current_room_id_of_item = None 
        
        self._setup_connections()
        self.setup_table_widget()
        self.set_initial_ui_state()

    def set_initial_ui_state(self):
        """กำหนดสถานะเริ่มต้น"""
        self.view.ui.Download_form_pushButton.setEnabled(False)
        self.view.ui.lab_name_comboBox.setEnabled(False)
        self.view.ui.form_name_lineEdit.setEnabled(False)
        self.view.ui.detail_from_textEdit.setEnabled(False)
        self.view.ui.save_form_pushButton.setEnabled(False)
        
        self.view.ui.new_lab_name_lineEdit.setEnabled(False)
        self.view.ui.new_lab_detail_textEdit.setEnabled(False)
        self.view.ui.save_new_lab_pushButton.setEnabled(False)
        
        self.view.ui.form_name_lineEdit.clear()
        self.view.ui.detail_from_textEdit.clear()
        
        self.editing_report_id = None
        self.pending_file_path = None

    def _setup_connections(self):
        self.view.ui.list_detail_treeWidget.itemSelectionChanged.connect(self.on_item_selection_changed)
        self.view.ui.Edte_form_pushButton.clicked.connect(self.edit_form_pushButton_clicked)
        self.view.ui.Download_form_pushButton.clicked.connect(self.download_pushButton_clicked)
        self.view.ui.Delete_form_pushButton.clicked.connect(self.delete_pushButton_clicked)
        self.view.ui.save_form_pushButton.clicked.connect(self.save_form_pushButton_clicked)
        self.view.ui.save_new_lab_pushButton.clicked.connect(self.save_new_lab_pushButton_clicked)

    def setup_table_widget(self):
        tree = self.view.ui.list_detail_treeWidget
        tree.setColumnWidth(0, 400)
        tree.setColumnWidth(1, 100)
        tree.setColumnWidth(2, 550)
        tree.header().setStretchLastSection(True)
        tree.setSelectionMode(tree.SelectionMode.SingleSelection)
        tree.setSelectionBehavior(tree.SelectionBehavior.SelectRows)
        tree.setEditTriggers(tree.EditTrigger.NoEditTriggers)
        tree.setAlternatingRowColors(True)

    def get_app_root_path(self):
        """ดึง Path ที่ตั้งของโปรแกรม เพื่อทำ Relative Path"""
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            application_path = os.path.dirname(current_dir) # ถอย 2 step จาก controller -> root
            # เช็คว่าถอยถูกไหม (ควรจะเจอ folder BACKEND หรือ Report_lab)
            if not os.path.exists(os.path.join(application_path, 'Saved_Forms')):
                 # fallback: ลองถอยอีกชั้นถ้า structure ลึกกว่าปกติ
                 pass
        return application_path

    def on_item_selection_changed(self):
        selected_items = self.view.ui.list_detail_treeWidget.selectedItems()
        if not selected_items:
            self.set_initial_ui_state()
            return

        item = selected_items[0]
        report_id = item.data(0, 1000)
        
        if not report_id: # Group Header
            self.set_initial_ui_state()
            return

        # --- EDIT MODE SETUP ---
        self.editing_report_id = report_id
        
        # Path นี้ถูกแปลงเป็น Absolute แล้วใน populate_tree_widget
        self.current_report_path = item.data(0, 1001) 
        self.current_room_id_of_item = item.data(0, 1002) 
        self.pending_file_path = None

        report_name = item.text(0)
        detail = item.text(2)

        self.view.ui.form_name_lineEdit.setText(report_name)
        self.view.ui.detail_from_textEdit.setText(detail)

        parent_item = item.parent()
        if parent_item:
            self.view.ui.lab_name_comboBox.setCurrentText(parent_item.text(0))

        self.view.ui.lab_name_comboBox.setEnabled(True)
        self.view.ui.form_name_lineEdit.setEnabled(True)
        self.view.ui.detail_from_textEdit.setEnabled(True)
        self.view.ui.save_form_pushButton.setEnabled(True)
        self.view.ui.Download_form_pushButton.setEnabled(True)

    def edit_form_pushButton_clicked(self):
        file_dialog = QFileDialog(self.view)
        file_dialog.setNameFilter("Word Documents (*.docx *.doc)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.pending_file_path = selected_files[0]
                file_name = os.path.basename(self.pending_file_path)

                if self.editing_report_id:
                    QMessageBox.information(self.view, "Info", f"เปลี่ยนไฟล์เป็น: {file_name}\nกด 'บันทึก' เพื่อยืนยัน")
                else:
                    name_only = os.path.splitext(file_name)[0]
                    self.view.ui.form_name_lineEdit.setText(name_only)
                    self.view.ui.lab_name_comboBox.setEnabled(True)
                    self.view.ui.form_name_lineEdit.setEnabled(True)
                    self.view.ui.detail_from_textEdit.setEnabled(True)
                    self.view.ui.save_form_pushButton.setEnabled(True)
                    QMessageBox.information(self.view, "Info", f"เตรียมเพิ่มไฟล์: {file_name}")

    def save_form_pushButton_clicked(self):
        try:
            new_report_name = self.view.ui.form_name_lineEdit.text().strip()
            detail_text = self.view.ui.detail_from_textEdit.toPlainText()
            
            if not new_report_name:
                QMessageBox.warning(self.view, "Warning", "กรุณากรอกชื่อแบบฟอร์ม")
                return

            root_path = self.get_app_root_path()
            user_id = 1
            if self.main_controller:
                user_id = self.main_controller.get_logged_in_user_id() or 1

            allow_all = self.user_group_id in [1, 2, 3, 18, 19, 20]
            room_id_to_save = None

            if self.editing_report_id:
                room_id_to_save = self.current_room_id_of_item
            else:
                if allow_all:
                    selected_room_name = self.view.ui.lab_name_comboBox.currentText()
                    room_id_to_save = self.room_name_map.get(selected_room_name)
                    
                    if not room_id_to_save:
                        QMessageBox.warning(self.view, "Error", "ไม่สามารถระบุ ID ของห้องที่เลือกได้")
                        return
                else:
                    room_id_to_save = self.user_room_id

            if not room_id_to_save:
                room_id_to_save = 999 
            
            # --- PATH LOGIC (เหมือนเดิม) ---
            backend_root = os.path.join(root_path, "..", "BACKEND")
            backend_root = os.path.abspath(backend_root)
            rel_folder = os.path.join("report_template", "word", f"Room_{room_id_to_save}")
            abs_folder = os.path.join(backend_root, rel_folder)

            if not os.path.exists(abs_folder):
                os.makedirs(abs_folder)

            db_path_to_save = None

            # --- 2. Process (Edit vs New) ---
            if self.editing_report_id:
                # === EDIT ===
                if self.pending_file_path:
                    # มีการเปลี่ยนไฟล์ -> Copy ใหม่
                    file_name = os.path.basename(self.pending_file_path)
                    shutil.copy2(self.pending_file_path, os.path.join(abs_folder, file_name))
                    db_path_to_save = os.path.join("report_template", "word", f"Room_{room_id_to_save}", file_name) # Save Relative (ไม่รวม BACKEND)
                else:
                    # ไม่เปลี่ยนไฟล์ -> ใช้ Path เดิม (ต้องแปลงกลับเป็น Relative ถ้าทำได้)
                    current_abs = self.current_report_path
                    if current_abs and current_abs.startswith(root_path):
                        db_path_to_save = os.path.relpath(current_abs, root_path)
                    else:
                        db_path_to_save = current_abs # กรณีเป็น Path ภายนอกเก่าๆ

                success, message = self.report_info_service.save_new_report_version(
                    old_report_id=self.editing_report_id,
                    new_name=new_report_name,
                    new_path=db_path_to_save,
                    room_id=room_id_to_save,
                    updater_id=user_id,
                    detail=detail_text
                )
            else:
                # === NEW ===
                if not self.pending_file_path:
                     QMessageBox.warning(self.view, "Warning", "กรุณาเลือกไฟล์ก่อน")
                     return
                
                file_name = os.path.basename(self.pending_file_path)
                shutil.copy2(self.pending_file_path, os.path.join(abs_folder, file_name))
                db_path_to_save = os.path.join("report_template", "word", f"Room_{room_id_to_save}", file_name) # Save Relative (ไม่รวม BACKEND)
                
                success, message = self.report_info_service.add_report(
                    report_name=new_report_name,
                    room_id=room_id_to_save,
                    report_path=db_path_to_save,
                    updater_id=user_id,
                    detail=detail_text
                )

            # --- 3. Result ---
            if success:
                QMessageBox.information(self.view, "Success", "บันทึกข้อมูลเรียบร้อยแล้ว")
                self.set_initial_ui_state()
                self.reload_data()
            else:
                QMessageBox.critical(self.view, "Error", f"บันทึกข้อมูลล้มเหลว: {message}")

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            QMessageBox.critical(self.view, "Error", f"System Error: {str(e)}")

    def delete_pushButton_clicked(self):
        selected_items = self.view.ui.list_detail_treeWidget.selectedItems()
        if not selected_items: return
            
        item = selected_items[0]
        report_id = item.data(0, 1000)
        
        if not report_id: return

        confirm = QMessageBox.question(self.view, "Confirm", f"ลบรายงาน '{item.text(0)}' ?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            user_id = self.main_controller.get_logged_in_user_id() or 1 if self.main_controller else 1
            success, message = self.report_info_service.delete_report(report_id, user_id)
            if success:
                self.reload_data()
            else:
                QMessageBox.critical(self.view, "Error", message)

    def save_new_lab_pushButton_clicked(self):
        QMessageBox.information(self.view, "Information", "Feature Disabled")

    def download_pushButton_clicked(self):
        selected_items = self.view.ui.list_detail_treeWidget.selectedItems()
        if not selected_items: return
            
        item = selected_items[0]
        src_path = item.data(0, 1001) # อันนี้เป็น Absolute Path แล้ว
        
        if not src_path or not os.path.exists(src_path):
            QMessageBox.critical(self.view, "Error", f"ไม่พบไฟล์ต้นฉบับ:\n{src_path}")
            return

        _, ext = os.path.splitext(src_path)
        save_path, _ = QFileDialog.getSaveFileName(self.view, "Save File", f"{item.text(0)}{ext}", f"*{ext}")

        if save_path:
            try:
                shutil.copy2(src_path, save_path)
                QMessageBox.information(self.view, "Success", "ดาวน์โหลดเสร็จสิ้น")
            except Exception as e:
                QMessageBox.critical(self.view, "Error", str(e))

    def set_user_group_id(self, group_id):
        self.user_group_id = group_id

    def reload_data(self):
        self.load_report_data()
    
    def set_room_id(self, room_id: int):
        self.user_room_id = room_id
    
    def load_report_data(self):
        # เงื่อนไขพิเศษ ให้โหลดทั้งหมด
        allow_all = self.user_group_id in [1, 2, 3, 18, 19, 20]

        if allow_all:
            result = self.report_info_service.get_all_reports_with_status(1)
        else:
            # User ทั่วไป โหลดตามห้องตัวเอง
            if self.user_room_id is None: return
            result = self.report_info_service.get_reports_by_room_and_status(self.user_room_id, 1)
            
        reports = result if isinstance(result, list) else []
        self.populate_tree_widget(reports)
    
    def populate_tree_widget(self, reports):
        tree = self.view.ui.list_detail_treeWidget
        combo = self.view.ui.lab_name_comboBox
        if not tree: return
        
        tree.clear()
        combo.clear()
        self.room_name_map.clear() 
        
        # เช็คสิทธิ์
        allow_all = self.user_group_id in [1, 2, 3, 18, 19, 20]

        if allow_all:
            # ถ้าเป็น Admin ให้ดึงรายชื่อห้องทั้งหมดจาก DB มาใส่
            all_rooms = self.report_info_service.get_all_rooms_list()
            
            for room in all_rooms:
                r_name = room.get('name')
                r_id = room.get('id')
                if r_name and r_id:
                    self.room_name_map[r_name] = r_id
                    combo.addItem(r_name)
        else:
            # ถ้าเป็น User ธรรมดา ให้ใส่เฉพาะห้องที่มีใน report หรือห้องตัวเอง
            if reports:
                for r in reports:
                    name = r.get('room_name', f"Room {r.get('room_id')}")
                    rid = r.get('room_id')
                    if name not in self.room_name_map:
                        self.room_name_map[name] = rid
                        combo.addItem(name)
            else:
                pass

        root_path = self.get_app_root_path()
        backend_root = os.path.abspath(os.path.join(root_path, "..", "BACKEND"))
        
        grouped_reports = {}
        if reports:
            for r in reports:
                key = r.get('room_name')
                if not key:
                     key = f"Room {r.get('room_id', '?')}"
                
                grouped_reports.setdefault(key, []).append(r)

        for g_name, g_reports in grouped_reports.items():
            parent = QTreeWidgetItem(tree)
            parent.setText(0, g_name)
            parent.setText(1, str(len(g_reports)))
            
            for r in g_reports:
                child = QTreeWidgetItem(parent)
                child.setText(0, r.get('report_name', 'No Name'))
                child.setText(1, "1")
                
                detail_db = r.get('detial') or r.get('detail') or "" 
                child.setText(2, str(detail_db))
                
                child.setData(0, 1000, r.get('id'))
                child.setData(0, 1002, r.get('room_id'))
                
                db_path = r.get('report_path', '')
                full_path = db_path
                if db_path and not os.path.isabs(db_path):
                    full_path = os.path.join(backend_root, db_path)
                
                child.setData(0, 1001, full_path)
                
        tree.collapseAll()