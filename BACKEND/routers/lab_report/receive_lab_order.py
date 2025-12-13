from fastapi import APIRouter, HTTPException
import mariadb
from database import get_db_connection

router = APIRouter(tags=["Receive_lab_order"])

@router.get("/get_lab_order/to_day")
def get_lab_order_to_day(room_id: str, offset: int = 0, limit: int = 50):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("""
                SELECT 
                    sample_registration.dtime,
                    lab_order.id AS lab_order_id,
                    sample_registration.speed,
                    sample_registration.sample_inspection
                FROM lab_order
                INNER JOIN sample_registration 
                    ON lab_order.sample_id = sample_registration.id
                WHERE lab_order.room_id = ? AND lab_order.status = 1
                ORDER BY lab_order.id DESC 
                LIMIT ? OFFSET ?
                """, (room_id, limit, offset))
        groups = [{"time": row[0], "lab_order_id": row[1], "speed": row[2], "sample_inspection": row[3]} for row in cursor]
        
        cursor.execute("SELECT COUNT(*) FROM lab_order WHERE room_id = ? AND status = 1", (room_id,))
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