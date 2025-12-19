import mariadb
from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pathlib import Path
import os
import shutil
from database import get_db_connection # เรียกใช้ Connection เดิมของคุณ



router = APIRouter(tags=["save_report_lab"])
BASE_DIR = Path(__file__).resolve().parent.parent.parent / "report_file"


@router.post("/save_report_files")
async def save_report_files(
    lab_name: str = Form(...),
    barcode: str = Form(...),
    lab_id: int = Form(...),        # lab_order_id
    case_id: int = Form(...),       # NEW: case_id
    room_id: int = Form(...),       # NEW: send_from_room
    updater: int = Form(...),       # NEW: user_id
    date_str: str = Form(...),
    file_word: UploadFile = File(...),
    file_pdf: UploadFile = File(...)
):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        # 1. จัดการไฟล์ (File Handling)
        safe_lab_name = "".join([c for c in lab_name if c.isalnum() or c in (' ', '_', '-')]).strip().replace(" ", "_")
        
        target_folder = BASE_DIR / safe_lab_name / barcode
        word_folder = target_folder / "WORD"
        pdf_folder = target_folder / "PDF"
        
        word_folder.mkdir(parents=True, exist_ok=True)
        pdf_folder.mkdir(parents=True, exist_ok=True)
        
        final_word_name = file_word.filename
        final_pdf_name = file_pdf.filename
        
        word_path = word_folder / final_word_name
        pdf_path = pdf_folder / final_pdf_name

        with open(word_path, "wb") as buffer:
            shutil.copyfileobj(file_word.file, buffer)
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file_pdf.file, buffer)
        cursor = conn.cursor()
        
        # SQL Insert ข้อมูลการส่งงาน
        sql = """
            INSERT INTO send_lab_detail 
            (dtime, case_id, lab_order_id, send_from_room, folder_name, word_name, pdf_name, updater)
            VALUES (NOW(), ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (
            case_id, 
            lab_id, 
            room_id, 
            safe_lab_name, 
            final_word_name, 
            final_pdf_name, 
            updater
        ))
        
        conn.commit()

        return {
            "status": "success", 
            "message": "Files saved and database updated successfully",
            "saved_id": cursor.lastrowid
        }

    except Exception as e:
        print(f"Error saving files: {e}")
        return {"status": "error", "message": str(e)}
        
    finally:
        if conn: conn.close()


@router.get("/initialize_lab_folders")
def initialize_lab_folders():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        try:
            sql = "SELECT name FROM room_information WHERE status = 1" 
            cursor.execute(sql)
            rooms = cursor.fetchall()
            if not BASE_DIR.exists():
                BASE_DIR.mkdir(parents=True, exist_ok=True)

            created_count = 0
            existing_count = 0
            folders_status = []

            for room in rooms:
                lab_name = room[0] 
                safe_lab_name = "".join([c for c in lab_name if c.isalnum() or c in (' ', '_', '-')]).strip().replace(" ", "_")
                lab_folder_path = BASE_DIR / safe_lab_name
                if lab_folder_path.exists():
                    existing_count += 1
                    folders_status.append(f"{safe_lab_name}: Found")
                else:
                    lab_folder_path.mkdir(parents=True, exist_ok=True)
                    created_count += 1
                    folders_status.append(f"{safe_lab_name}: Created")
                    
            if created_count > 0:
                return {
                    "status": "CREATED",
                    "message": f"Created {created_count} new folders. Found {existing_count} existing.",
                    "details": folders_status
                }
            else:
                return {
                    "status": "FOUND",
                    "message": "All lab folders already exist.",
                    "details": folders_status
                }
        except mariadb.Error as e:
            print(f"Database Error: {e}")
            return {
                "status": "ERROR",
                "message": "Server encountered an error while initializing folders.",
                "error_detail": str(e)
            }

    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    finally:
        if conn:
            conn.close()