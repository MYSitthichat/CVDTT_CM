from .base_service import BaseService

class EmployeeService(BaseService):
    def search_employee(self, query, current_username=None):
        params = {"q": query}
        if current_username:
            params["current_username"] = current_username
        data = self._get("/search_employee", params=params)
        return data.get("employees", []) if data else []

    def get_employee_by_id(self, emp_id, include_archived=False):
        params = {"include_archived": include_archived}
        return self._get(f"/get_employee/{emp_id}", params=params)

    def get_permission(self, emp_id):
        data = self._get(f"/get_employee_permission/{emp_id}")
        return data.get("group_id") if data else None

    def create_employee(self, data):
        return self._post("/create_employee", json=data)

    def update_employee(self, emp_id, data):
        return self._put(f"/update_employee/{emp_id}", json=data)

    def delete_employee(self, emp_id, updater_id):
        return self._delete(f"/delete_employee/{emp_id}", params={"updater": updater_id})

    def get_groups(self):
        data = self._get("/get_employee_groups")
        return data.get("employee_groups", []) if data else []

    def get_signature(self, username):
        data = self._get(f"/get_signature/{username}")
        return data.get("signature_base64") if data else None