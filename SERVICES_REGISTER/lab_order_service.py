from .base_service import BaseService

class LabOrderService(BaseService):
    def search_by_barcode(self, barcode, offset=0, limit=100):
        """ค้นหารายการตาม barcode พร้อม Pagination"""
        params = {"offset": offset, "limit": limit}
        return self._get(f"/search_lab_order_by_barcode/{barcode}", params=params)
    
    def search_today_orders(self, offset=0, limit=100):
        """ค้นหารายการในวันนี้ พร้อม Pagination"""
        params = {"offset": offset, "limit": limit}
        return self._get("/search_today_lab_orders", params=params)
    
    def get_lab_order_details(self, order_id):
        """ดึงรายละเอียดของ lab order"""
        return self._get(f"/get_lab_order_details/{order_id}")