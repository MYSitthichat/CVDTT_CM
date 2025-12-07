# routers/auth.py
from fastapi import APIRouter, HTTPException
import mariadb
from database import get_db_connection
from security import pwd_context

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(username: str, password: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT id, password, group_id 
                    FROM employee 
                    WHERE username = ?
                    AND status = 1
                    ORDER BY id DESC 
                    LIMIT 1
        """, (username,))
        user = cursor.fetchone()
        if not user:
            return {"success": False, "user_id": None, "group_id": None}
        
        user_id = user[0]
        stored_password = user[1]
        group_id = user[2]
        password_to_verify = password[:72]
        
        if stored_password.startswith("$2b$"):
            try:
                is_valid = pwd_context.verify(password_to_verify, stored_password)
                return {"success": is_valid, "user_id": user_id if is_valid else None, "group_id": group_id if is_valid else None}
            except Exception as e:
                print(f"Password verification error: {e}")
                return {"success": False, "user_id": None, "group_id": None}
        else:
            if password != stored_password:
                return {"success": False, "user_id": None, "group_id": None}
            try:
                new_hashed = pwd_context.hash(password_to_verify)
                cursor.execute("UPDATE employee SET password = ? WHERE id = ?", (new_hashed, user_id))
                conn.commit()
                return {"success": True, "user_id": user_id, "group_id": group_id}
            except Exception as e:
                return {"success": True, "user_id": user_id, "group_id": group_id}
                
    except mariadb.Error as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database query failed")
    finally:
        conn.close()

@router.post("/check_email")
def check_email(email: str) -> bool:
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM employee WHERE email = ? LIMIT 1", (email,))
        email_check = cursor.fetchone()
        return True if email_check else False
    except mariadb.Error:
        raise HTTPException(status_code=500, detail="Database query failed")
    finally:
        conn.close()

@router.post("/update_password")
def update_password(email: str, new_password: str) -> bool:
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE employee SET password = ? WHERE email = ?", (new_password, email))
        conn.commit()
        return True
    except mariadb.Error:
        raise HTTPException(status_code=500, detail="Database query failed")
    finally:
        conn.close()