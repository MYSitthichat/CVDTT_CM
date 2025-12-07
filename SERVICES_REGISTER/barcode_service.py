from .base_service import BaseService

class BarcodeService(BaseService):
    def get_today_cases(self):
        """ดึงข้อมูล Case ที่ลงทะเบียนวันนี้"""
        result = self._get("/barcode/today")
        return result if result is not None else []

    def search_barcode_cases(self, name, surname):
        """ค้นหา Case จากชื่อ-นามสกุลลูกค้า"""
        params = {"name": name, "surname": surname}
        result = self._get("/barcode/search", params=params)
        return result if result is not None else []

    def search_barcode_by_employee(self, employee_id):
        """ค้นหา Case จากรหัสพนักงาน (ผู้บันทึก)"""
        params = {"employee_id": employee_id}
        result = self._get("/barcode/search_by_employee", params=params)
        return result if result is not None else []