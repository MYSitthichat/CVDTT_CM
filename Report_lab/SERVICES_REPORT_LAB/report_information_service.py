from .base_service import BaseService


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
        try:
            params = {"room_id": room_id, "status": status}
            result = self._get("/report_information/by_room_and_status", params=params)
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and "data" in result:
                return result["data"]
            else:
                return []
        except Exception as e:
            print(f"ERROR getting reports by room and status: {e}")
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
            params = {"status": status}
            result = self._get("/report_information/all_by_status", params=params)
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and "data" in result:
                return result["data"]
            else:
                return []
        except Exception as e:
            print(f"ERROR getting all reports with status: {e}")
            return []
        
    def update_report_path(self, report_id: int, new_path: str, updater_id: int):
        """
        อัปเดต path ของไฟล์รายงานและผู้แก้ไข
        """
        try:
            data = {
                "report_id": report_id,
                "new_path": new_path,
                "updater_id": updater_id
            }
            result = self._put("/report_information/update_path", json=data)
            if isinstance(result, dict) and result.get("status") == "success":
                return True, "Update successful"
            else:
                return False, result.get("detail", "Update failed")
        except Exception as e:
            print(f"ERROR update_report_path: {e}")
            return False, str(e)
        
    def update_report_data(self, report_id: int, report_name: str, report_path: str, updater_id: int):
        """
        อัปเดตข้อมูลรายงาน (ชื่อและ Path)
        """
        try:
            data = {
                "report_id": report_id,
                "report_name": report_name,
                "report_path": report_path,
                "updater_id": updater_id
            }
            result = self._put("/report_information/update_data", json=data)
            if isinstance(result, dict) and result.get("status") == "success":
                return True, "Update successful"
            else:
                return False, result.get("detail", "Update failed")
        except Exception as e:
            print(f"ERROR update_report_data: {e}")
            return False, str(e)
        
    def delete_report(self, report_id: int, updater_id: int):
        """
        ลบรายการโดยการเปลี่ยน status เป็น 0 (Soft Delete)
        """
        try:
            params = {"report_id": report_id, "updater_id": updater_id}
            result = self._delete("/report_information/delete", params=params)
            if isinstance(result, dict) and result.get("status") == "success":
                return True, "Delete successful"
            else:
                return False, result.get("detail", "Delete failed")
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
            data = {
                "old_report_id": old_report_id,
                "new_name": new_name,
                "new_path": new_path,
                "room_id": room_id,
                "updater_id": updater_id
            }
            result = self._post("/report_information/save_new_version", json=data)
            if isinstance(result, dict) and result.get("status") == "success":
                return True, "Save new version successful"
            else:
                return False, result.get("detail", "Save new version failed")
        except Exception as e:
            print(f"ERROR save_new_report_version: {e}")
            return False, str(e)

    def add_report(self, report_name: str, room_id: int, report_path: str, updater_id: int):
        """
        เพิ่มรายงานใหม่ (INSERT) โดยกำหนด status = 1
        """
        try:
            data = {
                "report_name": report_name,
                "room_id": room_id,
                "report_path": report_path,
                "updater_id": updater_id
            }
            result = self._post("/report_information/add", json=data)
            if isinstance(result, dict) and result.get("status") == "success":
                return True, "Add report successful"
            else:
                return False, result.get("detail", "Add report failed")
        except Exception as e:
            print(f"ERROR add_report: {e}")
            return False, str(e)