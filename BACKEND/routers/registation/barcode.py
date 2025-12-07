# routers/barcode.py
from fastapi import APIRouter
import mariadb
from database import get_db_connection

router = APIRouter(tags=["Barcode"])

@router.get("/barcode/today")
def get_today_cases():
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        sql = """SELECT s.dtime, s.case_id, s.species, CONCAT(IFNULL(r.code, ''), '(', IFNULL(r.nickname, ''), ')') AS lab_name,
                s.keep_method, s.speed, lo.room_id AS room_debug
                FROM sample_registration s
                LEFT JOIN lab_order lo ON s.id = lo.sample_id
                LEFT JOIN room_information r ON lo.room_id = r.id
                WHERE DATE(s.dtime) = CURDATE() ORDER BY s.dtime DESC"""
        cursor.execute(sql)
        results = [{"date": str(row[0]), "barcode": row[1], "species": row[2], 
                    "lab_name": row[3], "storage": row[4], "urgency": row[5]} for row in cursor]
        return results
    finally:
        conn.close()

@router.get("/barcode/search")
def search_barcode_cases(name: str = "", surname: str = ""):
    """ Search cases by Customer Name/Surname """
    conn = None
    try:
        conn = get_db_connection()
        if not conn: 
            return []
        
        cursor = conn.cursor()
        conditions = []
        params = []
        search_name = name.strip() if name else ""
        search_surname = surname.strip() if surname else ""
        if search_name and search_surname and search_surname in search_name:
            search_name = search_name.replace(search_surname, "").strip()
        
        if search_name:
            conditions.append("cust.name LIKE ?")
            params.append(f"%{search_name}%")
        
        if search_surname:
            conditions.append("cust.surname LIKE ?")
            params.append(f"%{search_surname}%")
        if not conditions:
            return []

        where_clause = " AND ".join(conditions)
        debug_sql = f"""
            SELECT DISTINCT cust.id, cust.name, cust.surname
            FROM customer cust
            WHERE {where_clause}
        """
        cursor.execute(debug_sql, tuple(params))
        cursor.fetchall()
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
            LEFT JOIN lab_order lo ON s.id = lo.sample_id
            LEFT JOIN room_information r ON lo.room_id = r.id
            WHERE {where_clause}
            ORDER BY s.dtime DESC, s.id
        """
        cursor.execute(sql, tuple(params))
        results = []
        seen_sample_ids = set()
        for row in cursor:
            sample_id = row[0]
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
        return results
    except mariadb.Error as e:
        print(f"Query Error (Search): {e}")
        return []
    finally:
        if conn: 
            conn.close()


@router.get("/barcode/search_by_employee")
def search_by_employee(employee_id: int):
    conn = None
    try:
        conn = get_db_connection()
        if not conn: 
            return []
        
        cursor = conn.cursor()
        debug_sql = "SELECT id, sample_id, room_id, updater FROM lab_order WHERE updater = ? LIMIT 10"
        cursor.execute(debug_sql, (employee_id,))
        cursor.fetchall()

        sql = """
            SELECT DISTINCT
                s.id AS sample_id,
                s.dtime, 
                s.case_id, 
                s.name AS sample_name,
                s.species, 
                CONCAT(IFNULL(r.code, ''), '(', IFNULL(r.nickname, ''), ')') AS lab_name,
                s.keep_method, 
                s.speed 
            FROM lab_order lo
            LEFT JOIN sample_registration s ON lo.sample_id = s.id
            LEFT JOIN room_information r ON lo.room_id = r.id
            WHERE lo.updater = ?
            ORDER BY s.dtime DESC, s.id
        """
        cursor.execute(sql, (employee_id,))
        results = []
        seen_sample_ids = set()
        for row in cursor:
            sample_id = row[0]
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
        return results
    except mariadb.Error as e:
        print(f"Query Error (Search by Employee): {e}")
        return []
    finally:
        if conn: 
            conn.close()