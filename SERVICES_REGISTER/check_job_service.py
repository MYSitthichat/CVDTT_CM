from .base_service import BaseService

class CheckJobService(BaseService):

    def get_job_progress(self, offset=0, limit=100):
        """ดึงข้อมูลความคืบหน้างานในระบบ พร้อม Pagination"""
        params = {"offset": offset, "limit": limit}
        result = self._get("/get_job_progress", params=params)
        return result if result is not None else None