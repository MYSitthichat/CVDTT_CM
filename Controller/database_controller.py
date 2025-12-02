import mariadb
from PySide6.QtCore import QObject
import datetime

# Remote Database Configuration
DB_CONFIG = {
    "host": "202.28.24.55",
    "user": "python_engine",
    "password": "c#@4573kt",
    "database": "cvdtt_lab",
    "port": 3306
}

# DB_CONFIG = {
#     "host": "127.0.0.1",
#     "user": "root",
#     "password": "",
#     "database": "cvdtt_lab",
#     "port": 3306
# }

class DatabaseController(QObject):
    def __init__(self):
        super().__init__()
        self.conn = None
        self.connect_db()

    def connect_db(self):
        if self.conn is None:
            try:
                self.conn = mariadb.connect(**DB_CONFIG)
                print("Database Connected Successfully")
            except mariadb.Error as e:
                print(f"Connection Error: {e}")
                self.conn = None

    def is_connected(self):
        return self.conn is not None

    def check_login(self, username, password):
        return True

    # ==========================================
    #           BARCODE PAGE FUNCTIONS
    # ==========================================
    
    def get_today_case_detail(self):
        if not self.conn: self.connect_db()
        if not self.conn: return []

        try:
            cursor = self.conn.cursor()
            sql = """
                SELECT 
                    c.dtime,        
                    c.id,           
                    s.species,      
                    CONCAT(IFNULL(r.code, ''), '(', IFNULL(r.nickname, ''), ')'),
                    s.keep_method,  
                    s.speed         
                FROM case_registration c
                JOIN sample_registration s ON c.id = s.case_id
                LEFT JOIN room_information r ON s.room = r.id
                WHERE DATE(c.dtime) = CURDATE()
            """
            cursor.execute(sql)
            results = [list(row) for row in cursor]
            cursor.close()
            return results
        except mariadb.Error as e:
            print(f"Search Today Error: {e}")
            return []

    def get_case_detail_by_customer_name(self, name, surname):
        if not self.conn: self.connect_db()
        if not self.conn: return []

        try:
            cursor = self.conn.cursor()
            sql = """
                SELECT 
                    c.dtime, 
                    c.id, 
                    s.species, 
                    CONCAT(IFNULL(r.code, ''), '(', IFNULL(r.nickname, ''), ')'),
                    s.keep_method, 
                    s.speed 
                FROM case_registration c
                JOIN sample_registration s ON c.id = s.case_id
                JOIN customer cust ON c.owner_id = cust.id
                LEFT JOIN room_information r ON s.room = r.id
                WHERE cust.name LIKE ? OR cust.surname LIKE ?
            """
            cursor.execute(sql, (f"%{name}%", f"%{surname}%"))
            results = [list(row) for row in cursor]
            cursor.close()
            return results
        except mariadb.Error as e:
            print(f"Search Customer Error: {e}")
            return []

    # ==========================================
    #       CHECK JOB PROGRESS FUNCTIONS
    # ==========================================

    def get_job_detail_in_check_job_progress_page(self):
        """ Get all active jobs (Top Table) """
        if not self.conn: self.connect_db()
        if not self.conn: return []

        try:
            cursor = self.conn.cursor()
            sql = """
                SELECT 
                    t.dtime, 
                    t.lab_order_id, 
                    t.tracking_info
                FROM tracking_lab_order t
                ORDER BY t.dtime DESC
            """
            cursor.execute(sql)
            results = [list(row) for row in cursor]
            cursor.close()
            return results
        except mariadb.Error as e:
            print(f"Search Active Jobs Error: {e}")
            return []

    def get_job_detail_in_check_job_progress_page_by_id(self, job_id):
        """ Get detailed history for a specific job ID (Bottom Table) """
        if not self.conn: self.connect_db()
        if not self.conn: return []

        try:
            cursor = self.conn.cursor()
            sql = """
                SELECT 
                    t.dtime, 
                    t.lab_order_id, 
                    t.tracking_info, 
                    CONCAT(IFNULL(e.name, ''), ' ', IFNULL(e.surname, ''))
                FROM tracking_lab_order t
                LEFT JOIN employee e ON t.receiver = e.id
                WHERE t.lab_order_id = ?
                ORDER BY t.dtime DESC
            """
            cursor.execute(sql, (job_id,))
            results = [list(row) for row in cursor]
            cursor.close()
            return results
        except mariadb.Error as e:
            print(f"Get Job Detail Error: {e}")
            return []

    # ==========================================
    #      LAB RECEIVED SAMPLE FUNCTIONS
    # ==========================================

    def search_employee_by_name(self, search_text):
        """ Search for employees by name or surname """
        if not self.conn: self.connect_db()
        if not self.conn: return []

        try:
            cursor = self.conn.cursor()
            # Select ID, Name, Surname
            sql = """
                SELECT id, name, surname 
                FROM employee 
                WHERE name LIKE ? OR surname LIKE ?
            """
            term = f"%{search_text}%"
            cursor.execute(sql, (term, term))
            results = [list(row) for row in cursor]
            cursor.close()
            return results
        except mariadb.Error as e:
            print(f"Search Employee Error: {e}")
            return []

    def save_tracking_information(self, barcode_id, receiver_id, updater_id, info_text):
        """ Save new tracking log entry """
        if not self.conn: self.connect_db()
        if not self.conn: return False

        try:
            cursor = self.conn.cursor()
            # We insert current time (NOW())
            sql = """
                INSERT INTO tracking_lab_order 
                (dtime, lab_order_id, tracking_info, receiver, updater, status)
                VALUES (NOW(), ?, ?, ?, ?, ?)
            """
            # We use the 'info_text' for both 'tracking_info' and 'status' columns
            # based on your previous code patterns.
            cursor.execute(sql, (barcode_id, info_text, receiver_id, updater_id, info_text))
            self.conn.commit()
            cursor.close()
            return True
        except mariadb.Error as e:
            print(f"Save Tracking Error: {e}")
            return False

    def close_db(self):
        if self.conn:
            self.conn.close()
            self.conn = None