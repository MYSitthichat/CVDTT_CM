# routers/employee.py
from fastapi import APIRouter, HTTPException
from typing import Optional
import mariadb
import os
import base64
from database import get_db_connection
from security import pwd_context
from schemas import EmployeeData

router = APIRouter(tags=["Employee"])

# ... (ฟังก์ชันอื่นๆ: update_employee, delete_employee, get_signature, save_signature_to_file ให้ใส่ที่นี่ โดยอิงจาก logic เดิม)
# หมายเหตุ: เพื่อความกระชับ ผมไม่ได้วาง update_employee/delete_employee ทั้งหมด แต่คุณสามารถ copy จาก server_api.py มาแปะต่อได้เลย
# โดยเปลี่ยนแค่ pwd_context และการเรียก DB ให้เหมือนข้างบน

@router.get("/search_employee")
def search_employee(q: str, current_username: str = None):
    if not q or len(q) < 2:
        return []
    
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        if current_username:
            # Include active employees + current user's latest record (even if archived)
            sql = """SELECT e.id, e.title, e.name, e.surname, e.email, e.username, e.group_id, eg.name as position
                     FROM employee e
                     LEFT JOIN employee_group eg ON e.group_id = eg.id
                     WHERE (e.name LIKE ? OR e.surname LIKE ?) 
                     AND (e.status = 1 OR (e.username = ? AND e.id = (
                         SELECT MAX(id) FROM employee WHERE username = ?
                     )))
                     ORDER BY e.name
                     LIMIT 20"""
            search_pattern = f"%{q}%"
            cursor.execute(sql, (search_pattern, search_pattern, current_username, current_username))
        else:
            # Only active employees
            sql = """SELECT e.id, e.title, e.name, e.surname, e.email, e.username, e.group_id, eg.name as position
                     FROM employee e
                     LEFT JOIN employee_group eg ON e.group_id = eg.id
                     WHERE (e.name LIKE ? OR e.surname LIKE ?) AND e.status = 1
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

@router.get("/get_employee/{employee_id}")
def get_employee(employee_id: int, include_archived: bool = False):
    """Get employee details by ID
    
    Args:
        employee_id: The employee ID
        include_archived: If True, includes archived employees (status=0)
    """
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        if include_archived:
            # No status filter - allows getting archived employees
            sql = """SELECT e.id, e.title, e.name, e.surname, e.email, e.username, e.group_id, eg.name as position
                     FROM employee e
                     LEFT JOIN employee_group eg ON e.group_id = eg.id
                     WHERE e.id = ?"""
        else:
            # Only active employees
            sql = """SELECT e.id, e.title, e.name, e.surname, e.email, e.username, e.group_id, eg.name as position
                     FROM employee e
                     LEFT JOIN employee_group eg ON e.group_id = eg.id
                     WHERE e.id = ? AND e.status = 1"""
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

@router.get("/get_employee_permission/{employee_id}")
def get_employee_permission(employee_id: int):
    """Get employee permission (group_id) - NO status filter for archived users"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        # NO status filter - allows getting permission for archived users
        sql = """SELECT group_id FROM employee WHERE id = ? ORDER BY id DESC LIMIT 1"""
        cursor.execute(sql, (employee_id,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return {"group_id": result[0]}
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get employee permission")
    finally:
        conn.close()

@router.post("/create_employee")
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
        
        # print(f"[API DEBUG] create_employee - Received updater: {employee.updater}")
        # print(f"[API DEBUG] create_employee - Will save updater: {employee.updater if employee.updater is not None else 1}")
        
        sql = """INSERT INTO employee 
                 (title, name, surname, email, username, password, group_id, status, updater)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        cursor.execute(sql, (
            employee.title,
            employee.name,
            employee.surname,
            employee.email,
            employee.username,
            hashed_password,
            employee.group_id,
            employee.status if employee.status is not None else 1,
            employee.updater if employee.updater is not None else 1
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

@router.put("/update_employee/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeData):
    """Update employee data with version history
    1. Archives old record by setting status=0 and updater
    2. Inserts new record with updated data, status=1 and updater
    """
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # Get the most recent record for this employee (regardless of status)
        # This allows updating archived employees
        cursor.execute("""
            SELECT username, password, status 
            FROM employee 
            WHERE id = ? 
            ORDER BY dtime DESC 
            LIMIT 1
        """, (employee_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        old_username = result[0]
        old_password = result[1]
        old_status = result[2]
        
        # Check if username exists for other employees (excluding this employee's records)
        cursor.execute("""
            SELECT e.id 
            FROM employee e
            WHERE e.username = ? 
            AND e.id != ?
            AND e.status = 1
        """, (employee.username, employee_id))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # print(f"[API DEBUG] update_employee - Received updater: {employee.updater}")
        # print(f"[API DEBUG] update_employee - Will save updater: {employee.updater if employee.updater is not None else 1}")
        
        # Step 1: Archive old record (set status=0 and update updater)
        cursor.execute(
            "UPDATE employee SET status = 0, updater = ? WHERE id = ?",
            (employee.updater if employee.updater is not None else 1, employee_id)
        )
        
        # Step 2: Insert new record with updated data
        # If new password provided, hash it; otherwise keep old password
        password_to_save = old_password  # Default: keep old password
        if employee.password:
            # Hash the new password
            password_to_save = pwd_context.hash(employee.password)
            # print(f"[API DEBUG] New password provided, hashing it")
        else:
            # print(f"[API DEBUG] No new password, keeping old password")
            pass
        
        sql = """INSERT INTO employee 
                 (title, name, surname, email, username, password, group_id, status, updater)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        cursor.execute(sql, (
            employee.title,
            employee.name,
            employee.surname,
            employee.email,
            employee.username,
            password_to_save,  # Use new password if provided, else old password
            employee.group_id,
            1,  # New record is active
            employee.updater if employee.updater is not None else 1
        ))
        
        new_employee_id = cursor.lastrowid
        
        # Save signature image if provided
        if employee.signature_base64:
            save_signature_to_file(employee.username, employee.signature_base64)
        
        conn.commit()
        
        return {"status": "success", "employee_id": new_employee_id, "old_employee_id": employee_id}
        
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

@router.get("/get_employee_groups")
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

@router.delete("/delete_employee/{employee_id}")
def delete_employee(employee_id: int, updater: Optional[int] = None):
    """Soft delete employee by setting status=0 and tracking who deleted it"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # Check if employee exists and is active
        cursor.execute("SELECT id FROM employee WHERE id = ? AND status = 1", (employee_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Employee not found or already deleted")
        
        # Soft delete: set status=0 and update updater field
        cursor.execute(
            "UPDATE employee SET status = 0, updater = ? WHERE id = ?",
            (updater if updater is not None else 1, employee_id)
        )
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return {"status": "success", "message": "Employee deleted (soft delete)"}
        
    except mariadb.Error as e:
        print(f"Delete Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete employee")
    finally:
        conn.close()

@router.get("/get_signature/{username}")
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

