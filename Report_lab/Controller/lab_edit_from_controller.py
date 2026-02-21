import os
import sys
import shutil
import subprocess
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
        
        # State variables
        self.pending_file_path = None
        self.editing_report_id = None
        self.current_report_path = None
        self.current_lab_name_of_item = None 
        
        self._setup_connections()
        self.setup_table_widget()
        self.set_initial_ui_state()

    def set_initial_ui_state(self):
        """กำหนดสถานะเริ่มต้น"""
        self.view.ui.Download_form_pushButton.setEnabled(False)
        self.view.ui.lab_name_comboBox.setEnabled(True)   # user เลือก lab ได้ตลอด
        self.view.ui.form_name_lineEdit.setEnabled(False)
        self.view.ui.detail_from_textEdit.setEnabled(False)
        self.view.ui.save_form_pushButton.setEnabled(False)
        
        # ส่วน New Lab — ขึ้นอยู่กับ group_id
        self._apply_group_permissions()
        
        # เคลียร์ข้อมูล
        self.view.ui.form_name_lineEdit.clear()
        self.view.ui.detail_from_textEdit.clear()
        
        self.editing_report_id = None
        self.pending_file_path = None

    def _setup_connections(self):
        self.view.ui.list_detail_treeWidget.itemSelectionChanged.connect(self.on_item_selection_changed)
        self.view.ui.lab_name_comboBox.currentIndexChanged.connect(self.on_lab_name_comboBox_changed)
        self.view.ui.Edte_form_pushButton.clicked.connect(self.edit_form_pushButton_clicked)
        self.view.ui.Download_form_pushButton.clicked.connect(self.download_pushButton_clicked)
        self.view.ui.Delete_form_pushButton.clicked.connect(self.delete_pushButton_clicked)
        self.view.ui.save_form_pushButton.clicked.connect(self.save_form_pushButton_clicked)
        self.view.ui.save_new_lab_pushButton.clicked.connect(self.save_new_lab_pushButton_clicked)

    def setup_table_widget(self):
        tree = self.view.ui.list_detail_treeWidget
        tree.setColumnWidth(0, 600)
        tree.setColumnWidth(1, 150)
        tree.setColumnWidth(2, 300)
        tree.header().setStretchLastSection(True)
        tree.setSelectionMode(tree.SelectionMode.SingleSelection)
        tree.setSelectionBehavior(tree.SelectionBehavior.SelectRows)
        tree.setEditTriggers(tree.EditTrigger.NoEditTriggers)
        tree.setAlternatingRowColors(True)

    def on_lab_name_comboBox_changed(self, index: int):
        """เมื่อ user เลือก lab จาก comboBox โดยตรง (ไม่ผ่าน TreeWidget)
        ถ้าไม่ได้อยู่ใน Edit Mode ให้เปิดฟิลด์เพื่อกรอกข้อมูล New Form"""
        if self.editing_report_id:
            # อยู่ใน Edit Mode อยู่แล้ว — ไม่ต้องทำอะไรพิเศษ
            return
        if index >= 0:
            # มีการเลือก lab → เปิดฟิลด์สำหรับเพิ่มฟอร์มใหม่
            # ยกเลิก tree selection เฉพาะเมื่อไม่ได้อยู่ใน Edit Mode
            tree = self.view.ui.list_detail_treeWidget
            tree.blockSignals(True)
            tree.clearSelection()
            tree.blockSignals(False)
            self.editing_report_id = None
            self.pending_file_path = None
            self.view.ui.form_name_lineEdit.clear()
            self.view.ui.form_name_lineEdit.setEnabled(True)
            self.view.ui.detail_from_textEdit.clear()
            self.view.ui.detail_from_textEdit.setEnabled(True)
            self.view.ui.save_form_pushButton.setEnabled(True)
            self.view.ui.Download_form_pushButton.setEnabled(False)

    def get_app_root_path(self):
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            application_path = os.path.dirname(current_dir)
        return application_path

    def on_item_selection_changed(self):
        selected_items = self.view.ui.list_detail_treeWidget.selectedItems()
        if not selected_items:
            # ถ้าไม่มีการเลือก ให้ Reset กลับไปสถานะเริ่มต้น (พร้อมสำหรับ New Form)
            self.set_initial_ui_state()
            return

        item = selected_items[0]
        report_id = item.data(0, 1000)
        
        if not report_id:
            # กรณีคลิก Group Header — เตรียม New Form Mode โดยเลือก lab นั้นไว้ล่วงหน้า
            self.set_initial_ui_state()
            lab_name = item.text(0)
            combo = self.view.ui.lab_name_comboBox
            combo.blockSignals(True)
            combo.setCurrentText(lab_name)
            combo.blockSignals(False)
            combo.setEnabled(True)
            self.view.ui.form_name_lineEdit.setEnabled(True)
            self.view.ui.detail_from_textEdit.setEnabled(True)
            self.view.ui.save_form_pushButton.setEnabled(True)
            return

        # --- EDIT MODE SETUP ---
        self.editing_report_id = report_id
        self.current_report_path = item.data(0, 1001)
        self.current_lab_name_of_item = item.data(0, 1002)
        self.pending_file_path = None

        # Display Data
        report_name = item.text(0)
        detail = item.text(2)

        self.view.ui.form_name_lineEdit.setText(report_name)
        self.view.ui.detail_from_textEdit.setText(detail)

        parent_item = item.parent()
        if parent_item:
            combo = self.view.ui.lab_name_comboBox
            combo.blockSignals(True)
            combo.setCurrentText(parent_item.text(0))
            combo.blockSignals(False)

        # Enable UI for Edit
        self.view.ui.lab_name_comboBox.setEnabled(True)
        self.view.ui.form_name_lineEdit.setEnabled(True)
        self.view.ui.detail_from_textEdit.setEnabled(True)
        self.view.ui.save_form_pushButton.setEnabled(True)
        self.view.ui.Download_form_pushButton.setEnabled(True)

    def edit_form_pushButton_clicked(self):
        """
        ปุ่มนี้ทำหน้าที่ 2 อย่าง:
        1. ถ้าเลือกรายการอยู่ (Edit) -> เปลี่ยนไฟล์ (Change File)
        2. ถ้าไม่ได้เลือกรายการ (New) -> เลือกไฟล์เพื่อสร้างฟอร์มใหม่ (New Form)
        """
        # เปิด File Dialog เหมือนกันทั้ง 2 กรณี
        file_dialog = QFileDialog(self.view)
        file_dialog.setNameFilter("Word Documents (*.docx *.doc)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.pending_file_path = selected_files[0]
                file_name = os.path.basename(self.pending_file_path)

                if self.editing_report_id:
                    # --- CASE 1: EDIT MODE ---
                    QMessageBox.information(self.view, "Info", f"เปลี่ยนไฟล์สำหรับรายการที่เลือกเป็น:\n{file_name}\n\nกด 'บันทึกแบบฟอร์ม' เพื่อยืนยัน")
                else:
                    # --- CASE 2: NEW FORM MODE ---
                    # ดึงชื่อไฟล์มาเป็นชื่อฟอร์มอัตโนมัติ (ตัดนามสกุลออก)
                    name_only = os.path.splitext(file_name)[0]
                    self.view.ui.form_name_lineEdit.setText(name_only)
                    
                    # เปิดการใช้งานช่องกรอกข้อมูล
                    self.view.ui.lab_name_comboBox.setEnabled(True)
                    self.view.ui.form_name_lineEdit.setEnabled(True)
                    self.view.ui.detail_from_textEdit.setEnabled(True)
                    self.view.ui.save_form_pushButton.setEnabled(True)
                    
                    QMessageBox.information(self.view, "Info", f"เตรียมเพิ่มแบบฟอร์มใหม่:\n{file_name}\n\nกรุณาตรวจสอบชื่อและกด 'บันทึกแบบฟอร์ม'")

    def save_form_pushButton_clicked(self):
        """
        ปุ่ม Save ทำหน้าที่ 2 อย่างตามสถานะ self.editing_report_id
        """
        try:
            # 1. Validate Input
            new_report_name = self.view.ui.form_name_lineEdit.text().strip()
            if not new_report_name:
                QMessageBox.warning(self.view, "Warning", "กรุณากรอกชื่อแบบฟอร์ม")
                return

            root_path = self.get_app_root_path()
            user_id = 1
            if self.main_controller:
                user_id = self.main_controller.get_logged_in_user_id() or 1

            # --- 2. Determine Logic (Edit vs New) ---
            lab_name_to_save = self.view.ui.lab_name_comboBox.currentText().strip()
            detail_text = self.view.ui.detail_from_textEdit.toPlainText().strip()

            if self.editing_report_id:
                # ================= EDIT MODE (VERSIONING) =================
                final_path = self.current_report_path

                # Upload File to Backend if changed
                if self.pending_file_path:
                    upload_ok, result = self.report_info_service.upload_file(
                        local_file_path=self.pending_file_path,
                        lab_name=lab_name_to_save,
                        from_name=new_report_name
                    )
                    if not upload_ok:
                        QMessageBox.critical(self.view, "Error", f"อัพโหลดไฟล์ล้มเหลว: {result}")
                        return
                    final_path = result  # path ที่ Backend ได้ให้มา

                success, message = self.report_info_service.save_new_report_version(
                    old_report_id=self.editing_report_id,
                    new_name=new_report_name,
                    new_path=final_path,
                    lab_name=lab_name_to_save,
                    updater=user_id,
                    comment=detail_text
                )

            else:
                # ================= NEW FORM MODE (INSERT) =================
                if not self.pending_file_path:
                    QMessageBox.warning(self.view, "Warning", "กรุณาเลือกไฟล์ก่อนบันทึก (กดปุ่มเพิ่มแบบฟอร์ม)")
                    return

                # Upload File to Backend
                upload_ok, result = self.report_info_service.upload_file(
                    local_file_path=self.pending_file_path,
                    lab_name=lab_name_to_save,
                    from_name=new_report_name
                )
                if not upload_ok:
                    QMessageBox.critical(self.view, "Error", f"อัพโหลดไฟล์ล้มเหลว: {result}")
                    return
                dest_path = result  # path ที่ Backend ได้ให้มา

                success, message = self.report_info_service.add_report(
                    from_name=new_report_name,
                    lab_name=lab_name_to_save,
                    location_file=dest_path,
                    updater=user_id,
                    comment=detail_text
                )

            # --- 3. Result Handling ---
            if success:
                action_text = "แก้ไข" if self.editing_report_id else "เพิ่ม"
                QMessageBox.information(self.view, "Success", f"{action_text}ข้อมูลเรียบร้อยแล้ว")
                self.set_initial_ui_state()
                self.reload_data()
            else:
                QMessageBox.critical(self.view, "Error", f"บันทึกข้อมูลล้มเหลว: {message}")

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            QMessageBox.critical(self.view, "Error", f"เกิดข้อผิดพลาด: {str(e)}")

    def delete_pushButton_clicked(self):
        selected_items = self.view.ui.list_detail_treeWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.view, "Warning", "กรุณาเลือกรายการที่ต้องการลบ")
            return
            
        item = selected_items[0]
        report_id = item.data(0, 1000)
        
        if not report_id:
            QMessageBox.warning(self.view, "Warning", "ไม่สามารถลบหัวข้อกลุ่มได้")
            return

        confirm = QMessageBox.question(
            self.view, 
            "Confirm Delete", 
            f"คุณต้องการลบรายงาน '{item.text(0)}' ใช่หรือไม่?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            user_id = 1
            if self.main_controller:
                user_id = self.main_controller.get_logged_in_user_id() or 1
                
            success, message = self.report_info_service.delete_report(report_id, user_id)
            
            if success:
                QMessageBox.information(self.view, "Success", "ลบข้อมูลเรียบร้อยแล้ว")
                self.set_initial_ui_state()
                self.reload_data()
            else:
                QMessageBox.critical(self.view, "Error", f"เกิดข้อผิดพลาดในการลบ: {message}")

    def save_new_lab_pushButton_clicked(self):
        """บันทึก lab_name ใหม่เข้า database และเพิ่มเข้า comboBox"""
        new_lab_name = self.view.ui.new_lab_name_lineEdit.text().strip()
        if not new_lab_name:
            QMessageBox.warning(self.view, "Warning", "กรุณากรอกชื่อห้องปฏิบัติการ")
            return

        user_id = 1
        if self.main_controller:
            user_id = self.main_controller.get_logged_in_user_id() or 1

        success, message = self.report_info_service.add_lab_name(new_lab_name, user_id)

        if not success:
            # 409 = มีอยู่แล้ว ให้แสดง warning แต่ยังเพิ่มเข้า comboBox ได้
            if "already exists" in message:
                QMessageBox.warning(self.view, "Warning", f"ห้องปฏิบัติการ '{new_lab_name}' มีอยู่ใน database แล้ว")
            else:
                QMessageBox.critical(self.view, "Error", f"บันทึกล้มเหลว: {message}")
            return

        # เพิ่มเข้า comboBox ถ้ายังไม่มี
        combo = self.view.ui.lab_name_comboBox
        existing = [combo.itemText(i) for i in range(combo.count())]
        if new_lab_name not in existing:
            combo.addItem(new_lab_name)
        combo.setCurrentText(new_lab_name)

        self.view.ui.new_lab_name_lineEdit.clear()
        self.view.ui.new_lab_detail_textEdit.clear()
        self.reload_data()
        QMessageBox.information(self.view, "Success", f"เพิ่มห้องปฏิบัติการ '{new_lab_name}' เรียบร้อยแล้ว")

    def download_pushButton_clicked(self):
        selected_items = self.view.ui.list_detail_treeWidget.selectedItems()
        if not selected_items:
            return
            
        item = selected_items[0]
        relative_path = item.data(0, 1001)  # location_file เก็บเป็น relative path (Backend-relative)
        report_name = item.text(0)
        
        if not relative_path:
            QMessageBox.critical(self.view, "Error", "ไม่พบไฟล์ต้นฉบับ")
            return

        _, file_extension = os.path.splitext(relative_path)
        default_filename = f"{report_name}{file_extension}"

        save_path, _ = QFileDialog.getSaveFileName(
            self.view, "บันทึกแบบฟอร์ม", default_filename, f"Document Files (*{file_extension});;All Files (*.*)"
        )

        if save_path:
            try:
                success, result = self.report_info_service.download_file(relative_path, save_path)
                if success:
                    QMessageBox.information(self.view, "Success", f"ดาวน์โหลดเรียบร้อยแล้วที่: {save_path}")
                else:
                    QMessageBox.critical(self.view, "Error", f"ดาวน์โหลดล้มเหลว: {result}")
            except Exception as e:
                QMessageBox.critical(self.view, "Error", str(e))

    def reload_data(self):
        self.load_report_data()
    
    def _apply_group_permissions(self):
        """เปิด/ปิด new_lab_frame ตาม group_id (เฉพาะ group 1, 2 เท่านั้น)"""
        allowed = self.user_group_id in (1, 2)
        self.view.ui.new_lab_name_lineEdit.setEnabled(allowed)
        self.view.ui.new_lab_detail_textEdit.setEnabled(allowed)
        self.view.ui.save_new_lab_pushButton.setEnabled(allowed)
        self.view.ui.new_lab_frame.setVisible(allowed)

    def set_user_group_id(self, group_id):
        """เก็บ group_id ของ user (เรียกจาก MainController)"""
        self.user_group_id = group_id
        self._apply_group_permissions()

    def set_room_id(self, room_id: int):
        self.user_room_id = room_id
    
    def load_report_data(self):
        reports = self.report_info_service.get_all_reports_with_status(status=1)
        self.populate_tree_widget(reports)
    
    def populate_tree_widget(self, reports):
        tree = self.view.ui.list_detail_treeWidget
        combo = self.view.ui.lab_name_comboBox
        
        if tree is None: return
        tree.clear()
        combo.clear()

        if not reports: return

        # Group by lab_name (รวมทั้งแถวที่ from_name ว่าง เพื่อเอา lab header ขึ้นมาด้วย)
        grouped_reports = {}
        for report in reports:
            group_key = report.get('lab_name', 'Unknown')
            if group_key not in grouped_reports:
                grouped_reports[group_key] = []
            grouped_reports[group_key].append(report)

        combo.blockSignals(True)
        combo.addItems(list(grouped_reports.keys()))
        combo.blockSignals(False)

        for group_name, group_reports in grouped_reports.items():
            # กรองเฉพาะฟอร์มที่มีชื่อจริง (ไม่ใช่ placeholder จาก add_lab_name)
            real_forms = [r for r in group_reports if r.get('from_name', '').strip()]

            parent_item = QTreeWidgetItem(tree)
            parent_item.setText(0, group_name)
            parent_item.setText(1, str(len(real_forms)))  # นับเฉพาะฟอร์มจริง
            parent_item.setText(2, "")

            for report in real_forms:
                child_item = QTreeWidgetItem(parent_item)
                child_item.setText(0, report.get('from_name', ''))
                child_item.setText(1, "")
                child_item.setText(2, report.get('comment', ''))
                child_item.setData(0, 1000, report['id'])
                child_item.setData(0, 1001, report.get('location_file', ''))
                child_item.setData(0, 1002, report.get('lab_name', ''))

        tree.collapseAll()