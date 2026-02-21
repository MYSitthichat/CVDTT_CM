from SERVICES_REPORT_LAB.base_service import BaseService
import requests
import os

class ReportInformationService(BaseService):
    def get_reports_by_room_and_status(self, lab_name: str, status: int = 1):
        try:
            response = self._get(
                "/lab_form_edite/by_room_and_status",
                params={"lab_name": lab_name, "status": status}
            )
            return response if isinstance(response, list) else []
        except Exception as e:
            print(f"ERROR get_reports_by_room_and_status: {e}")
            return []
    
    def get_all_reports_with_status(self, status: int = 1):
        """
        ดึงข้อมูลรายงานทั้งหมดโดยกรองตาม status เท่านั้น
        Args:
            status: สถานะของรายงาน (1 = แสดง, 0 = ซ่อน), default = 1
            
        Returns:
            list: รายการข้อมูลรายงานทั้งหมดที่มี status ตามที่กำหนด
        """
        try:
            response = self._get(
                "/lab_form_edite/all_by_status",
                params={"status": status}
            )
            # API returns {"data": [...]}
            if isinstance(response, dict) and "data" in response:
                return response["data"] if isinstance(response["data"], list) else []
            return []
        except Exception as e:
            print(f"ERROR get_all_reports_with_status: {e}")
            return []
        
    def delete_report(self, id: int, updater_id: int):
        """
        ลบรายการโดยการเปลี่ยน status เป็น 0 (Soft Delete)
        """
        try:
            response = self._delete(
                "/lab_form_edite/delete",
                params={"report_id": id, "updater_id": updater_id}
            )
            
            if isinstance(response, dict) and response.get("status") == "success":
                return True, response.get("message", "Delete successful")
            else:
                return False, response.get("detail", "Delete failed") if isinstance(response, dict) else "Delete failed"
                
        except Exception as e:
            print(f"ERROR delete_report: {e}")
            return False, str(e)
        
    def save_new_report_version(self, old_report_id: int, new_name: str, new_path: str, lab_name: str, updater: int, comment: str = ""):
        """
        บันทึกการแก้ไขโดย:
        1. เปลี่ยน status ตัวเก่าเป็น 0
        2. เพิ่มรายการใหม่ (Insert) ที่มี status 1
        """
        try:
            payload = {
                "old_report_id": old_report_id,
                "new_name": new_name,
                "new_path": new_path,
                "lab_name": lab_name,
                "updater": updater,
                "comment": comment
            }
            
            response = self._post("/lab_form_edite/save_new_version", json=payload)
            
            if isinstance(response, dict) and response.get("status") == "success":
                return True, response.get("message", "Version update successful")
            else:
                return False, response.get("detail", "Version update failed") if isinstance(response, dict) else "Version update failed"
                
        except Exception as e:
            print(f"ERROR save_new_report_version: {e}")
            return False, str(e)

    def add_report(self, from_name: str, lab_name: str, location_file: str, updater: int, comment: str = ""):
        """
        เพิ่มรายงานใหม่ (INSERT) โดยกำหนด status = 1
        """
        try:
            payload = {
                "from_name": from_name,
                "lab_name": lab_name,
                "location_file": location_file,
                "updater": updater,
                "comment": comment
            }
            
            response = self._post("/lab_form_edite/add", json=payload)
            
            if isinstance(response, dict) and response.get("status") == "success":
                return True, response.get("message", "Add successful")
            else:
                return False, response.get("detail", "Add failed") if isinstance(response, dict) else "Add failed"
                
        except Exception as e:
            print(f"ERROR add_report: {e}")
            return False, str(e)
    
    def upload_file(self, local_file_path: str, lab_name: str, from_name: str):
        """
        อัพโหลดไฟล์ .docx/.doc ไปเก็บที่ Backend
        Returns:
            (True, file_path) ถ้าสำเร็จ
            (False, error_msg) ถ้าล้มเหลว
        """
        try:
            url = f"{self.base_url}/lab_form_edite/upload_file"

            with open(local_file_path, "rb") as f:
                files = {"file": (os.path.basename(local_file_path), f)}
                data = {"lab_name": lab_name, "from_name": from_name}
                response = requests.post(url, files=files, data=data)

            result = response.json()
            if response.status_code == 200 and result.get("status") == "success":
                return True, result.get("file_path", "")
            else:
                return False, result.get("detail", "Upload failed")

        except Exception as e:
            print(f"ERROR upload_file: {e}")
            return False, str(e)

    def download_file(self, relative_path: str, save_path: str):
        """
        ดาวน์โหลดไฟล์จาก Backend ผ่าน API โดยใช้ relative_path ที่เก็บใน database
        Returns:
            (True, save_path) ถ้าสำเร็จ
            (False, error_msg) ถ้าล้มเหลว
        """
        try:
            url = f"{self.base_url}/lab_form_edite/download_file"
            response = requests.get(url, params={"relative_path": relative_path}, stream=True)

            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True, save_path
            else:
                try:
                    detail = response.json().get("detail", "Download failed")
                except Exception:
                    detail = f"HTTP {response.status_code}"
                return False, detail

        except Exception as e:
            print(f"ERROR download_file: {e}")
            return False, str(e)

    def add_lab_name(self, lab_name: str, updater: int):
        """
        บันทึก lab_name ใหม่เข้า database (placeholder row status=2)
        Returns:
            (True, message) ถ้าสำเร็จ
            (False, error_msg) ถ้าล้มเหลว
        """
        try:
            url = f"{self.base_url}/lab_form_edite/add_lab_name"
            response = requests.post(url, data={"lab_name": lab_name, "updater": updater})
            result = response.json()
            if response.status_code == 200 and result.get("status") == "success":
                return True, result.get("message", "Lab name added")
            else:
                return False, result.get("detail", "Add lab name failed")
        except Exception as e:
            print(f"ERROR add_lab_name: {e}")
            return False, str(e)

    def get_all_rooms_list(self):
        """
        ดึงรายการ lab_name ทั้งหมดที่มีอยู่ใน lab_form_edite (status=1)
        
        Returns:
            list: รายการชื่อห้องทั้งหมด (list of strings)
        """
        try:
            response = self._get("/lab_form_edite/get_all_rooms_list")
            # API returns {"data": ["lab_name1", "lab_name2", ...]}
            if isinstance(response, dict) and "data" in response:
                return response["data"] if isinstance(response["data"], list) else []
            return []
        except Exception as e:
            print(f"ERROR get_all_rooms_list: {e}")
            return []