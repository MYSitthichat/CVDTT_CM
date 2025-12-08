from fastapi import APIRouter, HTTPException
from datetime import date, datetime
import mariadb
from database import get_db_connection

router = APIRouter(tags=["Lab_Order"])


@router.get("/search_lab_order_by_barcode/{barcode}")
def search_lab_order_by_barcode(barcode: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = None
    try:
        cursor = conn.cursor()
        try:
            order_id = int(barcode.lstrip('0')) if barcode.lstrip('0') else 0
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid barcode format")
        
        sql = """
            SELECT 
                lo.dtime, 
                lo.id, 
                sr.species, 
                ri.code, 
                ri.nickname, 
                sr.keep_method, 
                sr.speed 
            FROM lab_order lo
            LEFT JOIN sample_registration sr ON lo.sample_id = sr.id 
            LEFT JOIN room_information ri ON lo.room_id = ri.id 
            WHERE lo.id = %s AND lo.status = 1
        """
        
        cursor.execute(sql, (order_id,))
        result = cursor.fetchall()
        
        return {
            "status": "success", 
            "barcode": barcode,
            "order_id": order_id,
            "data": result
        }
        
    except mariadb.Error as e:
        print(f"MariaDB Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@router.get("/search_today_lab_orders")
def search_today_lab_orders():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = None
    try:
        cursor = conn.cursor()
        today = date.today()
        
        sql = """
            SELECT 
                lo.dtime, 
                lo.id, 
                sr.species, 
                ri.code, 
                ri.nickname, 
                sr.keep_method, 
                sr.speed 
            FROM lab_order lo
            LEFT JOIN sample_registration sr ON lo.sample_id = sr.id 
            LEFT JOIN room_information ri ON lo.room_id = ri.id 
            WHERE DATE(lo.dtime) = %s AND lo.status = 1
            ORDER BY lo.dtime DESC
        """
        
        cursor.execute(sql, (today,))
        result = cursor.fetchall()
        
        return {
            "status": "success", 
            "date": str(today),
            "count": len(result),
            "data": result
        }
        
    except mariadb.Error as e:
        print(f"MariaDB Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@router.get("/get_lab_order_details/{order_id}")
def get_lab_order_details(order_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = None
    try:
        cursor = conn.cursor()
        
        sql = """
            SELECT 
                lo.dtime, 
                lo.id, 
                sr.species, 
                ri.code, 
                ri.nickname, 
                sr.keep_method, 
                sr.speed,
                sr.name,
                sr.opd_number,
                sr.sex,
                sr.age_year,
                sr.age_month,
                sr.age_day,
                sr.breed,
                sr.sample_type,
                cr.project_name
            FROM lab_order lo
            LEFT JOIN sample_registration sr ON lo.sample_id = sr.id 
            LEFT JOIN room_information ri ON lo.room_id = ri.id 
            LEFT JOIN case_registration cr ON sr.case_id = cr.id
            WHERE lo.id = %s AND lo.status = 1
        """
        
        cursor.execute(sql, (order_id,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Order ID {order_id} not found")
        
        return {
            "status": "success", 
            "order_id": order_id,
            "data": result
        }
        
    except mariadb.Error as e:
        print(f"MariaDB Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()