from .base_service import BaseService


class ReportFormService(BaseService):
    """Service for managing report_form table data"""
    
    def get_latest_id(self):
        """ดึง ID ล่าสุดจาก report_form เพื่อสร้างเลขที่รายงาน"""
        try:
            result = self._get("/report_form/latest_id")
            if isinstance(result, dict) and result.get("status") == "success":
                return result
            else:
                return {"status": "error", "current_max_id": 0, "next_id": 1}
        except Exception as e:
            print(f"ERROR getting latest report form id: {e}")
            return {"status": "error", "current_max_id": 0, "next_id": 1}
    
    def get_by_lab_order(self, lab_order_id: int):
        """ดึงข้อมูล report_form จาก lab_order_id"""
        try:
            result = self._get(f"/report_form/by_lab_order/{lab_order_id}")
            if isinstance(result, dict) and result.get("status") == "success":
                return result.get("data", [])
            else:
                return []
        except Exception as e:
            print(f"ERROR getting report form by lab_order: {e}")
            return []
    
    def create_report_form(self, lab_order_id: int, location: str = "", comment: str = "", 
                          state: int = 0, status: int = 1, recorder: int = 0, approver: int = 0, room_id: int = 0):
        """สร้าง report_form ใหม่"""
        try:
            data = {
                "lab_order_id": lab_order_id,
                "location": location,
                "comment": comment,
                "state": state,
                "status": status,
                "recorder": recorder,
                "approver": approver,
                "room_id": room_id
            }
            result = self._post("/report_form/create", json=data)
            if isinstance(result, dict) and result.get("status") == "success":
                return True, result.get("id"), result.get("message", "Success")
            else:
                return False, None, result.get("detail", "Failed to create report form")
        except Exception as e:
            print(f"ERROR creating report form: {e}")
            return False, None, str(e)
    
    def update_report_form(self, report_id: int, location: str = None, comment: str = None,
                          state: int = None, status: int = None, recorder: int = None, approver: int = None):
        """อัพเดท report_form"""
        try:
            data = {
                "id": report_id,
                "location": location,
                "comment": comment,
                "state": state,
                "status": status,
                "recorder": recorder,
                "approver": approver
            }
            # Remove None values
            data = {k: v for k, v in data.items() if v is not None}
            
            result = self._put("/report_form/update", json=data)
            if isinstance(result, dict) and result.get("status") == "success":
                return True, result.get("message", "Success")
            else:
                return False, result.get("detail", "Failed to update report form")
        except Exception as e:
            print(f"ERROR updating report form: {e}")
            return False, str(e)
    
    def get_lab_order_details(self, lab_order_id: int):
        """ดึงข้อมูล lab_order พร้อม case_registration details"""
        try:
            result = self._get(f"/report_form/lab_order_details/{lab_order_id}")
            # DEBUG: Uncomment for debugging
            # print(f"DEBUG get_lab_order_details API Response: {result}")
            if isinstance(result, dict) and result.get("status") == "success":
                return result.get("data", None)
            else:
                # DEBUG: Uncomment for debugging
                # print(f"ERROR: API returned unexpected response: {result}")
                return None
        except Exception as e:
            # DEBUG: Uncomment for debugging
            # print(f"ERROR getting lab order details: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_lab_order_with_tests(self, lab_order_id: int):
        """ดึงข้อมูล lab_order พร้อมรายการทดสอบ (สำหรับ room_id 8 = Molecular Biology)"""
        try:
            # ใช้ endpoint ที่ต้องการ room_id parameter
            result = self._get(f"/get_lab_order/details?lab_order_id={lab_order_id}&room_id=8")
            if isinstance(result, dict) and result.get("success"):
                return result
            else:
                print(f"ERROR: API returned unexpected response: {result}")
                return None
        except Exception as e:
            # DEBUG: Uncomment for debugging
            print(f"ERROR getting lab order with tests: {e}")
            import traceback
            traceback.print_exc()
            return None
