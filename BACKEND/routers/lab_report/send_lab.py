from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import mariadb
from database import get_db_connection

router = APIRouter(tags=["Send_lab"])



@router.get("/get_detail/lab_order")
def get_lab_order_detail(lab_order_id: int):
    conn = get_db_connection()
    print(f"Fetching details for Lab Order ID: {lab_order_id}")
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        sql = """
            SELECT 
                lab_receive_detail.case_id, 
                lab_receive_detail.lab_order_id, 
                room_information.name AS room_name
            FROM lab_receive_detail
            LEFT JOIN room_information 
                ON lab_receive_detail.receive_from_room = room_information.id
            WHERE lab_receive_detail.room_action_status = 1 
            AND lab_receive_detail.lab_order_id = ?
        """
        cursor.execute(sql, (lab_order_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Lab order not found")
        case_id, lab_order_id, room_name = result
        return {
            "case_id": case_id,
            "lab_order_id": lab_order_id,
            "room_name": room_name
        }
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve lab order details")


@router.get("/get_received_labs/to_day")
def get_received_labs_to_day(room_id: str, offset: int = 0, limit: int = 50):
    """
    ดึงข้อมูล lab ที่รับแล้วจาก table lab_receive_detail
    โดยกรองตาม room_id ของเจ้าหน้าที่และแสดงเฉพาะที่ room_action_status = 1 (รับแลป)
    ถ้า room_id="" (admin) จะดึงข้อมูลจากทุกห้อง
    """
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        
        # สร้าง query ตาม room_id
        if room_id == "":
            # Admin mode - ดูข้อมูลทุกห้อง
            cursor.execute("""
                SELECT 
                    lrd.dtime,
                    lrd.lab_order_id,
                    sr.speed,
                    sr.sample_inspection
                FROM lab_receive_detail lrd
                INNER JOIN lab_order lo ON lrd.lab_order_id = lo.id
                INNER JOIN sample_registration sr ON lo.sample_id = sr.id
                WHERE lrd.room_action_status = 1 AND lrd.send_success = 0
                    AND lo.status = 1
                ORDER BY lrd.id DESC 
                LIMIT ? OFFSET ?
            """, (limit, offset))
        else:
            # User mode - ดูเฉพาะห้องของตัวเอง
            cursor.execute("""
                SELECT 
                    lrd.dtime,
                    lrd.lab_order_id,
                    sr.speed,
                    sr.sample_inspection
                FROM lab_receive_detail lrd
                INNER JOIN lab_order lo ON lrd.lab_order_id = lo.id
                INNER JOIN sample_registration sr ON lo.sample_id = sr.id
                WHERE lrd.receive_from_room = ? 
                    AND lrd.room_action_status = 1 AND lrd.send_success = 0
                    AND lo.status = 1
                ORDER BY lrd.id DESC 
                LIMIT ? OFFSET ?
            """, (room_id, limit, offset))
        
        groups = [{
            "time": row[0], 
            "lab_order_id": row[1], 
            "speed": row[2], 
            "sample_inspection": row[3]
        } for row in cursor]
        
        # Count query
        if room_id == "":
            cursor.execute("""
                SELECT COUNT(*) 
                FROM lab_receive_detail lrd
                INNER JOIN lab_order lo ON lrd.lab_order_id = lo.id
                WHERE lrd.room_action_status = 1 AND lrd.send_success = 0
                    AND lo.status = 1
            """)
        else:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM lab_receive_detail lrd
                INNER JOIN lab_order lo ON lrd.lab_order_id = lo.id
                WHERE lrd.receive_from_room = ? 
                    AND lrd.room_action_status = 1 AND lrd.send_success = 0
                    AND lo.status = 1
            """, (room_id,))
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
        raise HTTPException(status_code=500, detail="Failed to retrieve received labs")
    finally:
        conn.close()


@router.get("/get_received_labs/barcode")
def get_received_labs_by_barcode(barcode: str, room_id: str = ""):
    """
    ค้นหา lab ที่รับแล้วด้วย barcode
    room_id = "" หมายถึง admin สามารถดูได้ทุกห้อง
    """
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        
        # Convert barcode to lab_order_id
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
                    lrd.dtime,
                    lrd.lab_order_id,
                    sr.speed,
                    sr.sample_inspection,
                    sr.id AS sample_id,
                    lrd.receive_from_room
                FROM lab_receive_detail lrd
                INNER JOIN lab_order lo ON lrd.lab_order_id = lo.id
                INNER JOIN sample_registration sr ON lo.sample_id = sr.id
                WHERE lrd.lab_order_id = ? 
                    AND lrd.receive_from_room = ? 
                    AND lrd.room_action_status = 1 AND lrd.send_success = 0
                    AND lo.status = 1
                ORDER BY lrd.id DESC 
            """
            cursor.execute(query, (lab_order_id, room_id))
        else:
            # Admin mode - no room restriction
            query = """
                SELECT 
                    lrd.dtime,
                    lrd.lab_order_id,
                    sr.speed,
                    sr.sample_inspection,
                    sr.id AS sample_id,
                    lrd.receive_from_room
                FROM lab_receive_detail lrd
                INNER JOIN lab_order lo ON lrd.lab_order_id = lo.id
                INNER JOIN sample_registration sr ON lo.sample_id = sr.id
                WHERE lrd.lab_order_id = ? 
                    AND lrd.room_action_status = 1 AND lrd.send_success = 0
                    AND lo.status = 1
                ORDER BY lrd.id DESC 
            """
            cursor.execute(query, (lab_order_id,))
        
        results = cursor.fetchall()
        
        if not results:
            if room_id:
                return {
                    "job_progress": [],
                    "total": 0,
                    "found": False,
                    "message": "ไม่พบข้อมูล Barcode นี้ในรายการที่รับแล้ว หรือไม่มีสิทธิ์เข้าถึง"
                }
            else:
                return {
                    "job_progress": [],
                    "total": 0,
                    "found": False,
                    "message": "ไม่พบข้อมูล Barcode นี้ในรายการที่รับแล้ว"
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
