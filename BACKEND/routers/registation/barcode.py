# routers/barcode.py
from fastapi import APIRouter, Query
import mariadb
from database import get_db_connection

router = APIRouter(tags=["Barcode"])

@router.get("/barcode/today")
def get_today_cases(offset: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """ดึงรายการในวันนี้ พร้อม Pagination"""
    conn = get_db_connection()
    if not conn: 
        return {"data": [], "total": 0, "has_more": False}
    try:
        cursor = conn.cursor()
        
        # Count total
        count_sql = """SELECT COUNT(DISTINCT s.id)
            FROM sample_registration s
            LEFT JOIN lab_order lo ON s.id = lo.sample_id
            WHERE DATE(s.dtime) = CURDATE() AND lo.status = 1
        """
        cursor.execute(count_sql)
        total = cursor.fetchone()[0]
        
        # Get paginated data
        sql = """SELECT 
                s.dtime, 
                lo.id,
                s.species, 
                CONCAT(IFNULL(r.code, ''), '(', IFNULL(r.nickname, ''), ')') AS lab_name,
                s.keep_method, 
                s.speed,
                lo.room_id AS room_debug
            FROM sample_registration s
            LEFT JOIN lab_order lo ON s.id = lo.sample_id
            LEFT JOIN room_information r ON lo.room_id = r.id
            WHERE DATE(s.dtime) = CURDATE() AND lo.status = 1
            ORDER BY s.dtime DESC
            LIMIT ? OFFSET ?
        """
        cursor.execute(sql, (limit, offset))
        results = [{"date": str(row[0]), "barcode": row[1], "species": row[2], 
                    "lab_name": row[3], "storage": row[4], "urgency": row[5]} for row in cursor]
        
        has_more = (offset + len(results)) < total
        
        return {
            "data": results,
            "total": total,
            "has_more": has_more,
            "offset": offset,
            "limit": limit
        }
    finally:
        conn.close()

@router.get("/barcode/search")
def search_barcode_cases(name: str = "", surname: str = "", offset: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """ Search cases by Customer Name/Surname with Pagination """
    conn = None
    try:
        conn = get_db_connection()
        if not conn: 
            return {"data": [], "total": 0, "has_more": False}
        
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
            return {"data": [], "total": 0, "has_more": False}

        where_clause = " AND ".join(conditions)
        
        # Count total
        count_sql = f"""
            SELECT COUNT(DISTINCT s.id)
            FROM sample_registration s
            LEFT JOIN case_registration c ON s.case_id = c.id
            LEFT JOIN customer cust ON (c.owner_id = cust.id OR c.sender_id = cust.id)
            LEFT JOIN lab_order lo ON s.id = lo.sample_id
            WHERE {where_clause} AND lo.status = 1
        """
        cursor.execute(count_sql, tuple(params))
        total = cursor.fetchone()[0]
        
        # Get paginated data
        sql = f"""
            SELECT DISTINCT
                s.id AS sample_id,
                s.dtime, 
                lo.id, 
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
            WHERE {where_clause} AND lo.status = 1
            ORDER BY s.dtime DESC, s.id
            LIMIT ? OFFSET ?
        """
        # Add limit and offset to params
        params_with_limit = list(params) + [limit, offset]
        cursor.execute(sql, tuple(params_with_limit))
        
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
        
        has_more = (offset + len(results)) < total
        
        return {
            "data": results,
            "total": total,
            "has_more": has_more,
            "offset": offset,
            "limit": limit
        }
    except mariadb.Error as e:
        print(f"Query Error (Search): {e}")
        return {"data": [], "total": 0, "has_more": False}
    finally:
        if conn: 
            conn.close()


@router.get("/barcode/search_by_employee")
def search_by_employee(employee_id: int, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Search cases by Employee ID with Pagination"""
    conn = None
    try:
        conn = get_db_connection()
        if not conn: 
            return {"data": [], "total": 0, "has_more": False}
        
        cursor = conn.cursor()
        
        # Count total
        count_sql = """
            SELECT COUNT(DISTINCT s.id)
            FROM lab_order lo
            LEFT JOIN sample_registration s ON lo.sample_id = s.id
            WHERE lo.updater = ? AND lo.status = 1
        """
        cursor.execute(count_sql, (employee_id,))
        total = cursor.fetchone()[0]

        # Get paginated data
        sql = """
            SELECT DISTINCT
                s.id AS sample_id,
                s.dtime, 
                lo.id,
                s.name AS sample_name,
                s.species, 
                CONCAT(IFNULL(r.code, ''), '(', IFNULL(r.nickname, ''), ')') AS lab_name,
                s.keep_method, 
                s.speed 
            FROM lab_order lo
            LEFT JOIN sample_registration s ON lo.sample_id = s.id
            LEFT JOIN room_information r ON lo.room_id = r.id
            WHERE lo.updater = ? AND lo.status = 1
            ORDER BY s.dtime DESC, s.id
            LIMIT ? OFFSET ?
        """
        cursor.execute(sql, (employee_id, limit, offset))
        
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
        
        has_more = (offset + len(results)) < total
        
        return {
            "data": results,
            "total": total,
            "has_more": has_more,
            "offset": offset,
            "limit": limit
        }
    except mariadb.Error as e:
        print(f"Query Error (Search by Employee): {e}")
        return {"data": [], "total": 0, "has_more": False}
    finally:
        if conn: 
            conn.close()