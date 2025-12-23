from .base_service import BaseService

class ReceiveLabService(BaseService):
    def get_lab_order_to_day(self, room_id: str, offset=0, limit=50):
        params = {"room_id": room_id, "offset": offset, "limit": limit}
        result = self._get("/get_lab_order/to_day", params=params)
        return result if result is not None else None
    
    def get_lab_order_by_barcode(self, barcode: str, room_id: str = ""):
        """Search lab order by barcode with room_id access control"""
        params = {"barcode": barcode, "room_id": room_id}
        result = self._get("/get_lab_order/barcode", params=params)
        return result if result is not None else None
    
    def get_lab_order_details(self, lab_order_id: str, room_id: str):
        """ดึงรายละเอียดของ Lab Order สำหรับแสดงใน Dialog"""
        params = {"lab_order_id": lab_order_id, "room_id": room_id}
        result = self._get("/get_lab_order/details", params=params)
        return result if result is not None else None
    
    def receive_lab_order(self, lab_order_id: int, receive_from_room: int, comment_for_sample: str, sample_status: str, updater_id: int):
        """บันทึกการรับแลป"""
        data = {
            "lab_order_id": lab_order_id,
            "receive_from_room": receive_from_room,
            "comment_for_sample": comment_for_sample,
            "sample_status": sample_status,
            "updater_id": updater_id
        }
        result = self._post("/receive_lab_order", json=data)
        return result if result is not None else None
    
    def reject_lab_order(self, lab_order_id: int, receive_from_room: int, comment_for_sample: str, sample_status: str, updater_id: int):
        """ปฏิเสธการรับแลป"""
        data = {
            "lab_order_id": lab_order_id,
            "receive_from_room": receive_from_room,
            "comment_for_sample": comment_for_sample,
            "sample_status": sample_status,
            "updater_id": updater_id
        }
        result = self._post("/reject_lab_order", json=data)
        return result if result is not None else None
    
    def get_report_templates(self, room_id: int = None):
        """ดึงรายการ report templates จาก database"""
        try:
            import sys
            import os
            
            # หา path ของ BACKEND folder
            current_file = os.path.abspath(__file__)
            print(f"DEBUG Service: current_file = {current_file}")
            
            # Report_lab/SERVICES_REPORT_LAB/receive_lab_service.py -> BACKEND
            report_lab_path = os.path.dirname(os.path.dirname(current_file))  # Report_lab
            project_path = os.path.dirname(report_lab_path)  # CVDTT_CM
            backend_path = os.path.join(project_path, 'BACKEND')
            
            print(f"DEBUG Service: backend_path = {backend_path}")
            print(f"DEBUG Service: backend_path exists = {os.path.exists(backend_path)}")
            
            if backend_path not in sys.path:
                sys.path.insert(0, backend_path)
            
            from database import get_db_connection
            
            conn = get_db_connection()
            if conn is None:
                print("DEBUG Service: ไม่สามารถเชื่อมต่อ database")
                return []
            
            cursor = conn.cursor()
            
            if room_id:
                query = "SELECT id, report_name, room_id, report_path, updater FROM report_information WHERE room_id = ?"
                cursor.execute(query, (room_id,))
                print(f"DEBUG Service: query with room_id = {room_id}")
            else:
                query = "SELECT id, report_name, room_id, report_path, updater FROM report_information"
                cursor.execute(query)
                print("DEBUG Service: query all templates")
            
            results = cursor.fetchall()
            print(f"DEBUG Service: พบผลลัพธ์ {len(results)} รายการ")
            
            templates = []
            for row in results:
                template_info = {
                    'id': row[0],
                    'report_name': row[1],
                    'room_id': row[2],
                    'report_path': row[3],
                    'updater': row[4]
                }
                templates.append(template_info)
                print(f"DEBUG Service: - {template_info['report_name']}")
            
            cursor.close()
            conn.close()
            
            return templates
        except Exception as e:
            import traceback
            print(f"Error getting report templates: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            return []
