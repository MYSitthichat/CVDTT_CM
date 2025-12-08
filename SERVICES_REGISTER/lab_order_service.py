from .base_service import BaseService

class LabOrderService(BaseService):
    def search_by_barcode(self, barcode):
        """ค้นหารายการตาม barcode"""
        return self._get(f"/search_lab_order_by_barcode/{barcode}")
    
    def search_today_orders(self):
        """ค้นหารายการในวันนี้"""
        return self._get("/search_today_lab_orders")
    
    def get_lab_order_details(self, order_id):
        """ดึงรายละเอียดของ lab order"""
        return self._get(f"/get_lab_order_details/{order_id}")