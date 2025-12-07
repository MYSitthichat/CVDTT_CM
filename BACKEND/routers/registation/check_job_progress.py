from fastapi import APIRouter, HTTPException
import mariadb
from database import get_db_connection

router = APIRouter(tags=["Authentication"])

@router.get("/get_job_progress")
def get_job_progress(offset: int = 0, limit: int = 100):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("""
                SELECT 
                t.lab_order_id, 
                t.tracking_info, 
                t.receiver,
                CONCAT(IFNULL(e.title, ''), IFNULL(e.name, ''), ' ', IFNULL(e.surname, '')) AS receiver_name,
                t.dtime
                FROM tracking_lab_order t
                LEFT JOIN employee e ON t.receiver = e.id
                WHERE t.status = 1 
                ORDER BY t.dtime DESC
                LIMIT %s OFFSET %s
                """, (limit, offset))
        groups = [{"id": row[0], "tracking_info": row[1], "receiver": row[2], "receiver_name": row[3], "dtime": str(row[4]) if row[4] else ""} for row in cursor]
        cursor.execute("SELECT COUNT(*) FROM tracking_lab_order WHERE status = 1")
        total_count = cursor.fetchone()[0]
        
        return {
            "job_progress": groups,
            "total": total_count,
            "offset": offset,
            "limit": limit,
            "has_more": (offset + limit) < total_count
        }
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve job progress")
    finally:
        conn.close()