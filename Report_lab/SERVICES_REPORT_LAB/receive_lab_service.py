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
        """ดึงรายการ report templates จาก API"""
        try:
            params = {}
            if room_id is not None:
                params['room_id'] = room_id
            
            result = self._get("/get_report_templates", params=params)
            
            if result and result.get('success', False):
                return result.get('templates', [])
            else:
                print(f"Error getting report templates: {result}")
                return []
                
        except Exception as e:
            print(f"Error getting report templates: {e}")
            return []
    
    def get_template_data(self, lab_order_id: int):
        """ดึงข้อมูลสำหรับเติมลงใน template ผ่าน API"""
        try:
            params = {"lab_order_id": lab_order_id}
            result = self._get("/get_template_data", params=params)
            
            if result and result.get('success', False):
                return result.get('data', {})
            else:
                print(f"Error getting template data: {result}")
                return None
                
        except Exception as e:
            print(f"Error getting template data: {e}")
            return None
    
    def export_word_template(self, lab_order_id: int, template_path: str, template_name: str, output_filename: str):
        """Export Word template ผ่าน API และดาวน์โหลดไฟล์"""
        try:
            data = {
                "lab_order_id": lab_order_id,
                "template_path": template_path,
                "template_name": template_name,
                "output_filename": output_filename
            }
            
            import requests
            url = f"{self.base_url}/export_word_template"
            response = requests.post(url, json=data, timeout=30)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "content": response.content,  # ไฟล์ Word ที่ได้
                    "filename": output_filename
                }
            else:
                error_msg = f"Server Error: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail.get('detail', response.text)}"
                except:
                    error_msg += f" - {response.text}"
                print(error_msg)
                return {"success": False, "message": error_msg}
                
        except Exception as e:
            print(f"Error exporting template: {e}")
            return {"success": False, "message": str(e)}
