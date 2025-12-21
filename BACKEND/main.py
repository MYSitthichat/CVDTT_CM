from fastapi import FastAPI
from routers.registation import auth, customer, employee, work, lab, barcode, check_job_progress,lab_order, after_death
from routers.lab_report import select_room, receive_lab_order, send_lab , save_report_lab
from database import get_db_connection
from security import pwd_context
import mariadb

app = FastAPI()

# เชื่อมต่อ Router
app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(employee.router)
app.include_router(work.router)
app.include_router(lab.router)
app.include_router(barcode.router)
app.include_router(check_job_progress.router)
app.include_router(lab_order.router)
app.include_router(after_death.router)
app.include_router(select_room.router)
app.include_router(receive_lab_order.router)
app.include_router(send_lab.router)
app.include_router(save_report_lab.router)

@app.get("/")
def index():
    return {"message": "CVDTT API is running (Modular Structure)"}

@app.on_event("startup")
def hash_plain_passwords():
    conn = get_db_connection()
    if not conn:
        # print("Cannot connect to database for password encryption")
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
                # print(f"Encrypted password for user: {username}")
            except Exception as e:
                print(f"Error encrypting password for user {username}: {e}")
                continue
        
        if updated_count > 0:
            conn.commit()
            # print(f"Total {updated_count} passwords encrypted on startup")
        else:
            print("All passwords are already encrypted")

    except mariadb.Error as e:
        print(f"Database error during password encryption: {e}")
    finally:
        conn.close()


# python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level warning ::#คำสั่งรันเซิฟเวอร์ production

# python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug ::#คำสั่งรันเซิฟเวอร์ development