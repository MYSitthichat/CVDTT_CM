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
