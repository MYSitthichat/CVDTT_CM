from .base_service import BaseService

class CustomerService(BaseService):
    def search_customer(self, query):
        if not query: return []
        return self._get("/search", params={"q": query.strip()})

    def add_new_customer(self, customer_data):
        return self._post("/add_customer", json=customer_data)

    def get_customer_groups(self):
        data = self._get("/get_customer_group_id")
        return data if data else {}

    def fetch_search_results(self, query):
        return self._get("/customer/search", params={"q": query.strip()})