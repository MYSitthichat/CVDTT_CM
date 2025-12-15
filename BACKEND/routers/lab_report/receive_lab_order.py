from fastapi import APIRouter, HTTPException
import mariadb
from database import get_db_connection

router = APIRouter(tags=["Receive_lab_order"])


@router.get("/get_lab_order/detail")
def get_lab_order_detail(lab_order_id: str, room_id: str = ""):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        if room_id:
            query = """
                SELECT 
                    lab_order.id AS lab_order_id,
                    sample_registration.dtime,
                    sample_registration.speed,
                    sample_registration.sample_inspection,
                    sample_registration.id AS sample_id,
                    lab_order.room_id
                FROM lab_order
                INNER JOIN sample_registration
                    ON lab_order.sample_id = sample_registration.id
                WHERE lab_order.id = ? AND 
                lab_order.room_id = ? AND lab_order.status = 1
                """
            cursor.execute(query, (lab_order_id, room_id))
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve lab order detail")
    finally:
        conn.close()




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

@router.get("/get_lab_order/barcode")
def get_lab_order_by_barcode(barcode: str, room_id: str = ""):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        
        # Convert barcode to lab_order_id (remove leading zeros)
        try:
            lab_order_id = int(barcode)
        except ValueError:
            return {
                "job_progress": [],
                "total": 0,
                "found": False,
                "message": "Barcode ไม่ถูกต้อง"
            }
        
        # Build query with room_id filter if provided
        if room_id:
            query = """
                SELECT 
                    sample_registration.dtime,
                    lab_order.id AS lab_order_id,
                    sample_registration.speed,
                    sample_registration.sample_inspection,
                    sample_registration.id AS sample_id,
                    lab_order.room_id
                FROM lab_order
                INNER JOIN sample_registration 
                    ON lab_order.sample_id = sample_registration.id
                WHERE lab_order.id = ? 
                    AND lab_order.room_id = ? 
                    AND lab_order.status = 1
                ORDER BY lab_order.id DESC 
                """
            cursor.execute(query, (lab_order_id, room_id))
        else:
            # Admin mode - no room restriction
            query = """
                SELECT 
                    sample_registration.dtime,
                    lab_order.id AS lab_order_id,
                    sample_registration.speed,
                    sample_registration.sample_inspection,
                    sample_registration.id AS sample_id,
                    lab_order.room_id
                FROM lab_order
                INNER JOIN sample_registration 
                    ON lab_order.sample_id = sample_registration.id
                WHERE lab_order.id = ? AND lab_order.status = 1
                ORDER BY lab_order.id DESC 
                """
            cursor.execute(query, (lab_order_id,))
        
        results = cursor.fetchall()
        
        if not results:
            if room_id:
                return {
                    "job_progress": [],
                    "total": 0,
                    "found": False,
                    "message": "ไม่พบข้อมูล Barcode นี้ในห้องของคุณ หรือไม่มีสิทธิ์เข้าถึง"
                }
            else:
                return {
                    "job_progress": [],
                    "total": 0,
                    "found": False,
                    "message": "ไม่พบข้อมูล Barcode นี้"
                }
        
        groups = [{
            "time": row[0], 
            "lab_order_id": row[1], 
            "speed": row[2], 
            "sample_inspection": row[3],
            "sample_id": row[4],
            "room_id": row[5]
        } for row in results]
        
        return {
            "job_progress": groups,
            "total": len(groups),
            "found": True,
            "message": f"พบข้อมูล {len(groups)} รายการ"
        }
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to search by barcode")
    finally:
        conn.close()

@router.get("/get_lab_order/details")
def get_lab_order_details(lab_order_id: str, room_id: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # แปลง lab_order_id เป็น int
        try:
            order_id = int(lab_order_id)
        except ValueError:
            return {
                "success": False,
                "message": "Lab Order ID ไม่ถูกต้อง"
            }
        
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve lab order details")