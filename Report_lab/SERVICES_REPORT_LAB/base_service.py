import requests

# ตั้งค่า IP Server ที่นี่
# API_URL = "http://202.28.24.55:8000" Production

API_URL = "http://127.0.0.1:8000" # Development

class BaseService:
    def __init__(self):
        self.base_url = API_URL
        self.timeout = 10

    def _post(self, endpoint, json=None, params=None):
        """ส่งข้อมูลแบบ POST"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.post(url, json=json, params=params, timeout=self.timeout)
            if response.status_code == 200:
                try:
                    return response.json()
                except ValueError:
                    return response.text
            else:
                error_msg = f"Server Error ({endpoint}): {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail.get('detail', response.text)}"
                except:
                    error_msg += f" - {response.text}"
                print(error_msg)
                return {"status": "error", "detail": error_msg}
        except requests.RequestException as e:
            print(f"Network Error ({endpoint}): {e}")
            return {"status": "error", "detail": str(e)}

    def _get(self, endpoint, params=None):
        """ดึงข้อมูลแบบ GET"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            else:
                return [] if "search" in endpoint else None
        except requests.RequestException as e:
            print(f"Network Error ({endpoint}): {e}")
            return [] if "search" in endpoint else None

    def _put(self, endpoint, json=None):
        """อัปเดตข้อมูลแบบ PUT"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.put(url, json=json, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                # print(f"Server Error ({endpoint}): {response.status_code}")
                return {"status": "error", "detail": response.text}
        except requests.RequestException as e:
            return {"status": "error", "detail": str(e)}

    def _delete(self, endpoint, params=None):
        """ลบข้อมูลแบบ DELETE"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.delete(url, params=params, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "error", "detail": response.text}
        except requests.RequestException as e:
            return {"status": "error", "detail": str(e)}