from .base_service import BaseService

class SearchRoomService(BaseService):
    def search_room(self, parameter: str = None):
        data = self._get("/lab_report/rooms", params={"search_keyword": parameter})
        if data and "rooms" in data and len(data["rooms"]) > 0:
            return data["rooms"][0].get("id")
        return None