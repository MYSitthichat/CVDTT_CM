from fastapi import APIRouter
import mariadb
from database import get_db_connection

router = APIRouter(tags=["Search_room"])

@router.get("/lab_report/rooms")
def get_rooms(search_keyword: str = ""):
    conn = get_db_connection()
    if not conn:
        return {"rooms": []}
    try:
        cursor = conn.cursor()
        
        query = """SELECT id, thai_name FROM room_information """
        params = []

        if search_keyword:
            query += " WHERE thai_name LIKE ?"
            params.append(f"%{search_keyword}%")

        cursor.execute(query, params)
        rooms = [{"id": row[0], "thai_name": row[1]} for row in cursor]
        cursor.close()
        
        return {"rooms": rooms}
    except mariadb.Error as e:
        print(f"Database Error: {e}")
        return {"rooms": []}
    finally:
        conn.close()