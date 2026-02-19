from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db_connection
import mariadb

router = APIRouter(
    prefix="/report_information",
    tags=["Report Information"]
)

# --- Pydantic Models (สำหรับรับค่า JSON) ---
class ReportAddRequest(BaseModel):
    report_name: str
    room_id: int
    report_path: str
    updater_id: int

class ReportVersionRequest(BaseModel):
    old_report_id: int
    new_name: str
    new_path: str
    room_id: int
    updater_id: int

class ReportDeleteRequest(BaseModel):
    report_id: int
    updater_id: int

# --- Helper Function แปลง Tuple เป็น Dict ---
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# --- API Endpoints ---

@router.get("/by_room_and_status")
def get_reports_by_room_and_status(room_id: int, status: int = 1):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # --- แก้ไข SQL ตรงนี้: ตัด created_at, updated_at ออก ---
        sql = """
            SELECT id, report_name, room_id, report_path, status, updater
            FROM report_information 
            WHERE room_id = ? AND status = ?
            ORDER BY id DESC
        """
        cursor.execute(sql, (room_id, status))
        
        columns = [col[0] for col in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
            
        return results

    except mariadb.Error as e:
        # เพิ่ม print เพื่อดู error จริงใน terminal backend ด้วย
        print(f"DEBUG DB ERROR: {e}") 
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@router.post("/add")
def add_report(request: ReportAddRequest):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO report_information (report_name, room_id, report_path, updater, status) 
            VALUES (?, ?, ?, ?, 1)
        """
        cursor.execute(sql, (request.report_name, request.room_id, request.report_path, request.updater_id))
        conn.commit()
        
        return {"status": "success", "message": "Report added successfully"}

    except mariadb.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@router.post("/save_new_version")
def save_new_report_version(request: ReportVersionRequest):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # 1. Soft Delete ตัวเก่า (status = 0)
        update_sql = "UPDATE report_information SET status = 0, updater = ? WHERE id = ?"
        cursor.execute(update_sql, (request.updater_id, request.old_report_id))
        
        # 2. Insert ตัวใหม่ (status = 1)
        insert_sql = """
            INSERT INTO report_information (report_name, room_id, report_path, updater, status) 
            VALUES (?, ?, ?, ?, 1)
        """
        cursor.execute(insert_sql, (request.new_name, request.room_id, request.new_path, request.updater_id))
        
        conn.commit()
        return {"status": "success", "message": "Version updated successfully"}

    except mariadb.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@router.delete("/delete")
def delete_report(report_id: int, updater_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        # Soft Delete
        sql = "UPDATE report_information SET status = 0, updater = ? WHERE id = ?"
        cursor.execute(sql, (updater_id, report_id))
        conn.commit()
        
        return {"status": "success", "message": "Report deleted successfully"}

    except mariadb.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()