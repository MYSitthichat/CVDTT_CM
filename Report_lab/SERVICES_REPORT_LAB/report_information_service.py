from SERVICES_REPORT_LAB.base_service import BaseService
import sys
import os

class ReportInformationService(BaseService):
    """Service for managing report_information table data"""
    
    def get_reports_by_room_and_status(self, room_id: int, status: int = 1):
        """
        ดึงข้อมูลจาก report_information table โดยกรองตาม room_id และ status
        
        Args:
            room_id: ID ของห้องที่ต้องการดึงข้อมูล
            status: สถานะของรายงาน (1 = แสดง, 0 = ซ่อน), default = 1
            
        Returns:
            list: รายการข้อมูลรายงานที่ตรงตามเงื่อนไข
        """
        print(f"DEBUG ReportInformationService: get_reports_by_room_and_status called with room_id={room_id}, status={status}")
        try:
            # หา path ของ BACKEND folder
            current_file = os.path.abspath(__file__)
            report_lab_path = os.path.dirname(os.path.dirname(current_file))
            project_path = os.path.dirname(report_lab_path)
            backend_path = os.path.join(project_path, 'BACKEND')
            
            print(f"DEBUG ReportInformationService: backend_path = {backend_path}")
            
            if backend_path not in sys.path:
                sys.path.insert(0, backend_path)
                print(f"DEBUG ReportInformationService: Added backend_path to sys.path")
            
            from database import get_db_connection
            
            conn = get_db_connection()
            if conn is None:
                print("ERROR ReportInformationService: Cannot connect to database")
                return []
            
            print(f"DEBUG ReportInformationService: Database connection successful")
            cursor = conn.cursor()
            
            query = """
                SELECT id, report_name, room_id, report_path, updater, status 
                FROM report_information 
                WHERE room_id = ? AND status = ?
                ORDER BY report_name
            """
            print(f"DEBUG ReportInformationService: Executing query with room_id={room_id}, status={status}")
            cursor.execute(query, (room_id, status))
            
            results = cursor.fetchall()
            print(f"DEBUG ReportInformationService: Query returned {len(results)} rows")
            
            if len(results) > 0:
                print(f"DEBUG ReportInformationService: First result: {results[0]}")
            
            reports = []
            for row in results:
                report_info = {
                    'id': row[0],
                    'report_name': row[1],
                    'room_id': row[2],
                    'report_path': row[3],
                    'updater': row[4],
                    'status': row[5]
                }
                reports.append(report_info)
            
            cursor.close()
            conn.close()
            
            return reports
            
        except Exception as e:
            import traceback
            print(f"ERROR getting reports by room and status: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            return []
    
    def get_all_reports_with_status(self, status: int = 1):
        """
        ดึงข้อมูลรายงานทั้งหมดโดยกรองตาม status เท่านั้น
        (ใช้สำหรับ admin หรือผู้ที่ดูได้ทุกห้อง)
        
        Args:
            status: สถานะของรายงาน (1 = แสดง, 0 = ซ่อน), default = 1
            
        Returns:
            list: รายการข้อมูลรายงานทั้งหมดที่มี status ตามที่กำหนด
        """
        try:
            # หา path ของ BACKEND folder
            current_file = os.path.abspath(__file__)
            report_lab_path = os.path.dirname(os.path.dirname(current_file))
            project_path = os.path.dirname(report_lab_path)
            backend_path = os.path.join(project_path, 'BACKEND')
            
            if backend_path not in sys.path:
                sys.path.insert(0, backend_path)
            
            from database import get_db_connection
            
            conn = get_db_connection()
            if conn is None:
                print("ERROR: Cannot connect to database")
                return []
            
            cursor = conn.cursor()
            
            query = """
                SELECT id, report_name, room_id, report_path, updater, status 
                FROM report_information 
                WHERE status = ?
                ORDER BY room_id, report_name
            """
            cursor.execute(query, (status,))
            
            results = cursor.fetchall()
            print(f"DEBUG ReportInformationService: Found {len(results)} reports with status={status}")
            
            reports = []
            for row in results:
                report_info = {
                    'id': row[0],
                    'report_name': row[1],
                    'room_id': row[2],
                    'report_path': row[3],
                    'updater': row[4],
                    'status': row[5]
                }
                reports.append(report_info)
            
            cursor.close()
            conn.close()
            
            return reports
            
        except Exception as e:
            import traceback
            print(f"ERROR getting all reports with status: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            return []
        
    def update_report_path(self, report_id: int, new_path: str, updater_id: int):
        """
        อัปเดต path ของไฟล์รายงานและผู้แก้ไข
        """
        try:
            # Setup path เพื่อ import database (เหมือนฟังก์ชันอื่น)
            current_file = os.path.abspath(__file__)
            report_lab_path = os.path.dirname(os.path.dirname(current_file))
            project_path = os.path.dirname(report_lab_path)
            backend_path = os.path.join(project_path, 'BACKEND')
            
            if backend_path not in sys.path:
                sys.path.insert(0, backend_path)
            
            from database import get_db_connection
            
            conn = get_db_connection()
            if conn is None:
                return False, "Database connection failed"
            
            cursor = conn.cursor()
            
            query = """
                UPDATE report_information 
                SET report_path = ?, updater = ?
                WHERE id = ?
            """
            cursor.execute(query, (new_path, updater_id, report_id))
            conn.commit()
            
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            if rows_affected > 0:
                return True, "Update successful"
            else:
                return False, "No report found with this ID"
                
        except Exception as e:
            print(f"ERROR update_report_path: {e}")
            return False, str(e)
        
    def update_report_data(self, report_id: int, report_name: str, report_path: str, updater_id: int):
        """
        อัปเดตข้อมูลรายงาน (ชื่อและ Path)
        """
        try:
            # Setup path
            current_file = os.path.abspath(__file__)
            report_lab_path = os.path.dirname(os.path.dirname(current_file))
            project_path = os.path.dirname(report_lab_path)
            backend_path = os.path.join(project_path, 'BACKEND')
            
            if backend_path not in sys.path:
                sys.path.insert(0, backend_path)
            
            from database import get_db_connection
            
            conn = get_db_connection()
            if conn is None:
                return False, "Database connection failed"
            
            cursor = conn.cursor()
            
            # Update ชื่อรายงาน และ Path
            query = """
                UPDATE report_information 
                SET report_name = ?, report_path = ?, updater = ?
                WHERE id = ?
            """
            cursor.execute(query, (report_name, report_path, updater_id, report_id))
            conn.commit()
            
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            if rows_affected > 0:
                return True, "Update successful"
            else:
                return False, "No report found with this ID"
                
        except Exception as e:
            print(f"ERROR update_report_data: {e}")
            return False, str(e)
        
    def delete_report(self, report_id: int, updater_id: int):
        """
        ลบรายการโดยการเปลี่ยน status เป็น 0 (Soft Delete)
        """
        try:
            current_file = os.path.abspath(__file__)
            report_lab_path = os.path.dirname(os.path.dirname(current_file))
            project_path = os.path.dirname(report_lab_path)
            backend_path = os.path.join(project_path, 'BACKEND')
            
            if backend_path not in sys.path:
                sys.path.insert(0, backend_path)
            
            from database import get_db_connection
            conn = get_db_connection()
            if conn is None: return False, "Database connection failed"
            cursor = conn.cursor()
            
            # Update status เป็น 0
            query = "UPDATE report_information SET status = 0, updater = ? WHERE id = ?"
            cursor.execute(query, (updater_id, report_id))
            conn.commit()
            
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            if rows_affected > 0:
                return True, "Delete successful"
            else:
                return False, "Report not found"
        except Exception as e:
            print(f"ERROR delete_report: {e}")
            return False, str(e)
        
    def save_new_report_version(self, old_report_id: int, new_name: str, new_path: str, room_id: int, updater_id: int):
        """
        บันทึกการแก้ไขโดย:
        1. เปลี่ยน status ตัวเก่าเป็น 0
        2. เพิ่มรายการใหม่ (Insert) ที่มี status 1
        """
        try:
            current_file = os.path.abspath(__file__)
            report_lab_path = os.path.dirname(os.path.dirname(current_file))
            project_path = os.path.dirname(report_lab_path)
            backend_path = os.path.join(project_path, 'BACKEND')
            
            if backend_path not in sys.path:
                sys.path.insert(0, backend_path)
            
            from database import get_db_connection
            conn = get_db_connection()
            if conn is None: return False, "Database connection failed"
            cursor = conn.cursor()
            
            try:
                # 1. เปลี่ยน Status ตัวเก่าเป็น 0
                update_query = "UPDATE report_information SET status = 0 WHERE id = ?"
                cursor.execute(update_query, (old_report_id,))
                
                # 2. เพิ่มรายการใหม่ (Status 1)
                insert_query = """
                    INSERT INTO report_information (report_name, room_id, report_path, updater, status)
                    VALUES (?, ?, ?, ?, 1)
                """
                cursor.execute(insert_query, (new_name, room_id, new_path, updater_id))
                
                conn.commit()
                cursor.close()
                conn.close()
                return True, "Version update successful"
                
            except Exception as db_err:
                conn.rollback() # ถ้ามี error ให้ยกเลิกทั้ง 2 คำสั่ง
                cursor.close()
                conn.close()
                raise db_err

        except Exception as e:
            print(f"ERROR save_new_report_version: {e}")
            return False, str(e)

    def add_report(self, report_name: str, room_id: int, report_path: str, updater_id: int):
        """
        เพิ่มรายงานใหม่ (INSERT) โดยกำหนด status = 1
        """
        try:
            # Setup path
            current_file = os.path.abspath(__file__)
            report_lab_path = os.path.dirname(os.path.dirname(current_file))
            project_path = os.path.dirname(report_lab_path)
            backend_path = os.path.join(project_path, 'BACKEND')
            
            if backend_path not in sys.path:
                sys.path.insert(0, backend_path)
            
            from database import get_db_connection
            
            conn = get_db_connection()
            if conn is None:
                return False, "Database connection failed"
            
            cursor = conn.cursor()
            
            query = """
                INSERT INTO report_information (report_name, room_id, report_path, updater, status)
                VALUES (?, ?, ?, ?, 1)
            """
            cursor.execute(query, (report_name, room_id, report_path, updater_id))
            conn.commit()
            
            last_id = cursor.lastrowid # รับ ID ล่าสุดที่ insert
            cursor.close()
            conn.close()
            
            if last_id: 
                return True, "Add successful"
            else:
                return False, "Failed to add report"
                
        except Exception as e:
            print(f"ERROR add_report: {e}")
            return False, str(e)