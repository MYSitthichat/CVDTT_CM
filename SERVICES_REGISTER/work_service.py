from .base_service import BaseService

class WorkService(BaseService):
    def get_max_sample_id(self):
        data = self._get("/get_max_sample_id")
        return data.get("max_id") if data else 0

    def add_new_work(self, sender_id, owner_id, project_name, updater):
        params = {
            "sender_id": sender_id,
            "owner_id": owner_id,
            "project_name": project_name if project_name else "",
            "updater": updater
        }
        return self._post("/add_new_work", params=params)

    def add_specimen(self, specimen_data):
        return self._post("/add_new_specimen", json=specimen_data)
    
    def get_case_details(self, case_id):
        return self._get(f"/get_case_details/{case_id}")
    
    def delete_sample_registration(self, order_id):
        return self._get(f"/delete_sample_registration/{order_id}")
    
    def get_lab_order_pdf_data(self, order_id):
        """Get lab order data for PDF generation"""
        return self._get(f"/get_lab_order_pdf_data/{order_id}")
    
    def change_state_work(self, work_id, new_state):
        """Change work state (1=printed sticker, 2=printed lab form)"""
        params = {
            "work_id": work_id,
            "new_state": str(new_state)
        }
        return self._post("/change_state_work", params=params)