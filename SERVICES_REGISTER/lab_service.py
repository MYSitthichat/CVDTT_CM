from .base_service import BaseService

class LabService(BaseService):
    def get_room_details(self):
        return self._get("/get_room_details")

    def add_new_lab_order(self, order_data):
        return self._post("/add_new_lab_order", json=order_data)

    def update_tracking_lab_order(self, tracking_data):
        return self._post("/update_tracking_lab_order", json=tracking_data)

    def get_case_details(self, case_id):
        return self._get(f"/get_case_details/{case_id}")

    # --- Save Test Results ---
    def save_molecular_biology(self, data):
        return self._post("/save_molecular_biology", json=data)

    def save_parasite_biology(self, data):
        return self._post("/save_parasite_biology", json=data)

    def save_bacteria_biology(self, data):
        return self._post("/save_bacteria_biology", json=data)

    # --- Progress ---
    def get_job_progress(self, offset=0, limit=100):
        return self._get("/get_job_progress", params={"offset": offset, "limit": limit})