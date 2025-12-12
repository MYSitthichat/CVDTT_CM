from .base_service import BaseService

class CustomerService(BaseService):
    def search_customer(self, query):
        """Search for customers by name, surname, or tax_id"""
        if not query: 
            return []
        return self._get("/search", params={"q": query.strip()})

    def add_new_customer(self, customer_data):
        """Add a new customer to the database"""
        return self._post("/add_customer", json=customer_data)

    def get_customer_groups(self):
        """Get all customer groups"""
        data = self._get("/get_customer_group_id")
        return data if data else {}