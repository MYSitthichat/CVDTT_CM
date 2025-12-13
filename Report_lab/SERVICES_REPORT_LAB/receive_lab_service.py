from .base_service import BaseService

class ReceiveLabService(BaseService):
    def get_lab_order_to_day(self, room_id: str, offset=0, limit=50):
        params = {"room_id": room_id, "offset": offset, "limit": limit}
        result = self._get("/get_lab_order/to_day", params=params)
        return result if result is not None else None
