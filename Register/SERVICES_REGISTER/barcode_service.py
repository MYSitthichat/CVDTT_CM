from .base_service import BaseService

class BarcodeService(BaseService):
    def get_today_cases(self, offset=0, limit=100):
        """ดึงข้อมูล Case ที่ลงทะเบียนวันนี้ พร้อม Pagination"""
        params = {"offset": offset, "limit": limit}
        result = self._get("/barcode/today", params=params)
        return result if result is not None else []

    def search_barcode_cases(self, name, surname, offset=0, limit=100):
        """ค้นหา Case จากชื่อ-นามสกุลลูกค้า พร้อม Pagination"""
        params = {"name": name, "surname": surname, "offset": offset, "limit": limit}
        result = self._get("/barcode/search", params=params)
        return result if result is not None else []

    def search_barcode_by_employee(self, employee_id, offset=0, limit=100):
        """ค้นหา Case จากรหัสพนักงาน (ผู้บันทึก) พร้อม Pagination"""
        params = {"employee_id": employee_id, "offset": offset, "limit": limit}
        result = self._get("/barcode/search_by_employee", params=params)
        return result if result is not None else []