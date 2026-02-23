from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from database import get_db_connection
import mariadb
from datetime import datetime

router = APIRouter(
    prefix="/report_form",
    tags=["Report Form"]
)

# --- Pydantic Models ---
class ReportFormCreateRequest(BaseModel):
    lab_order_id: int
    location: str = ""
    comment: str = ""
    state: int = 0
    status: int = 1
    recorder: int = 0
    approver: int = 0
    room_id: int = 0

class ReportFormUpdateRequest(BaseModel):
    id: int
    location: str = None
    comment: str = None
    state: int = None
    status: int = None
    recorder: int = None
    approver: int = None

# --- Helper Function ---
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# --- API Endpoints ---

@router.get("/latest_id")
def get_latest_report_form_id():
    """ดึง ID ล่าสุดจาก report_form table เพื่อสร้างเลขที่รายงาน"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        sql = "SELECT MAX(id) as max_id FROM report_form"
        cursor.execute(sql)
        result = cursor.fetchone()
        
        max_id = result[0] if result and result[0] else 0
        next_id = max_id + 1
        
        return {
            "status": "success",
            "current_max_id": max_id,
            "next_id": next_id
        }
    
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@router.get("/by_lab_order/{lab_order_id}")
def get_report_form_by_lab_order(lab_order_id: int):
    """ดึงข้อมูล report_form จาก lab_order_id"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id, dtime, lab_order_id, location, comment, state, status, recorder, approver, room_id
            FROM report_form
            WHERE lab_order_id = ?
            ORDER BY id DESC
        """
        cursor.execute(sql, (lab_order_id,))
        
        columns = [col[0] for col in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return {"status": "success", "data": results}
    
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@router.post("/create")
def create_report_form(request: ReportFormCreateRequest):
    """สร้าง report_form ใหม่"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO report_form (lab_order_id, location, comment, state, status, recorder, approver, room_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (
            request.lab_order_id,
            request.location,
            request.comment,
            request.state,
            request.status,
            request.recorder,
            request.approver,
            request.room_id
        ))
        conn.commit()
        
        # Get the inserted ID
        inserted_id = cursor.lastrowid
        
        return {
            "status": "success",
            "message": "Report form created successfully",
            "id": inserted_id
        }
    
    except mariadb.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@router.put("/update")
def update_report_form(request: ReportFormUpdateRequest):
    """อัพเดท report_form"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # Build dynamic update query
        update_fields = []
        params = []
        
        if request.location is not None:
            update_fields.append("location = ?")
            params.append(request.location)
        
        if request.comment is not None:
            update_fields.append("comment = ?")
            params.append(request.comment)
        
        if request.state is not None:
            update_fields.append("state = ?")
            params.append(request.state)
        
        if request.status is not None:
            update_fields.append("status = ?")
            params.append(request.status)
        
        if request.recorder is not None:
            update_fields.append("recorder = ?")
            params.append(request.recorder)
        
        if request.approver is not None:
            update_fields.append("approver = ?")
            params.append(request.approver)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        params.append(request.id)
        sql = f"UPDATE report_form SET {', '.join(update_fields)} WHERE id = ?"
        
        cursor.execute(sql, tuple(params))
        conn.commit()
        
        return {
            "status": "success",
            "message": "Report form updated successfully"
        }
    
    except mariadb.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@router.get("/lab_order_details/{lab_order_id}")
def get_lab_order_with_case_details(lab_order_id: int):
    """ดึงข้อมูล lab_order พร้อม case_registration และ lab_receive_detail"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # First, check if lab_order exists
        cursor.execute("SELECT id, dtime, sample_id, room_id FROM lab_order WHERE id = ?", (lab_order_id,))
        lab_order_result = cursor.fetchone()
        
        if not lab_order_result:
            raise HTTPException(status_code=404, detail=f"Lab order {lab_order_id} not found")
        
        # Build basic data from lab_order
        data = {
            "lab_order_id": lab_order_result[0],
            "lab_order_dtime": lab_order_result[1],
            "sample_id": lab_order_result[2],
            "room_id": lab_order_result[3],
            "case_id": None,
            "case_dtime": None,
            "sender_id": None,
            "owner_id": None,
            "project_name": None,
            "receive_dtime": None
        }
        
        # Try to get case_registration data if sample_registration exists
        if lab_order_result[2]:  # if sample_id exists
            cursor.execute("""
                SELECT sr.case_id, cr.dtime, cr.sender_id, cr.owner_id, cr.project_name
                FROM sample_registration sr
                LEFT JOIN case_registration cr ON sr.case_id = cr.id
                WHERE sr.id = ?
            """, (lab_order_result[2],))
            
            case_result = cursor.fetchone()
            if case_result:
                data["case_id"] = case_result[0]
                data["case_dtime"] = case_result[1]
                data["sender_id"] = case_result[2]
                data["owner_id"] = case_result[3]
                data["project_name"] = case_result[4]
        
        # Get receive date from lab_receive_detail
        cursor.execute("""
            SELECT dtime
            FROM lab_receive_detail
            WHERE lab_order_id = ?
            ORDER BY id DESC
            LIMIT 1
        """, (lab_order_id,))
        
        receive_result = cursor.fetchone()
        if receive_result:
            data["receive_dtime"] = receive_result[0]
        
        return {
            "status": "success",
            "data": data
        }
    
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()
