from .base_service import BaseService

class AuthService(BaseService):
    def login(self, username, password):
        params = {"username": username, "password": password}
        # หมายเหตุ: endpoint ต้องตรงกับ backend routers/auth.py
        data = self._post("/login", params=params)
        
        if data and isinstance(data, dict):
            if data.get("success"):
                return {
                    "id": data.get("user_id"), 
                    "user_id": data.get("user_id"),
                    "group_id": data.get("group_id")
                }
        return None

    def check_email(self, email):
        result = self._post("/check_email", params={"email": email})
        # แปลง string "true"/"false" หรือ boolean ให้ถูกต้อง
        if result is True or str(result).lower() == 'true':
            return True
        return False

    def update_password(self, email, new_password):
        result = self._post("/update_password", params={"email": email, "new_password": new_password})
        if result is True or str(result).lower() == 'true':
            return True
        return False