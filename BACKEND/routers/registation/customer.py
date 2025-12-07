# routers/customer.py
from fastapi import APIRouter, HTTPException
from typing import List
import mariadb
from database import get_db_connection
from schemas import SearchResult, NewCustomer

router = APIRouter(tags=["Customer"])

@router.get("/search", response_model=List[SearchResult])
def search_customer(q: str):
    if not q or len(q) < 2:
        return []
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    results = []
    try:
        cursor = conn.cursor()
        sql = """SELECT id, name, surname, tax_id 
                 FROM customer 
                 WHERE name LIKE ? OR surname LIKE ? OR id LIKE ? 
                 LIMIT 20"""
        search_pattern = f"%{q}%"
        cursor.execute(sql, (search_pattern, search_pattern, search_pattern))
        for row in cursor:
            results.append({
                "id": row[0],
                "name": row[1],
                "surname": row[2] if row[2] else "",
                "tax_id": row[3] if row[3] else "-",
                "display_text": f"{row[0]} : {row[1]} {row[2] if row[2] else ''} {row[3] if row[3] else '-'}"
            })
    except mariadb.Error as e:
        print(f"Query Error: {e}")
    finally:
        conn.close()
    return results

@router.post("/add_customer")
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
        raise HTTPException(status_code=500, detail="Failed to add customer")
    finally:
        conn.close()

@router.get("/get_customer_group_id")
def get_customer_group_id():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM customer_group ")
        groups = [{"id": row[0], "group_name": row[1]} for row in cursor]
        return {"customer_groups": groups}
    except mariadb.Error:
        raise HTTPException(status_code=500, detail="Failed to retrieve customer groups")
    finally:
        conn.close()