from fastapi import FastAPI, HTTPException
import mariadb
from pydantic import BaseModel
from typing import List, Optional
from passlib.context import CryptContext
import base64
import os

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# DB_CONFIG = {
#     "host": "202.28.24.55",
#     "user": "python_engine",
#     "password": "c#@4573kt",
#     "database": "cvdtt_lab",
#     "port": 3306
# }

#  MARK: - Local DB Config
# DB_CONFIG = {
#     "host": "127.0.0.1",
#     "user": "root",
#     "password": "",
#     "database": "testdb",
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
        cursor.execute("SELECT id, password FROM employee WHERE username = ? LIMIT 1", (username,))
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
def add_work(sender_id: int, owner_id: int, project_name: str, updater: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        sql = """INSERT INTO case_registration (sender_id, owner_id, project_name, updater) VALUES (?, ?, ?, ?)"""
        val = (sender_id, owner_id, project_name, updater,)
        cursor.execute(sql, val)
        conn.commit()
        return {"status": "success", "work_id": cursor.lastrowid}
    
    except mariadb.Error as e:
        print(f"Insert Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to add work")
    finally:
        conn.close()
# --- ADD NEW WORK API ---


# --- ADD NEW SPECIMEN API ---
class NewSpecimen(BaseModel):
    case_id: Optional[int] = None  # Optional
    name: Optional[str] = ""  # Optional
    opd_number: Optional[str] = ""
    sex: Optional[str] = ""
    age_year: Optional[int] = 0  # Default: 0
    age_month: Optional[int] = 0  # Default: 0
    age_day: Optional[int] = 0  # Default: 0
    demise: Optional[str] = ""
    species: str  # REQUIRED - ชนิดสัตว์
    breed: Optional[str] = ""
    sample_type: Optional[str] = ""
    weight: Optional[float] = 0.0  # Default: 0.0
    dead_date: Optional[str] = None
    collect_date: Optional[str] = None
    keep_method: Optional[str] = ""
    speed: Optional[str] = ""
    medical_record: Optional[str] = ""
    dosage_record: Optional[str] = ""
    sample_inspection: Optional[str] = ""
    updater: Optional[int] = None
    other_details: Optional[str] = ""

@app.post("/add_new_specimen")
def add_specimen(specimen: NewSpecimen):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        val = (
            specimen.case_id if specimen.case_id is not None else 0,
            specimen.name or "",
            specimen.opd_number or "",
            specimen.sex or "",
            specimen.age_year if specimen.age_year is not None else 0,
            specimen.age_month if specimen.age_month is not None else 0,
            specimen.age_day if specimen.age_day is not None else 0,
            specimen.demise or "",
            specimen.species,  # REQUIRED
            specimen.breed or "",
            specimen.sample_type or "",
            specimen.weight if specimen.weight is not None else 0.0,
            specimen.dead_date,  # Can be NULL
            specimen.collect_date,  # Can be NULL
            specimen.keep_method or "",
            specimen.speed or "",
            specimen.medical_record or "",
            specimen.dosage_record or "",
            specimen.sample_inspection or "",
            specimen.updater  # Can be NULL
        )
        sql = """INSERT INTO sample_registration (
                    case_id, name, opd_number, sex, age_year, age_month, age_day,
                    demise, species, breed, sample_type, weight, dead_date, collect_date,
                    keep_method, speed, medical_record, dosage_record, sample_inspection,
                    updater
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        cursor.execute(sql, val)
        conn.commit()
        return {"status": "success", "specimen_id": cursor.lastrowid}
    except mariadb.Error as e:
        print(f"Insert Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add specimen: {str(e)}")
    finally:
        conn.close()
        

@app.get("/get_room_details")
def get_room_id_and_details():
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


# --- ADD NEW SPECIMEN API ---




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

# --- ADD NEW WORK API ---

# print("Server Running ...")

# สั่ง ในขั้นตอน Production : python -m uvicorn server_api:app --host 0.0.0.0 --port 8000 --reload --log-level warning

# สั่ง ในขั้นตอน debug : python -m uvicorn server_api:app --host 0.0.0.0 --port 8000 --reload --log-level debug