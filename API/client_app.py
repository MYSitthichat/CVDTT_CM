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


# ADD BARCODE  API

    def get_today_cases(self):
        try:
            response = requests.get(f"{API_URL}/barcode/today", timeout=5)
            if response.status_code == 200:
                return response.json() # Important: Return the JSON object
            else:
                print(f"Server Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"API Error: {e}")
            return []

    def search_barcode_cases(self, name, surname):
        try:
            params = {"name": name, "surname": surname}
            response = requests.get(f"{API_URL}/barcode/search", params=params, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Server Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"API Error: {e}")
            return []
