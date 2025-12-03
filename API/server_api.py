from fastapi import FastAPI, HTTPException
import mariadb
from pydantic import BaseModel
from typing import List, Optional
from passlib.context import CryptContext
import os
import base64


app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# DB_CONFIG = {
#     "host": "202.28.24.55",
#     "user": "python_engine",
#     "password": "c#@4573kt",
#     "database": "cvdtt_lab",
#     "port": 3306
# }

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "cvdtt_lab",
    "port": 3306
}

class SearchResult(BaseModel):
    id: int
    name: str
    surname: Optional[str] = "" 
    tax_id: Optional[str] = "-"
    display_text: str

# --- Molecular Biology Data Model ---
class MolecularBiologyData(BaseModel):
    sample_id: str
    tests: List[dict]  # List of test items with name, amount, price
    cPCR_req: Optional[int] = 0
    qPCR_req: Optional[int] = 0
    extraction_req: Optional[int] = 0
    updater: Optional[int] = None  # user_id of person saving the data

# --- parasite Biology Data Model ---
class ParasiteBiologyData(BaseModel):
    sample_id: str
    tests: List[dict]  # List of test items with name, amount, price
    updater: Optional[int] = None  # user_id of person saving the data

# --- Specimen Registration Data Model ---
class SpecimenData(BaseModel):
    case_id: Optional[int] = None
    name: Optional[str] = ""
    opd_number: Optional[str] = ""
    sex: Optional[str] = ""
    age_year: Optional[int] = 0
    age_month: Optional[int] = 0
    age_day: Optional[int] = 0
    demise: Optional[str] = ""
    species: str  # REQUIRED
    breed: Optional[str] = ""
    sample_type: Optional[str] = ""
    weight: Optional[float] = 0.0
    dead_date: Optional[str] = None
    collect_date: Optional[str] = None
    keep_method: Optional[str] = ""
    speed: Optional[str] = ""
    medical_record: Optional[str] = ""
    dosage_record: Optional[str] = ""
    sample_inspection: Optional[str] = ""
    updater: Optional[int] = None
    
# --- Helper Function เชื่อมต่อ DB ---
def get_db_connection():
    try:
        conn = mariadb.connect(**DB_CONFIG)
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

@app.get("/")
def index():
    return {"message": "CVDTT API is running"}

# LOGIN AND FORGOT PASSWORD

@app.on_event("startup")
def hash_plain_passwords():
    conn = get_db_connection()
    if not conn:
        print("Cannot connect to database for password encryption")
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, username, password FROM employee")
        users = cursor.fetchall()
        updated_count = 0
        for user_id, username, plain_password in users:
            if plain_password.startswith("$2b$"):
                continue
            try:
                password_to_hash = plain_password[:72]  # ตัดไม่เกิน 72 bytes
                hashed = pwd_context.hash(password_to_hash)
                cursor.execute("UPDATE employee SET password = ? WHERE id = ?", (hashed, user_id))
                updated_count += 1
                print(f"Encrypted password for user: {username}")
            except Exception as e:
                print(f"Error encrypting password for user {username}: {e}")
                continue
        
        if updated_count > 0:
            conn.commit()
            print(f"Total {updated_count} passwords encrypted on startup")
        else:
            print("All passwords are already encrypted")

    except mariadb.Error as e:
        print(f"Database error during password encryption: {e}")
    finally:
        conn.close()


@app.post("/login")
def login(username: str, password: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM employee WHERE username = ? LIMIT 1 AND status = 1", (username,))
        user = cursor.fetchone()
        if not user:
            return {"success": False, "user_id": None}
        
        user_id = user[0]
        stored_password = user[1]
        password_to_verify = password[:72]
        if stored_password.startswith("$2b$"):
            try:
                is_valid = pwd_context.verify(password_to_verify, stored_password)
                return {"success": is_valid, "user_id": user_id if is_valid else None}
            except Exception as e:
                print(f"Password verification error: {e}")
                return {"success": False, "user_id": None}
        else:
            if password != stored_password:
                return {"success": False, "user_id": None}
            try:
                new_hashed = pwd_context.hash(password_to_verify)
                cursor.execute("UPDATE employee SET password = ? WHERE id = ?", (new_hashed, user_id))
                conn.commit()
                print(f"Password encrypted for user_id: {user_id}")
                return {"success": True, "user_id": user_id}
            except Exception as e:
                print(f" Error encrypting password: {e}")
                return {"success": True, "user_id": user_id}
                
    except mariadb.Error as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database query failed")
    finally:
        conn.close()

@app.post("/check_email")
def check_email(email: str) -> bool:
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM employee WHERE email = ? LIMIT 1", (email,))
        email_check = cursor.fetchone()
        
        if not email_check:
            return False
        return True
    except mariadb.Error as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database query failed")
    finally:
        conn.close()

@app.post("/update_password")
def update_password(email: str, new_password: str) -> bool:
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE employee SET password = ? WHERE email = ?", (new_password, email))
        conn.commit()
        return True
    except mariadb.Error as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database query failed")
    finally:
        conn.close()
# LOGIN AND FORGOT PASSWORD

# --- Customer Search API ---
@app.get("/search", response_model=List[SearchResult])
def search_customer(q: str):
    """ค้นหารายชื่อลูกค้า (ค้นหาได้ทั้ง ชื่อ, นามสกุล และ ID)"""
    if not q or len(q) < 2:
        return []
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    results = []
    try:
        cursor = conn.cursor()
        # ค้นหาจาก: ชื่อ, นามสกุล, หรือ ID
        sql = """SELECT id, name, surname, tax_id 
                 FROM customer 
                 WHERE name LIKE ? 
                    OR surname LIKE ? 
                    OR id LIKE ? 
                 LIMIT 20"""
        search_pattern = f"%{q}%"
        val = (search_pattern, search_pattern, search_pattern)
        cursor.execute(sql, val)
        for row in cursor:
            c_id = row[0]
            c_name = row[1]
            c_surname = row[2] if row[2] else "" # กันค่า NULL
            c_tax_id = row[3] if row[3] else "-"
            results.append({
                "id": c_id,
                "name": c_name,
                "surname": c_surname,
                "tax_id": c_tax_id,
                "display_text": f"{c_id} : {c_name} {c_surname} {c_tax_id}" # จัด Format ให้สวยงาม
            })
    except mariadb.Error as e:
        print(f"Query Error: {e}")
    finally:
        conn.close()
    return results
# --- Customer Search API ---


# --- ADD NEW CUSTOMER API ---
class NewCustomer(BaseModel):
    group_id: Optional[str] = ""
    title_name: Optional[str] = ""
    name: Optional[str] = ""
    mid_name: Optional[str] = ""
    surname: Optional[str] = ""
    tax_id: Optional[str] = ""
    phone: Optional[str] = ""
    email: Optional[str] = ""
    line_ID: Optional[str] = ""
    address: Optional[str] = ""
    bill_address: Optional[str] = ""
@app.post("/add_customer")
def add_customer(customer: NewCustomer):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        sql = """INSERT INTO customer (group_id, title, name, surname, tax_id, email, line_id, phone, contact_address, bill_address)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        val = (customer.group_id, customer.title_name, customer.name, customer.surname, customer.tax_id,
               customer.email, customer.line_ID, customer.phone, customer.address, customer.bill_address)
        cursor.execute(sql, val)
        conn.commit()
        
        return {"status": "success", "customer_id": cursor.lastrowid}
    except mariadb.Error as e:
        print(f"Insert Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to add customer")
    finally:
        conn.close()
@app.get("/get_customer_group_id")
def get_customer_group_id():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM customer_group ")
        groups = [{"id": row[0], "group_name": row[1]} for row in cursor]
        return {"customer_groups": groups}
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve customer groups")
# --- ADD NEW CUSTOMER API ---

# --- ADD NEW WORK API ---
@app.get("/get_max_sample_id")
def get_max_sample_id():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) AS last_case_number FROM case_registration")
        max_id = cursor.fetchone()
        return {"max_id": max_id[0] if max_id and max_id[0] is not None else 0}
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve max sample ID")
    finally:
        conn.close()

@app.post("/add_new_work")
def add_work(
    sender_id: Optional[int] = None, 
    owner_id: Optional[int] = None, 
    project_name: Optional[str] = "", 
    updater: Optional[int] = None ):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        pass
        # cursor = conn.cursor()
        # sql = """INSERT INTO work (title, description, owner_id, created_at)
        #          VALUES (?, ?, ?, ?)"""
        # val = (work.title, work.description, work.owner_id, datetime.now())
        # cursor.execute(sql, val)
        # conn.commit()
        # return {"status": "success", "work_id": cursor.lastrowid}
        if sender_id is None:
            raise HTTPException(status_code=422, detail="sender_id is required")
        if owner_id is None:
            raise HTTPException(status_code=422, detail="owner_id is required")
        project_name = project_name if project_name else ""
        
        cursor = conn.cursor()
        sql = """INSERT INTO case_registration (sender_id, owner_id, project_name, updater) VALUES (?, ?, ?, ?)"""
        val = (sender_id, owner_id, project_name, updater)
        cursor.execute(sql, val)
        conn.commit()
        work_id = cursor.lastrowid
        
        return {"status": "success", "work_id": work_id}
    
    except mariadb.Error as e:
        print(f"❌ Insert Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add work: {str(e)}")
    finally:
        conn.close()

# --- SPECIMEN REGISTRATION API ---

@app.post("/add_new_specimen")
def add_new_specimen(data: SpecimenData):
    """Add new specimen/sample registration"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        
        # Prepare SQL with all fields
        sql = """INSERT INTO sample_registration 
        (case_id, name, opd_number, sex, age_year, age_month, age_day, demise, 
         species, breed, sample_type, weight, dead_date, collect_date, 
         keep_method, speed, medical_record, dosage_record, sample_inspection, updater)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        val = (
            data.case_id,
            data.name,
            data.opd_number,
            data.sex,
            data.age_year,
            data.age_month,
            data.age_day,
            data.demise,
            data.species,
            data.breed,
            data.sample_type,
            data.weight,
            data.dead_date,
            data.collect_date,
            data.keep_method,
            data.speed,
            data.medical_record,
            data.dosage_record,
            data.sample_inspection,
            data.updater
        )
        
        cursor.execute(sql, val)
        conn.commit()
        specimen_id = cursor.lastrowid
        
        return {"status": "success", "specimen_id": specimen_id}
    
    except mariadb.Error as e:
        print(f"❌ Specimen Insert Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add specimen: {str(e)}")
    finally:
        conn.close()

# --- ROOM INFORMATION API ---

@app.get("/get_room_details")
def get_room_details():
    """Get all active lab room details"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, code, name, thai_name, nickname FROM room_information WHERE status = 1")
        rooms = [{"id": row[0], "code": row[1], "name": row[2], "thai_name": row[3], "nickname": row[4]} for row in cursor]
        return {"lab_rooms": rooms}
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve lab rooms")
    finally:
        conn.close()


# --- BARCODE / STICKER API ---

@app.get("/barcode/today")
def get_today_cases():
    """ Get all cases registered today """
    conn = None
    try:
        conn = get_db_connection()
        if not conn: 
            return []
        
        cursor = conn.cursor()
        cursor.execute("SELECT id, code, name, thai_name, nickname FROM room_information WHERE status = 1")
        rooms = [{"id": row[0], "code": row[1], "name": row[2], "thai_name": row[3], "nickname": row[4]} for row in cursor]
        return {"lab_rooms": rooms}
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve lab rooms")
    finally:
        conn.close()


# --- ADD NEW LAB ORDER API ---
class LabOrder(BaseModel):
    sample_id: Optional[str] = ""
    room_id: Optional[str] = None
    comments: Optional[str] = ""
    state: Optional[str] = "0"
    status: Optional[str] = "1"
    updater: Optional[int] = None  # user_id of person saving the data

@app.post("/add_new_lab_order")
def add_lab_order(lab_order: LabOrder):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lab_order (sample_id, room_id, comments, state, status, updater) VALUES (?, ?, ?, ?, ?, ?)", (lab_order.sample_id, lab_order.room_id, lab_order.comments, lab_order.state, lab_order.status, lab_order.updater))
        conn.commit()
        return {"status": "success", "sample_id": lab_order.sample_id}
    
    except mariadb.Error as e:
        print(f"Insert Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add sample ID: {str(e)}")
    finally:
        conn.close()

# --- ADD NEW LAB ID API ---

# --- UPDATE TRACKING LAB ORDER API ---

class update_tracking_LabOrder(BaseModel):
    lab_order_id: Optional[str] = ""
    tracking_info: Optional[str] = "รับงานเข้าระบบ"
    receiver: Optional[str] = None
    updater: Optional[str] = None
    
@app.post("/update_tracking_lab_order")
def update_tracking_lab_order(lab_order: update_tracking_LabOrder):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tracking_lab_order (lab_order_id, tracking_info, receiver, updater) VALUES (?, ?, ?, ?)", (lab_order.lab_order_id, lab_order.tracking_info, lab_order.receiver, lab_order.updater))
        conn.commit()
        return {"status": "success", "lab_order_id": lab_order.lab_order_id}
    
    except mariadb.Error as e:
        print(f"Insert Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add lab order ID: {str(e)}")
    finally:
        conn.close()

# --- UPDATE TRACKING LAB ORDER API ---

# --- UPDATE CASE DETAILS API ---

@app.get("/get_case_details/{case_id}")
def get_case_details(case_id: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT lab_order.dtime, lab_order.id, sample_registration.species, room_information.code, room_information.nickname, sample_registration.keep_method, sample_registration.speed FROM case_registration LEFT JOIN sample_registration ON case_registration.id = sample_registration.case_id RIGHT JOIN lab_order ON sample_registration.id = lab_order.sample_id LEFT JOIN room_information ON lab_order.room_id = room_information.id WHERE case_registration.id = %s AND lab_order.status = 1", (case_id,))
        result = cursor.fetchall()
        return {"status": "success", "case_id": case_id, "data": result}
    except mariadb.Error as e:
        print(f"Update Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update case details: {str(e)}")
    finally:
        conn.close()

# --- UPDATE CASE DETAILS API ---

# --- MOLECULAR BIOLOGY API ---

@app.post("/save_molecular_biology")
def save_molecular_biology(data: MolecularBiologyData):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        
        # Prepare data for 61 test slots (test1-test61)
        test_data = []
        for i in range(1, 62):  # 61 tests
            if i <= len(data.tests):
                test = data.tests[i-1]
                test_data.extend([
                    test.get('name', ''),
                    test.get('quantity', 0),
                    test.get('total_price', 0)
                ])
            else:
                test_data.extend(['', 0, 0])  # Empty test slot
                
        # Total columns: 1 (sample_id) + 183 (61 tests * 3 fields) + 4 (metadata) = 188
        sql = """INSERT INTO lab_molecular_biology 
        (sample_id, test1_name, test1_amount, test1_price, test2_name, test2_amount, test2_price, 
        test3_name, test3_amount, test3_price, test4_name, test4_amount, test4_price, 
        test5_name, test5_amount, test5_price, test6_name, test6_amount, test6_price, 
        test7_name, test7_amount, test7_price, test8_name, test8_amount, test8_price, 
        test9_name, test9_amount, test9_price, test10_name, test10_amount, test10_price, 
        test11_name, test11_amount, test11_price, test12_name, test12_amount, test12_price, 
        test13_name, test13_amount, test13_price, test14_name, test14_amount, test14_price, 
        test15_name, test15_amount, test15_price, test16_name, test16_amount, test16_price, 
        test17_name, test17_amount, test17_price, test18_name, test18_amount, test18_price, 
        test19_name, test19_amount, test19_price, test20_name, test20_amount, test20_price, 
        test21_name, test21_amount, test21_price, test22_name, test22_amount, test22_price, 
        test23_name, test23_amount, test23_price, test24_name, test24_amount, test24_price, 
        test25_name, test25_amount, test25_price, test26_name, test26_amount, test26_price, 
        test27_name, test27_amount, test27_price, test28_name, test28_amount, test28_price, 
        test29_name, test29_amount, test29_price, test30_name, test30_amount, test30_price, 
        test31_name, test31_amount, test31_price, test32_name, test32_amount, test32_price, 
        test33_name, test33_amount, test33_price, test34_name, test34_amount, test34_price, 
        test35_name, test35_amount, test35_price, test36_name, test36_amount, test36_price, 
        test37_name, test37_amount, test37_price, test38_name, test38_amount, test38_price, 
        test39_name, test39_amount, test39_price, test40_name, test40_amount, test40_price, 
        test41_name, test41_amount, test41_price, test42_name, test42_amount, test42_price, 
        test43_name, test43_amount, test43_price, test44_name, test44_amount, test44_price, 
        test45_name, test45_amount, test45_price, test46_name, test46_amount, test46_price, 
        test47_name, test47_amount, test47_price, test48_name, test48_amount, test48_price, 
        test49_name, test49_amount, test49_price, test50_name, test50_amount, test50_price, 
        test51_name, test51_amount, test51_price, test52_name, test52_amount, test52_price, 
        test53_name, test53_amount, test53_price, test54_name, test54_amount, test54_price, 
        test55_name, test55_amount, test55_price, test56_name, test56_amount, test56_price, 
        test57_name, test57_amount, test57_price, test58_name, test58_amount, test58_price, 
        test59_name, test59_amount, test59_price, test60_name, test60_amount, test60_price, 
        test61_name, test61_amount, test61_price, cPCR_req, qPCR_req, extraction_req, updater) 
        VALUES (""" + ",".join(["?"] * 188) + ")"
        
        # Prepare parameters: sample_id + test_data + metadata
        params = [data.sample_id] + test_data + [
            data.cPCR_req, 
            data.qPCR_req, 
            data.extraction_req, 
            data.updater
        ]
        
        if len(params) != 188:
            raise ValueError(f"Parameter mismatch: Expected 188, got {len(params)}")
        
        # Execute query
        cursor.execute(sql, params)
        conn.commit()
        
        return {
            "status": "success",
            "message": "Molecular biology data saved successfully",
            "sample_id": data.sample_id,
            "tests_count": len(data.tests)
        }
        
    except mariadb.Error as e:
        print(f"Database Error: {e}")
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save molecular biology data: {str(e)}")
    finally:
        conn.close()
        
# --- MOLECULAR BIOLOGY API ---

# --- PARASITE BIOLOGY API ---

@app.post("/save_parasite_biology")
def save_parasite_biology(data: ParasiteBiologyData):
    """Save parasite biology test data to database"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        test_data = []
        for i in range(1, 13):  # 12 tests for parasite
            if i <= len(data.tests):
                test = data.tests[i-1]
                name_with_price = test.get('name', '')  # Already includes price
                quantity = test.get('quantity', 0)
                price = test.get('price', 0)
                
                test_data.extend([
                    name_with_price,  
                    quantity,         
                    price             
                ])
            else:
                test_data.extend(['', 0, 0])  # Empty test slot
        sql = """INSERT INTO lab_parasite_biology 
        (sample_id, t1_name, t1_state, t1_price, t2_name, t2_state, t2_price, 
         t3_name, t3_state, t3_price, t4_name, t4_state, t4_price, 
         t5_name, t5_state, t5_price, t6_name, t6_state, t6_price, 
         t7_name, t7_state, t7_price, t8_name, t8_state, t8_price, 
         t9_name, t9_state, t9_price, t10_name, t10_state, t10_price, 
         t11_name, t11_state, t11_price, t12_name, t12_state, t12_price, updater) 
        VALUES (""" + ",".join(["?"] * 38) + ")"
        
        params = [data.sample_id] + test_data + [data.updater]
        
        # Validate parameter count
        if len(params) != 38:
            raise ValueError(f"Parameter mismatch: Expected 38, got {len(params)}")
        
        cursor.execute(sql, params)
        conn.commit()
        
        return {
            "status": "success",
            "message": "Parasite biology data saved successfully",
            "sample_id": data.sample_id,
            "tests_count": len(data.tests)
        }
        
    except mariadb.Error as e:
        print(f"❌ Parasite Biology Database Error: {e}")
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save parasite biology data: {str(e)}")
    except ValueError as e:
        print(f"❌ Parasite Biology Validation Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# --- PARASITE BIOLOGY API ---

# --- EMPLOYEE MANAGEMENT API ---

@app.get("/search_employee")
def search_employee(q: str):
    """Search employee by name or surname"""
    if not q or len(q) < 2:
        return []
    
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        sql = """SELECT e.id, e.title, e.name, e.surname, e.email, e.username, e.group_id, eg.name as position
                 FROM employee e
                 LEFT JOIN employee_group eg ON e.group_id = eg.id
                 WHERE e.name LIKE ? OR e.surname LIKE ?
                 ORDER BY e.name
                 LIMIT 20"""
        search_pattern = f"%{q}%"
        cursor.execute(sql, (search_pattern, search_pattern))
        
        employees = []
        for row in cursor:
            employees.append({
                "id": row[0],
                "title": row[1] if row[1] else "",
                "name": row[2] if row[2] else "",
                "surname": row[3] if row[3] else "",
                "email": row[4] if row[4] else "",
                "username": row[5] if row[5] else "",
                "group_id": row[6] if row[6] is not None else None,
                "position": row[7] if row[7] else ""
            })
        
        return {"employees": employees}
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to search employee")
    finally:
        conn.close()

@app.get("/get_employee/{employee_id}")
def get_employee(employee_id: int):
    """Get employee details by ID"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        sql = """SELECT e.id, e.title, e.name, e.surname, e.email, e.username, e.group_id, eg.name as position
                 FROM employee e
                 LEFT JOIN employee_group eg ON e.group_id = eg.id
                 WHERE e.id = ?"""
        cursor.execute(sql, (employee_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return {
            "id": row[0],
            "title": row[1] if row[1] else "",
            "name": row[2] if row[2] else "",
            "surname": row[3] if row[3] else "",
            "email": row[4] if row[4] else "",
            "username": row[5] if row[5] else "",
            "group_id": row[6] if row[6] else None,
            "position": row[7] if row[7] else ""
        }
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get employee")
    finally:
        conn.close()

class EmployeeData(BaseModel):
    title: Optional[str] = ""
    name: Optional[str] = ""
    surname: Optional[str] = ""
    email: Optional[str] = ""
    username: Optional[str] = ""
    password: Optional[str] = None
    group_id: Optional[int] = None
    signature_base64: Optional[str] = None  # Base64 encoded signature image

@app.post("/create_employee")
def create_employee(employee: EmployeeData):
    """Create new employee"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT id FROM employee WHERE username = ?", (employee.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Hash password
        password_to_hash = employee.password[:72] if employee.password else ""
        hashed_password = pwd_context.hash(password_to_hash)
        
        sql = """INSERT INTO employee 
                 (title, name, surname, email, username, password, group_id)
                 VALUES (?, ?, ?, ?, ?, ?, ?)"""
        
        cursor.execute(sql, (
            employee.title,
            employee.name,
            employee.surname,
            employee.email,
            employee.username,
            hashed_password,
            employee.group_id
        ))
        
        employee_id = cursor.lastrowid
        
        # Save signature image if provided
        if employee.signature_base64:
            save_signature_to_file(employee.username, employee.signature_base64)
        
        conn.commit()
        return {"status": "success", "employee_id": employee_id}
        
    except mariadb.Error as e:
        print(f"Insert Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create employee")
    finally:
        conn.close()

@app.put("/update_employee/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeData):
    """Update employee data"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # First check if employee exists
        print(f"Checking if employee {employee_id} exists...")
        cursor.execute("SELECT username FROM employee WHERE id = ?", (employee_id,))
        result = cursor.fetchone()
        if not result:
            print(f"Employee {employee_id} not found in database")
            raise HTTPException(status_code=404, detail="Employee not found")
        
        old_username = result[0]
        
        # Check if username exists for other employees
        cursor.execute("SELECT id FROM employee WHERE username = ? AND id != ?", 
                      (employee.username, employee_id))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")
        
        print(f"Updating employee {employee_id}: {employee.dict()}")
        sql = """UPDATE employee 
                 SET title=?, name=?, surname=?, email=?, username=?, group_id=?
                 WHERE id=?"""
        
        cursor.execute(sql, (
            employee.title,
            employee.name,
            employee.surname,
            employee.email,
            employee.username,
            employee.group_id,
            employee_id
        ))
        
        # Save signature image if provided
        if employee.signature_base64:
            save_signature_to_file(employee.username, employee.signature_base64)
        
        conn.commit()
        print(f"Employee {employee_id} updated successfully. Rows affected: {cursor.rowcount}")
        
        return {"status": "success", "employee_id": employee_id}
        
    except HTTPException:
        raise
    except mariadb.Error as e:
        print(f"Update Error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        conn.close()

@app.get("/get_employee_groups")
def get_employee_groups():
    """Get all employee groups/positions"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM employee_group ORDER BY name")
        groups = [{"id": row[0], "name": row[1]} for row in cursor]
        return {"employee_groups": groups}
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get employee groups")
    finally:
        conn.close()

@app.delete("/delete_employee/{employee_id}")
def delete_employee(employee_id: int):
    """Delete employee"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # Get username before deleting
        cursor.execute("SELECT username FROM employee WHERE id = ?", (employee_id,))
        result = cursor.fetchone()
        if result:
            username = result[0]
            # Delete signature files for this user
            delete_signature_files(username)
        
        cursor.execute("DELETE FROM employee WHERE id = ?", (employee_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return {"status": "success", "message": "Employee deleted"}
        
    except mariadb.Error as e:
        print(f"Delete Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete employee")
    finally:
        conn.close()

@app.get("/get_signature/{username}")
def get_signature(username: str):
    """Get the latest signature image for a username as base64"""
    try:
        signatures_dir = "signatures"
        if not os.path.exists(signatures_dir):
            return {"signature_base64": None}
        
        # Find all signature files for this username
        matching_files = []
        for filename in os.listdir(signatures_dir):
            if f"signature_{username}_" in filename and filename.endswith('.png'):
                filepath = os.path.join(signatures_dir, filename)
                matching_files.append((filepath, os.path.getmtime(filepath)))
        
        if not matching_files:
            return {"signature_base64": None}
        
        # Get the newest file
        matching_files.sort(key=lambda x: x[1], reverse=True)
        newest_file = matching_files[0][0]
        
        # Read and encode to base64
        with open(newest_file, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            return {"signature_base64": base64_data}
            
    except Exception as e:
        print(f"Error getting signature: {e}")
        return {"signature_base64": None}

# Helper functions for signature management
def save_signature_to_file(username: str, base64_data: str):
    """Save base64 encoded signature to file"""
    try:
        signatures_dir = "signatures"
        if not os.path.exists(signatures_dir):
            os.makedirs(signatures_dir)
        
        # Decode base64 to bytes
        image_data = base64.b64decode(base64_data)
        
        # Generate filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"signature_{username}_{timestamp}.png"
        filepath = os.path.join(signatures_dir, filename)
        
        # Save to file
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        print(f"Signature saved: {filepath}")
        return filepath
    except Exception as e:
        print(f"Error saving signature: {e}")
        return None

def delete_signature_files(username: str):
    """Delete all signature files for a username"""
    try:
        signatures_dir = "signatures"
        if not os.path.exists(signatures_dir):
            return
        
        for filename in os.listdir(signatures_dir):
            if f"signature_{username}_" in filename and filename.endswith('.png'):
                filepath = os.path.join(signatures_dir, filename)
                os.remove(filepath)
                print(f"Deleted signature: {filepath}")
    except Exception as e:
        print(f"Error deleting signatures: {e}")

# --- EMPLOYEE MANAGEMENT API ---


# --- BARCODE / STICKER API ---

@app.get("/barcode/today")
def get_today_cases():
    """ Get all cases registered today """
    conn = None
    try:
        conn = get_db_connection()
        if not conn: 
            return []
        
        cursor = conn.cursor()
        
        # Query based on sample_registration.dtime (today's samples)
        sql = """
            SELECT 
                s.dtime, 
                s.case_id, 
                s.species, 
                CONCAT(IFNULL(r.code, ''), '(', IFNULL(r.nickname, ''), ')') AS lab_name,
                s.keep_method, 
                s.speed,
                s.room AS room_debug
            FROM sample_registration s
            LEFT JOIN room_information r ON s.room = r.code
            WHERE DATE(s.dtime) = CURDATE()
            ORDER BY s.dtime DESC
        """
        cursor.execute(sql)
        results = []
        for row in cursor:
            print(f"[DEBUG] room value: {row[6]}, lab_name: {row[3]}")
            results.append({
                "date": str(row[0]) if row[0] else None,
                "barcode": row[1],
                "species": row[2],
                "lab_name": row[3],
                "storage": row[4],
                "urgency": row[5]
            })
        
        # If no data today, get all recent data (last 100 records)
        if len(results) == 0:
            print("No data for today, fetching all recent records...")
            sql_all = """
                SELECT 
                    s.dtime, 
                    s.case_id, 
                    s.species, 
                    CONCAT(IFNULL(r.code, ''), '(', IFNULL(r.nickname, ''), ')') AS lab_name,
                    s.keep_method, 
                    s.speed,
                    s.room AS room_debug
                FROM sample_registration s
                LEFT JOIN room_information r ON s.room = r.code
                ORDER BY s.dtime DESC
                LIMIT 100
            """
            cursor.execute(sql_all)
            for row in cursor:
                print(f"[DEBUG] room value: {row[6]}, lab_name: {row[3]}")
                results.append({
                    "date": str(row[0]) if row[0] else None,
                    "barcode": row[1],
                    "species": row[2],
                    "lab_name": row[3],
                    "storage": row[4],
                    "urgency": row[5]
                })
        
        print(f"Returning {len(results)} records")
        return results
    except mariadb.Error as e:
        print(f"Query Error (Today): {e}")
        return []
    finally:
        if conn: 
            conn.close()

@app.get("/barcode/search")
def search_barcode_cases(name: str = "", surname: str = ""):
    """ Search cases by Customer Name/Surname """
    conn = None
    try:
        conn = get_db_connection()
        if not conn: 
            return []
        
        cursor = conn.cursor()
        
        # Build dynamic WHERE clause based on provided parameters
        conditions = []
        params = []
        
        # Clean up the name - if it contains surname, extract just the first name
        search_name = name.strip() if name else ""
        search_surname = surname.strip() if surname else ""
        
        # If name contains the surname (e.g., "พนม แซ่ลี"), extract just the first part
        if search_name and search_surname and search_surname in search_name:
            search_name = search_name.replace(search_surname, "").strip()
        
        print(f"[DEBUG] Cleaned search: name='{search_name}', surname='{search_surname}'")
        
        if search_name:
            conditions.append("cust.name LIKE ?")
            params.append(f"%{search_name}%")
        
        if search_surname:
            conditions.append("cust.surname LIKE ?")
            params.append(f"%{search_surname}%")

        # If no search criteria provided, return empty
        if not conditions:
            return []
        
        # Use AND to match both name AND surname if both provided
        where_clause = " AND ".join(conditions)
        
        # Debug: Print customer IDs that match the search criteria
        print("=" * 50)
        print(f"[SEARCH] Name: '{name}', Surname: '{surname}'")
        debug_sql = f"""
            SELECT DISTINCT cust.id, cust.name, cust.surname
            FROM customer cust
            WHERE {where_clause}
        """
        cursor.execute(debug_sql, tuple(params))
        debug_rows = cursor.fetchall()
        print(f"[DEBUG] Found {len(debug_rows)} matching customers:")
        for row in debug_rows:
            print(f"  - ID: {row[0]}, Name: {row[1]} {row[2]}")
        print("=" * 50)
        
        # Search by both owner_id and sender_id
        # Use DISTINCT to avoid duplicates from owner_id/sender_id OR condition
        sql = f"""
            SELECT DISTINCT
                s.id AS sample_id,
                s.dtime, 
                s.case_id, 
                s.name AS sample_name,
                s.species, 
                CONCAT(IFNULL(r.code, ''), '(', IFNULL(r.nickname, ''), ')') AS lab_name,
                s.keep_method, 
                s.speed 
            FROM sample_registration s
            LEFT JOIN case_registration c ON s.case_id = c.id
            LEFT JOIN customer cust ON (c.owner_id = cust.id OR c.sender_id = cust.id)
            LEFT JOIN room_information r ON s.room = r.code
            WHERE {where_clause}
            ORDER BY s.dtime DESC, s.id
        """
        print(f"[DEBUG] Search SQL params: {params}")
        cursor.execute(sql, tuple(params))
        results = []
        seen_sample_ids = set()
        for row in cursor:
            sample_id = row[0]
            # Skip if we've already seen this sample
            if sample_id in seen_sample_ids:
                continue
            seen_sample_ids.add(sample_id)
            
            results.append({
                "date": str(row[1]) if row[1] else None,
                "barcode": row[2],
                "sample_name": row[3],
                "species": row[4],
                "lab_name": row[5],
                "storage": row[6],
                "urgency": row[7]
            })
        print(f"[DEBUG] Search returned {len(results)} results")
        return results
    except mariadb.Error as e:
        print(f"Query Error (Search): {e}")
        return []
    finally:
        if conn: 
            conn.close()


# print("Server Running ...")

# สั่ง ในขั้นตอน Production : python -m uvicorn server_api:app --host 0.0.0.0 --port 8000 --reload --log-level warning

# สั่ง ในขั้นตอน debug : python -m uvicorn server_api:app --host 0.0.0.0 --port 8000 --reload --log-level debug