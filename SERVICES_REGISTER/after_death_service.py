import requests
from .base_service import BaseService

class AfterDeathService(BaseService):
    """Service for After Death operations"""
    
    def save_after_death(self, sample_id: str, service_type: str, service_data: dict, user_id: int):
        """
        Save after death service data
        
        Args:
            sample_id: Sample identifier
            service_type: Type of service (Infectious Waste/Cremation/Jewelry)
            service_data: Dictionary containing service details
            user_id: Current user ID
            
        Returns:
            bool: True if successful
        """
        try:
            payload = {
                "sample_id": sample_id,
                "service_type": service_type,
                "service_data": service_data,
                "updater": user_id
            }
            
            response = self._post("/after_death/save_after_death", json=payload)
            
            if response:
                return True
            else:
                print(f"Error saving after death data: {response}")
                return False
                
        except Exception as e:
            print(f"Exception in save_after_death: {e}")
            return False
    
    def get_after_death(self, sample_id: str):
        """
        Get after death service data by sample ID
        
        Args:
            sample_id: Sample identifier
            
        Returns:
            dict: Service data or None
        """
        try:
            response = self._get(f"/after_death/get_after_death/{sample_id}")
            return response
                
        except Exception as e:
            print(f"Exception in get_after_death: {e}")
            return None