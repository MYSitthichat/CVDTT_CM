from .base_service import BaseService
import requests
import os

class DoctorReportService(BaseService):
    """Service สำหรับจัดการรายงานที่รอการตรวจสอบจากแพทย์"""
    
    def get_pending_reports(self, room_id: str = ""):
        """ดึงรายการรายงานที่รอการตรวจสอบ (approver = 0)"""
        params = {}
        if room_id:
            params["room_id"] = room_id
        
        result = self._get("/doctor_report/pending_reports", params=params)
        return result if result is not None else {"data": [], "count": 0}
    
    def get_report_by_id(self, report_id: int):
        """ดึงรายละเอียดรายงานตาม ID"""
        params = {"report_id": report_id}
        result = self._get("/doctor_report/report_by_id", params=params)
        return result if result is not None else None
    
    def download_report_file(self, report_id: int, save_path: str):
        """ดาวน์โหลดไฟล์รายงาน Word และบันทึกลงโฟลเดอร์"""
        try:
            url = f"{self.base_url}/doctor_report/report_file/{report_id}"
            # print(f"DEBUG: Downloading from {url}")
            
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # สร้างโฟลเดอร์ถ้ายังไม่มี
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # บันทึกไฟล์
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # print(f"✓ Downloaded file to: {save_path}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error downloading file: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False
