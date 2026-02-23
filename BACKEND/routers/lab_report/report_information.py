from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from database import get_db_connection
import mariadb
import os
import shutil

router = APIRouter(
    prefix="/lab_form_edite",
    tags=["Report Information"]
)

# --- Pydantic Models (สำหรับรับค่า JSON) ---
class ReportAddRequest(BaseModel):
<<<<<<< HEAD
    report_name: str
    room_id: int
    report_path: str
    updater_id: int
=======
    from_name: str
    lab_name: str
    location_file: str
    updater: int
    comment: str = ""
>>>>>>> ef7021bec0600bab8bb8970532f8dd9a047875ae

class ReportVersionRequest(BaseModel):
    old_report_id: int
    new_name: str
    new_path: str
<<<<<<< HEAD
    room_id: int
    updater_id: int
=======
    lab_name: str
    updater: int
    comment: str = ""
>>>>>>> ef7021bec0600bab8bb8970532f8dd9a047875ae

class ReportDeleteRequest(BaseModel):
    report_id: int
    updater: int

# --- Helper Function แปลง Tuple เป็น Dict ---
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# --- API Endpoints ---

@router.get("/all_by_status")
def get_all_reports_by_status(status: int = 1):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
    
        sql = """
<<<<<<< HEAD
            SELECT 
                t1.id, t1.report_name, t1.room_id, t1.report_path, t1.status, t1.updater, 
                t2.name AS room_name
            FROM report_information t1
            LEFT JOIN room_information t2 ON t1.room_id = t2.id
            WHERE t1.status = ?
            ORDER BY t1.room_id ASC, t1.id DESC
=======
            SELECT id, lab_name, from_name, comment, status, location_file, updater, dTime
            FROM lab_form_edite
            WHERE status = ?
            ORDER BY lab_name ASC, id DESC
>>>>>>> ef7021bec0600bab8bb8970532f8dd9a047875ae
        """

        cursor.execute(sql, (status,))
        
        columns = [col[0] for col in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
            
        return {"data": results}

    except mariadb.Error as e:
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
<<<<<<< HEAD
            INSERT INTO report_information (report_name, room_id, report_path, updater, status) 
            VALUES (?, ?, ?, ?, 1)
        """
        cursor.execute(sql, (request.report_name, request.room_id, request.report_path, request.updater_id))
=======
            INSERT INTO lab_form_edite (from_name, lab_name, location_file, updater, status, comment) 
            VALUES (?, ?, ?, ?, 1, ?)
        """
        cursor.execute(sql, (request.from_name, request.lab_name, request.location_file, request.updater, request.comment))
>>>>>>> ef7021bec0600bab8bb8970532f8dd9a047875ae
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
        update_sql = "UPDATE lab_form_edite SET status = 0, updater = ? WHERE id = ?"
        cursor.execute(update_sql, (request.updater, request.old_report_id))
        
        # 2. Insert ตัวใหม่ (status = 1)
        insert_sql = """
<<<<<<< HEAD
            INSERT INTO report_information (report_name, room_id, report_path, updater, status) 
            VALUES (?, ?, ?, ?, 1)
        """
        cursor.execute(insert_sql, (request.new_name, request.room_id, request.new_path, request.updater_id))
=======
            INSERT INTO lab_form_edite (from_name, lab_name, location_file, updater, status, comment) 
            VALUES (?, ?, ?, ?, 1, ?)
        """
        cursor.execute(insert_sql, (request.new_name, request.lab_name, request.new_path, request.updater, request.comment))
>>>>>>> ef7021bec0600bab8bb8970532f8dd9a047875ae
        
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
        sql = "UPDATE lab_form_edite SET status = 0, updater = ? WHERE id = ?"
        cursor.execute(sql, (updater_id, report_id))  # updater_id passed as query param
        conn.commit()
        
        return {"status": "success", "message": "Report deleted successfully"}

    except mariadb.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@router.get("/by_room_and_status")
def get_reports_by_room_and_status(lab_name: str, status: int = 1):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        sql = """
<<<<<<< HEAD
            SELECT 
                t1.id, t1.report_name, t1.room_id, t1.report_path, t1.status, t1.updater,
                t2.name AS room_name
            FROM report_information t1
            LEFT JOIN room_information t2 ON t1.room_id = t2.id
            WHERE t1.room_id = ? AND t1.status = ?
            ORDER BY t1.id DESC
=======
            SELECT id, lab_name, from_name, comment, status, location_file, updater, dTime
            FROM lab_form_edite
            WHERE lab_name = ? AND status = ?
            ORDER BY id DESC
>>>>>>> ef7021bec0600bab8bb8970532f8dd9a047875ae
        """
        
        cursor.execute(sql, (lab_name, status))
        
        columns = [col[0] for col in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
            
        return results

    except mariadb.Error as e:
        print(f"DEBUG DB ERROR: {e}") 
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@router.get("/get_all_rooms_list")
def get_all_rooms_list():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        sql = "SELECT DISTINCT lab_name FROM lab_form_edite WHERE status = 1 ORDER BY lab_name ASC"
        cursor.execute(sql)
        results = [row[0] for row in cursor.fetchall()]
        return {"data": results}

    except mariadb.Error as e:
        print(f"DEBUG DB ERROR: {e}") 
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()


@router.post("/add_lab_name")
def add_lab_name(lab_name: str = Form(...), updater: int = Form(...)):
    """
    เพิ่ม lab_name ใหม่ลงใน lab_form_edite (status=1, from_name='')
    เพื่อให้ชื่อ lab ปรากฏใน TreeWidget ทันทีเป็น group header
    """
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = conn.cursor()

        # ตรวจสอบว่ามี lab_name นี้อยู่แล้วหรือไม่
        cursor.execute(
            "SELECT COUNT(*) FROM lab_form_edite WHERE lab_name = ? AND status = 1",
            (lab_name,)
        )
        if cursor.fetchone()[0] > 0:
            raise HTTPException(status_code=409, detail=f"lab_name '{lab_name}' already exists")

        cursor.execute(
            "INSERT INTO lab_form_edite (lab_name, from_name, location_file, updater, status, comment) VALUES (?, '', '', ?, 1, '')",
            (lab_name, updater)
        )
        conn.commit()
        return {"status": "success", "message": f"Lab name '{lab_name}' added successfully"}

    except HTTPException:
        raise
    except mariadb.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()


@router.post("/upload_file")
async def upload_file(
    file: UploadFile = File(...),
    lab_name: str = Form(...),
    from_name: str = Form(...)
):
    """
    อัพโหลดไฟล์ไปเก็บที่ report_template/word/{lab_name}/{from_name}.ext
    """
    try:
        # หา BACKEND/ directory จาก routers/lab_report/report_information.py
        # __file__ → BACKEND/routers/lab_report/report_information.py
        # dirname x3 → BACKEND/
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        word_dir = os.path.join(backend_dir, "report_template", "word")
        word_dir = os.path.normpath(word_dir)
        # print(f"DEBUG upload path: {word_dir}")

        # สร้าง subfolder ตาม lab_name
        lab_folder = os.path.join(word_dir, lab_name)
        os.makedirs(lab_folder, exist_ok=True)

        # ตั้งชื่อไฟล์ตาม from_name + นามสกุลเดิม
        _, ext = os.path.splitext(file.filename)
        safe_from_name = from_name.replace("/", "_").replace("\\", "_")
        dest_filename = f"{safe_from_name}{ext}"
        dest_path = os.path.join(lab_folder, dest_filename)

        # เขียนไฟล์
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # เก็บ relative path (relative to BACKEND/) ไม่ใช่ absolute path
        relative_path = os.path.relpath(dest_path, backend_dir).replace("\\", "/")
        # print(f"DEBUG upload relative_path: {relative_path}")

        return {
            "status": "success",
            "file_path": relative_path,
            "message": f"File uploaded successfully"
        }

    except Exception as e:
        print(f"DEBUG UPLOAD ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Upload error: {e}")


@router.get("/download_file")
def download_file(relative_path: str):
    """
    ดาวน์โหลดไฟล์จาก relative path ที่เก็บใน database
    """
    try:
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        full_path = os.path.normpath(os.path.join(backend_dir, relative_path))

        # Security check: ตรวจสอบว่า path อยู่ภายใน backend_dir เท่านั้น
        if not full_path.startswith(os.path.normpath(backend_dir)):
            raise HTTPException(status_code=403, detail="Access denied")

        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail=f"File not found: {relative_path}")

        filename = os.path.basename(full_path)
        return FileResponse(full_path, filename=filename, media_type="application/octet-stream")

    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG DOWNLOAD ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Download error: {e}")