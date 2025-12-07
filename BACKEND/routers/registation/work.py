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
        
