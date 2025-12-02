import sys
import requests
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                               QLineEdit, QLabel, QCompleter, QMessageBox, QFrame, QFormLayout)
from PySide6.QtCore import QStringListModel, Qt, QTimer


API_URL = "http://127.0.0.1:8000" 

class APIApp(QWidget):
    def __init__(self):
        super().__init__()

    def fetch_search_results(self, command):
        text = command.strip()
        try:
            response = requests.get(f"{API_URL}/search", params={"q": text}, timeout=2)
            if response.status_code == 200:
                data = response.json()
                # print(f"API returned {len(data)} results for '{text}'")
                return data
            else:
                print(f"Server Error: {response.status_code}")
                return []
        except requests.Timeout:
            print(f"API Timeout Error for query: {text}")
            return []
        except Exception as e:
            print(f"API Connect Error: {e}")
            return []

    def get_status_login(self, username, password):
        params = {
            "username": username,
            "password": password
        }
        try:
            response = requests.post(f"{API_URL}/login", params=params, timeout=10)
            try:
                data = response.json()
            except ValueError:
                return None
            if response.status_code == 200:
                if isinstance(data, dict):
                    if data.get("success"):
                        return {"id": data.get("user_id"), "user_id": data.get("user_id")}
                    else:
                        return None
                elif isinstance(data, bool):
                    return {"id": None} if data else None
                return None
            else:
                return None
                
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None

    def check_email(self, email):
        try:
            response = requests.post(
                f"{API_URL}/check_email", 
                params={"email": email},
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                return False
                
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return False

    def update_password(self, email, new_password):
        try:
            response = requests.post(
                f"{API_URL}/update_password",
                params={"email": email, "new_password": new_password},
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                return False
                
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return False

# ADD NEW CUSTOMER API

    def add_new_customer(self, customer_data):
        try:
            response = requests.post(
                f"{API_URL}/add_customer",
                json=customer_data,
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                return False
                
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return False
        
    def get_customer_group_id(self):
        
        try:
            response = requests.get(f"{API_URL}/get_customer_group_id", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Server Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"API Connect Error: {e}")
            return []
        
# ADD NEW CUSTOMER API

# ADD NEW WORK API

    def get_max_sample_id(self):
        try:
            response = requests.get(f"{API_URL}/get_max_sample_id", timeout=5)
            if response.status_code == 200:
                data = response.json()
                # print(data)
                return data.get("max_id") # คืนค่า max_id ที่ได้จาก JSON
            else:
                print(f"Server Error on get_max_sample_id: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"API Connect Error on get_max_sample_id: {e}")
            return None

    def add_new_work(self, sender_id, owner_id, project_name, updater):
        """Add new work/case registration"""
        try:
            # Ensure project_name is not None
            if project_name is None:
                project_name = ""
            
            params = {
                "sender_id": sender_id,
                "owner_id": owner_id,
                "project_name": project_name,
                "updater": updater
            }
            
            response = requests.post(
                f"{API_URL}/add_new_work",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                error_text = response.text
                print(f"❌ API Error {response.status_code}: {error_text}")
                return {"status": "error", "detail": f"HTTP {response.status_code}: {error_text}"}
                
        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            return {"status": "error", "detail": f"Network error: {str(e)}"}

    def add_sample_registration(self, sample_data):
        try:
            response = requests.post(
                f"{API_URL}/add_new_specimen",
                json=sample_data,
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                return {"status": "error", "detail": response.text}
                
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return {"status": "error", "detail": str(e)}

    def get_room_details(self):
        try:
            response = requests.get(f"{API_URL}/get_room_details", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Server Error on get_room_details: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"API Connect Error on get_room_details: {e}")
            return None

# ADD NEW WORK API

# --- ADD NEW LAB ORDER API ---

    def add_new_lab_order(self, order_data):
        try:
            response = requests.post(f"{API_URL}/add_new_lab_order",json=order_data,timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                return {"status": "error", "detail": response.text}
                
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return {"status": "error", "detail": str(e)}

# --- ADD NEW LAB ORDER API ---

# --- UPDATE TRACKING LAB ORDER API ---

    def update_tracking_lab_order(self, order_data):
        try:
            response = requests.post(f"{API_URL}/update_tracking_lab_order",json=order_data,timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                return {"status": "error", "detail": response.text}
                
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return {"status": "error", "detail": str(e)}

# --- UPDATE TRACKING LAB ORDER API ---

# --- UPDATE CASE DETAILS API ---

    def get_case_details(self, case_id):
        """Get case details by case ID"""
        try:
            response = requests.get(f"{API_URL}/get_case_details/{case_id}", timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                return {"status": "error", "detail": response.text}

        except requests.RequestException as e:
            print(f"Network error: {e}")
            return {"status": "error", "detail": str(e)}

# --- UPDATE CASE DETAILS API ---

# --- MOLECULAR BIOLOGY API ---

    def save_molecular_biology(self, molecular_data):
        """
        Save molecular biology test data
        
        Args:
            molecular_data: dict with keys:
                - sample_id: str
                - tests: list of dicts with 'name', 'quantity', 'total_price'
                - cPCR_req: int (optional)
                - qPCR_req: int (optional)
                - extraction_req: int (optional)
                - updater: str (username)
        
        Returns:
            dict with status and message, or None on error
        """
        try:
            response = requests.post(
                f"{API_URL}/save_molecular_biology",
                json=molecular_data,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Server Error: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"Error detail: {error_detail}")
                except:
                    pass
                return None
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None

# --- MOLECULAR BIOLOGY API ---

# EMPLOYEE MANAGEMENT API

    def get_max_sample_id(self):
        try:
            response = requests.get(f"{API_URL}/get_max_sample_id", timeout=5)
            if response.status_code == 200:
                data = response.json()
                # print(data)
                return data.get("max_id") # คืนค่า max_id ที่ได้จาก JSON
            else:
                print(f"Server Error on get_max_sample_id: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"API Connect Error on get_max_sample_id: {e}")
            return None

# EMPLOYEE MANAGEMENT API

    def search_employee(self, search_text):
        """Search employee by name or surname"""
        try:
            response = requests.get(
                f"{API_URL}/search_employee",
                params={"q": search_text},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("employees", [])
            else:
                print(f"Server Error: {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return []

    def get_employee_by_id(self, employee_id):
        """Get employee details by ID"""
        try:
            response = requests.get(
                f"{API_URL}/get_employee/{employee_id}",
                timeout=10
            )
            if response.status_code == 200:
                # print(response.json())
                return response.json()
            else:
                return None
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None

    def create_employee(self, employee_data):
        """Create new employee"""
        try:
            response = requests.post(
                f"{API_URL}/create_employee",
                json=employee_data,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None

    def update_employee(self, employee_id, employee_data):
        """Update employee data"""
        try:
            response = requests.put(
                f"{API_URL}/update_employee/{employee_id}",
                json=employee_data,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None

    def delete_employee(self, employee_id):
        """Delete employee"""
        try:
            response = requests.delete(
                f"{API_URL}/delete_employee/{employee_id}",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None

    def get_employee_groups(self):
        """Get all employee groups/positions"""
        try:
            response = requests.get(
                f"{API_URL}/get_employee_groups",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                # print(data)
                return data.get("employee_groups", [])
            else:
                print(f"Server Error: {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return []

    def get_signature(self, username):
        """Get signature image for username as base64"""
        try:
            response = requests.get(
                f"{API_URL}/get_signature/{username}",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("signature_base64")
            else:
                return None
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None


