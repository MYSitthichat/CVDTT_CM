from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from database import get_db_connection
import mariadb
import os

router = APIRouter(
    prefix="/doctor_report",
    tags=["Doctor Report"]
)

@router.get("/pending_reports")
def get_pending_reports(room_id: str = ""):
    """ดึงรายการรายงานที่รอการตรวจสอบจากแพทย์ (approver = 0)"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # ทดสอบว่ามีตาราง report_form หรือไม่
        try:
            cursor.execute("SHOW TABLES LIKE 'report_form'")
            table_exists = cursor.fetchone()
            if not table_exists:
                print("ERROR: ตาราง report_form ไม่มีในฐานข้อมูล")
                # ถ้าไม่มีตาราง ให้คืนข้อมูลว่างแทน error
                return {"data": [], "count": 0, "message": "ตาราง report_form ไม่พร้อมใช้งาน"}
        except Exception as check_error:
            print(f"ERROR checking table: {check_error}")
        
        # ดึงข้อมูลจากตาราง report_form JOIN กับตารางอื่นๆ
        sql = """
            SELECT 
                rf.id,
                rf.dtime as report_date,
                rf.id as report_number,
                rf.lab_order_id as sample_id,
                sr.sample_inspection,
                ri.thai_name as lab_room,
                CONCAT(e.title, ' ', e.name, ' ', e.surname) as reporter_name,
                rf.state,
                rf.status,
                rf.location,
                rf.comment
            FROM report_form rf
            INNER JOIN lab_order lo ON rf.lab_order_id = lo.id
            LEFT JOIN sample_registration sr ON lo.sample_id = sr.id
            LEFT JOIN room_information ri ON rf.room_id = ri.id
            LEFT JOIN employee e ON rf.recorder = e.id
            WHERE rf.approver = 0 AND rf.status = 1
        """
        
        params = []
        
        # ถ้ามีการระบุ room_id ให้กรองเฉพาะห้องนั้น
        if room_id:
            sql += " AND rf.room_id = ?"
            params.append(room_id)
        
        sql += " ORDER BY rf.id DESC"  # เรียงจากเลขที่รายงานมากไปน้อย
        
        # print(f"DEBUG SQL: {sql}")
        # print(f"DEBUG PARAMS: {params}")
        
        cursor.execute(sql, params if params else ())
        
        columns = [col[0] for col in cursor.description]
        results = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            # แปลง state และ status เป็นข้อความ
            if row_dict.get('state') == 1:
                row_dict['state_text'] = 'รอการยืนยัน'
            elif row_dict.get('state') == 2:
                row_dict['state_text'] = 'ส่งแล้ว'
            else:
                row_dict['state_text'] = 'อื่นๆ'
            
            results.append(row_dict)
        
        # print(f"DEBUG: พบข้อมูล {len(results)} รายการ")
        return {"data": results, "count": len(results)}
    
    except mariadb.Error as e:
        error_msg = f"Database error: {str(e)}"
        # print(f"DEBUG DB ERROR: {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        # print(f"DEBUG UNEXPECTED ERROR: {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_msg)
    finally:
        if conn:
            conn.close()


@router.get("/pending_reports_from_lab_order")
def get_pending_reports_from_lab_order(room_id: str = ""):
    """ดึงรายการจาก lab_order โดยตรง (กรณีตาราง report_form ยังไม่มี)"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # ดึงข้อมูลจาก lab_order โดยตรง
        sql = """
            SELECT 
                lo.id,
                lo.dtime as report_date,
                lo.id as report_number,
                lo.sample_id,
                ri.thai_name as lab_room,
                CONCAT(e.title, ' ', e.name, ' ', e.surname) as reporter_name,
                lo.state,
                lo.status
            FROM lab_order lo
            LEFT JOIN room_information ri ON lo.room_id = ri.id
            LEFT JOIN employee e ON lo.employee_id = e.id
            WHERE lo.status = 1
        """
        
        params = []
        
        if room_id:
            sql += " AND lo.room_id = ?"
            params.append(room_id)
        
        sql += " ORDER BY lo.dtime DESC LIMIT 100"
        
        cursor.execute(sql, params if params else ())
        
        columns = [col[0] for col in cursor.description]
        results = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            row_dict['state_text'] = 'รอการยืนยัน'
            results.append(row_dict)
        
        return {"data": results, "count": len(results)}
    
    except mariadb.Error as e:
        print(f"DEBUG DB ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        if conn:
            conn.close()


@router.get("/report_by_id")
def get_report_by_id(report_id: int):
    """ดึงรายละเอียดรายงานตาม ID"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        sql = """
            SELECT 
                rf.*,
                lo.id as report_number,
                lo.sample_id,
                ri.thai_name as lab_room,
                CONCAT(e.title, ' ', e.name, ' ', e.surname) as reporter_name
            FROM report_form rf
            INNER JOIN lab_order lo ON rf.lab_order_id = lo.id
            LEFT JOIN room_information ri ON rf.room_id = ri.id
            LEFT JOIN employee e ON rf.recorder = e.id
            WHERE rf.id = ?
        """
        
        cursor.execute(sql, (report_id,))
        
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        if row:
            return {"data": dict(zip(columns, row))}
        else:
            raise HTTPException(status_code=404, detail="Report not found")
    
    except mariadb.Error as e:
        print(f"DEBUG DB ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()


@router.get("/report_file/{report_id}")
def get_report_file(report_id: int):
    """ดึงไฟล์รายงานตาม report_id"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # ดึง location จาก report_form
        sql = "SELECT location FROM report_form WHERE id = ?"
        cursor.execute(sql, (report_id,))
        result = cursor.fetchone()
        
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="Report location not found")
        
        location = result[0]
        
        # สร้าง absolute path
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(backend_dir, location.replace('/', os.sep))
        
        print(f"DEBUG: Looking for file at: {file_path}")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {location}")
        
        # ส่งไฟล์กลับไป
        return FileResponse(
            path=file_path,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            filename=os.path.basename(file_path)
        )
    
    except mariadb.Error as e:
        print(f"DEBUG DB ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

