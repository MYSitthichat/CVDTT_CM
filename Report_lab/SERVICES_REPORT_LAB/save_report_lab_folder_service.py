from .base_service import BaseService
import requests

class SaveReportLabFolderService(BaseService):
    def initialize_lab_report_folders(self):
        try:
            result = self._get("/initialize_lab_folders")
        except Exception as e:
            result = {
                "status": "ERROR",
                "message": "Server encountered an error while initializing folders.",
                "error_detail": str(e)
            }
        return result if result is not None else None


    def save_report_files(self, lab_name, barcode, lab_id, case_id, room_id, updater, date_str, word_path, pdf_path):
        """ ส่งไฟล์และข้อมูลลง Database """
        try:
            api_url = "http://202.28.24.55:8000/save_report_files" 
            
            # เตรียม Data (ตัด sample_id ออกตามที่คุณต้องการ)
            payload = {
                "lab_name": lab_name,
                "barcode": barcode,
                "lab_id": str(lab_id),     # lab_order_id
                "case_id": str(case_id),   # case_id
                "room_id": str(room_id),   # send_from_room
                "updater": str(updater),   # user_id
                "date_str": date_str
            }

            files_dict = {
                'file_word': open(word_path, 'rb'),
                'file_pdf': open(pdf_path, 'rb')
            }

            # ยิง Request
            response = requests.post(api_url, data=payload, files=files_dict, timeout=30)
            
            # ปิดไฟล์
            files_dict['file_word'].close()
            files_dict['file_pdf'].close()

            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "error", "message": f"Server Error: {response.text}"}

        except Exception as e:
            return {"status": "error", "message": str(e)}