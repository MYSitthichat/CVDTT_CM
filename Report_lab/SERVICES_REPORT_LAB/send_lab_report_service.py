from .base_service import BaseService

class SendLabService(BaseService):
    def get_received_labs_to_day(self, room_id: str, offset=0, limit=50):
        """ดึงข้อมูล lab ที่รับแล้วจาก table lab_receive_detail"""
        params = {"room_id": room_id, "offset": offset, "limit": limit}
        result = self._get("/get_received_labs/to_day", params=params)
        return result if result is not None else None
    
    def get_received_labs_by_barcode(self, barcode: str, room_id: str = ""):
        """ค้นหา lab ที่รับแล้วด้วย barcode พร้อม room_id access control"""
        params = {"barcode": barcode, "room_id": room_id}
        result = self._get("/get_received_labs/barcode", params=params)
        return result if result is not None else None
    
    def get_lab_order_details(self, lab_order_id: str, room_id: str):
        """ดึงรายละเอียดของ Lab Order สำหรับแสดงใน Dialog"""
        params = {"lab_order_id": lab_order_id, "room_id": room_id}
        result = self._get("/get_lab_order/details", params=params)
        return result if result is not None else None