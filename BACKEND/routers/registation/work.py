# routers/work.py
from fastapi import APIRouter, HTTPException
from typing import Optional
import mariadb
from database import get_db_connection
from schemas import SpecimenData

router = APIRouter(tags=["Work & Specimen"])

@router.get("/get_max_sample_id")
def get_max_sample_id():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) AS last_case_number FROM case_registration")
        max_id = cursor.fetchone()
        return {"max_id": max_id[0] if max_id and max_id[0] is not None else 0}
    except mariadb.Error:
        raise HTTPException(status_code=500, detail="Failed to retrieve max sample ID")
    finally:
        conn.close()

@router.post("/add_new_work")
def add_work(sender_id: Optional[int] = None, owner_id: Optional[int] = None, 
             project_name: Optional[str] = "", updater: Optional[int] = None):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        if sender_id is None or owner_id is None:
            raise HTTPException(status_code=422, detail="sender_id and owner_id are required")
        
        cursor = conn.cursor()
        sql = """INSERT INTO case_registration (sender_id, owner_id, project_name, updater) VALUES (?, ?, ?, ?)"""
        cursor.execute(sql, (sender_id, owner_id, project_name or "", updater))
        conn.commit()
        return {"status": "success", "work_id": cursor.lastrowid}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to add work: {str(e)}")
    finally:
        conn.close()

@router.post("/add_new_specimen")
def add_new_specimen(data: SpecimenData):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        sql = """INSERT INTO sample_registration 
        (case_id, name, opd_number, sex, age_year, age_month, age_day, demise, 
         species, breed, sample_type, weight, dead_date, collect_date, 
         keep_method, speed, medical_record, dosage_record, sample_inspection, updater)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        val = (data.case_id, data.name, data.opd_number, data.sex, data.age_year, data.age_month, data.age_day, 
               data.demise, data.species, data.breed, data.sample_type, data.weight, data.dead_date, 
               data.collect_date, data.keep_method, data.speed, data.medical_record, data.dosage_record, 
               data.sample_inspection, data.updater)
        cursor.execute(sql, val)
        conn.commit()
        return {"status": "success", "specimen_id": cursor.lastrowid}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to add specimen: {str(e)}")
    finally:
        conn.close()

@router.get("/get_case_details/{case_id}")
def get_case_details(case_id: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        sql = """SELECT lab_order.dtime, lab_order.id, sample_registration.species, 
                 room_information.code, room_information.nickname, sample_registration.keep_method, 
                 sample_registration.speed 
                 FROM case_registration 
                 LEFT JOIN sample_registration ON case_registration.id = sample_registration.case_id 
                 RIGHT JOIN lab_order ON sample_registration.id = lab_order.sample_id 
                 LEFT JOIN room_information ON lab_order.room_id = room_information.id 
                 WHERE case_registration.id = %s AND lab_order.status = 1"""
        cursor.execute(sql, (case_id,))
        result = cursor.fetchall()
        return {"status": "success", "case_id": case_id, "data": result}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to update case details: {str(e)}")
    finally:
        conn.close()
        

@router.get("/delete_sample_registration/{order_id}")
def delete_sample_registration(order_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = None
    try:
        cursor = conn.cursor()
        sql = """SELECT sample_id, room_id FROM lab_order WHERE id = %s AND status = 1"""
        cursor.execute(sql, (order_id,))
        fine_info = cursor.fetchone()
        
        if not fine_info:
            raise HTTPException(status_code=404, detail=f"Order ID {order_id} not found or already deleted")
        
        sample_id = fine_info[0]
        room_id = fine_info[1]
        room_code = None
        if room_id:
            get_room_code = """SELECT code FROM room_information WHERE id = %s"""
            cursor.execute(get_room_code, (room_id,))
            room_info = cursor.fetchone()
            
            if room_info:
                room_code = room_info[0]
                if room_code and room_code.startswith('E304'):  # Parasite
                    update_parasite = """UPDATE lab_parasite_biology SET status = 0 WHERE sample_id = %s"""
                    cursor.execute(update_parasite, (sample_id,))
                    
                elif room_code and room_code.startswith('E315'):  # Bacteria
                    update_bacteria = """UPDATE lab_bacteria_biology SET status = 0 WHERE sample_id = %s"""
                    cursor.execute(update_bacteria, (sample_id,))
                    
                elif room_code and room_code.startswith('E410'):  # Molecular Biology
                    update_molecular = """UPDATE lab_molecular_biology SET status = 0 WHERE sample_id = %s"""
                    cursor.execute(update_molecular, (sample_id,))
                else:
                    print(f"Unknown room_code: {room_code}, skipping result table update")
                    
        update_tracking_status = """UPDATE tracking_lab_order SET status = 0 WHERE lab_order_id = %s"""
        cursor.execute(update_tracking_status, (order_id,))
        print(f"Updated tracking_lab_order")

        update_lab_order_status = """UPDATE lab_order SET status = 0 WHERE id = %s"""
        cursor.execute(update_lab_order_status, (order_id,))
        print(f"Updated lab_order")

        update_sample_registration_status = """UPDATE sample_registration SET status = 0 WHERE id = %s"""
        cursor.execute(update_sample_registration_status, (sample_id,))
        print(f"Updated sample_registration")

        conn.commit()
        print(f"All changes committed successfully")
        
        return {
            "status": "success",
            "deleted_order_id": order_id,
            "sample_id": sample_id,
            "room_id": room_id,
            "room_code": room_code
        }
    
    except mariadb.Error as e:
        if conn:
            conn.rollback()
        print(f"❌ MariaDB Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Unexpected Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            



