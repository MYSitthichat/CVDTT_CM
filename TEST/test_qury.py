import sys
import mariadb
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                               QLineEdit, QLabel, QCompleter, QMessageBox)
from PySide6.QtCore import QStringListModel, Qt

# --- ตั้งค่า Database ---
DB_CONFIG = {
    "host": "202.28.24.55",
    "user": "python_engine",
    "password": "c#@4573kt",
    "database": "cvdtt_lab",
    "port": 3306
}

class MariaDBOfficialSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ระบบค้นหา (Official MariaDB Driver)")
        self.resize(600, 150)

        self.conn = None
        self.connect_db()

        layout = QVBoxLayout()
        self.label = QLabel("ค้นหาชื่อผู้ป่วย (Official Driver):")
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("พิมพ์ชื่ออย่างน้อย 2 ตัวอักษร...")
        self.search_box.setStyleSheet("font-size: 16px; padding: 5px;")

        # Setup Completer
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        
        self.model = QStringListModel()
        self.completer.setModel(self.model)
        self.search_box.setCompleter(self.completer)

        self.search_box.textChanged.connect(self.update_search_results)

        layout.addWidget(self.label)
        layout.addWidget(self.search_box)
        self.setLayout(layout)

    def connect_db(self):
        try:
            self.conn = mariadb.connect(**DB_CONFIG)
            print("✅ Connected to MariaDB (Official Driver)")
            
        except mariadb.Error as e: # <--- จับ Error เฉพาะของ MariaDB
            QMessageBox.critical(self, "Connection Error", f"เชื่อมต่อไม่ได้:\n{e}")
            sys.exit()

    def update_search_results(self, text):
            if len(text) < 2:
                return

            # เช็คว่า Connection ยังอยู่ไหม (Logic ต่างจาก pymysql นิดหน่อย)
            try:
                # ลอง ping ดูว่ายังต่ออยู่ไหม (ถ้าหลุดจะ throw Error)
                self.conn.ping() 
            except mariadb.Error:
                print("⚠️ Connection lost, reconnecting...")
                self.connect_db()

            try:
                cursor = self.conn.cursor()
                
                # SQL Statement
                sql = "SELECT name FROM customer WHERE name LIKE ? LIMIT 20"
                # หมายเหตุ: Official Driver ใช้เครื่องหมาย ? แทน %s ในการแทนค่า
                val = (f"%{text}%", )
                
                cursor.execute(sql, val)
                
                # ดึงข้อมูล (Official Driver คืนค่าเป็น Tuple ตามปกติ)
                # row[0] คือ name
                results = [row[0] for row in cursor]

                self.model.setStringList(results)
                
                if results:
                    self.completer.complete()
                    
                cursor.close()
                
            except mariadb.Error as e:
                print(f"Query Error: {e}")

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MariaDBOfficialSearchApp()
    window.show()
    sys.exit(app.exec())