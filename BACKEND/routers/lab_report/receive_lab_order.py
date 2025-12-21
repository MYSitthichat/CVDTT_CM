from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import mariadb
import re
from database import get_db_connection

router = APIRouter(tags=["Receive_lab_order"])


# Pydantic models สำหรับรับข้อมูล
class ReceiveLabRequest(BaseModel):
    lab_order_id: int
    receive_from_room: int
    comment_for_sample: str = ""
    sample_status: str = "ปกติ"
    updater_id: int  # employee_id ของคนที่ login


class RejectLabRequest(BaseModel):
    lab_order_id: int
    receive_from_room: int
    comment_for_sample: str = ""
    sample_status: str = "เสียหาย/ไม่ปกติ"
    updater_id: int  # employee_id ของคนที่ login


@router.get("/get_lab_order/detail")
def get_lab_order_detail(lab_order_id: str, room_id: str = ""):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        if room_id:
            query = """
                SELECT 
                    lab_order.id AS lab_order_id,
                    sample_registration.dtime,
                    sample_registration.speed,
                    sample_registration.sample_inspection,
                    sample_registration.id AS sample_id,
                    lab_order.room_id
                FROM lab_order
                INNER JOIN sample_registration
                    ON lab_order.sample_id = sample_registration.id
                WHERE lab_order.id = ? AND 
                lab_order.room_id = ? AND lab_order.status = 1
                """
            cursor.execute(query, (lab_order_id, room_id))
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve lab order detail")
    finally:
        conn.close()




@router.get("/get_lab_order/to_day")
def get_lab_order_to_day(room_id: str, offset: int = 0, limit: int = 50):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("""
                SELECT 
                    sample_registration.dtime,
                    lab_order.id AS lab_order_id,
                    sample_registration.speed,
                    sample_registration.sample_inspection
                FROM lab_order
                INNER JOIN sample_registration 
                    ON lab_order.sample_id = sample_registration.id
                WHERE lab_order.room_id = ? AND lab_order.status = 1
                ORDER BY lab_order.id DESC 
                LIMIT ? OFFSET ?
                """, (room_id, limit, offset))
        groups = [{"time": row[0], "lab_order_id": row[1], "speed": row[2], "sample_inspection": row[3]} for row in cursor]
        
        cursor.execute("SELECT COUNT(*) FROM lab_order WHERE room_id = ? AND status = 1", (room_id,))
        total_count = cursor.fetchone()[0]
        
        return {
            "job_progress": groups,
            "total": total_count,
            "offset": offset,
            "limit": limit,
            "has_more": (offset + limit) < total_count
        }
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve job progress")
    finally:
        conn.close()

@router.get("/get_lab_order/barcode")
def get_lab_order_by_barcode(barcode: str, room_id: str = ""):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        
        # Convert barcode to lab_order_id (remove leading zeros)
        try:
            lab_order_id = int(barcode)
        except ValueError:
            return {
                "job_progress": [],
                "total": 0,
                "found": False,
                "message": "Barcode ไม่ถูกต้อง"
            }
        
        # Build query with room_id filter if provided
        if room_id:
            query = """
                SELECT 
                    sample_registration.dtime,
                    lab_order.id AS lab_order_id,
                    sample_registration.speed,
                    sample_registration.sample_inspection,
                    sample_registration.id AS sample_id,
                    lab_order.room_id
                FROM lab_order
                INNER JOIN sample_registration 
                    ON lab_order.sample_id = sample_registration.id
                WHERE lab_order.id = ? 
                    AND lab_order.room_id = ? 
                    AND lab_order.status = 1
                ORDER BY lab_order.id DESC 
                """
            cursor.execute(query, (lab_order_id, room_id))
        else:
            # Admin mode - no room restriction
            query = """
                SELECT 
                    sample_registration.dtime,
                    lab_order.id AS lab_order_id,
                    sample_registration.speed,
                    sample_registration.sample_inspection,
                    sample_registration.id AS sample_id,
                    lab_order.room_id
                FROM lab_order
                INNER JOIN sample_registration 
                    ON lab_order.sample_id = sample_registration.id
                WHERE lab_order.id = ? AND lab_order.status = 1
                ORDER BY lab_order.id DESC 
                """
            cursor.execute(query, (lab_order_id,))
        
        results = cursor.fetchall()
        
        if not results:
            if room_id:
                return {
                    "job_progress": [],
                    "total": 0,
                    "found": False,
                    "message": "ไม่พบข้อมูล Barcode นี้ในห้องของคุณ หรือไม่มีสิทธิ์เข้าถึง"
                }
            else:
                return {
                    "job_progress": [],
                    "total": 0,
                    "found": False,
                    "message": "ไม่พบข้อมูล Barcode นี้"
                }
        
        groups = [{
            "time": row[0], 
            "lab_order_id": row[1], 
            "speed": row[2], 
            "sample_inspection": row[3],
            "sample_id": row[4],
            "room_id": row[5]
        } for row in results]
        
        return {
            "job_progress": groups,
            "total": len(groups),
            "found": True,
            "message": f"พบข้อมูล {len(groups)} รายการ"
        }
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to search by barcode")
    finally:
        conn.close()

@router.get("/get_lab_order/details")
def get_lab_order_details(lab_order_id: str, room_id: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = None
    try:
        cursor = conn.cursor()
        
        # แปลง lab_order_id เป็น int
        try:
            order_id = int(lab_order_id)
        except ValueError:
            return {
                "success": False,
                "message": "Lab Order ID ไม่ถูกต้อง"
            }
        
        # ดึงข้อมูล Lab Order และ Sample Registration
        sql_order = """
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
                cr.project_name,
                sr.id AS sample_id,
                lo.room_id,
                sr.sample_inspection
            FROM lab_order lo
            LEFT JOIN sample_registration sr ON lo.sample_id = sr.id 
            LEFT JOIN room_information ri ON lo.room_id = ri.id 
            LEFT JOIN case_registration cr ON sr.case_id = cr.id
            WHERE lo.id = %s AND lo.status = 1
        """
        
        if room_id:
            sql_order += " AND lo.room_id = %s"
            cursor.execute(sql_order, (order_id, room_id))
        else:
            cursor.execute(sql_order, (order_id,))
        
        order_result = cursor.fetchone()
        
        if not order_result:
            return {
                "success": False,
                "message": "ไม่พบข้อมูล Lab Order นี้"
            }
        
        # แปลง tuple เป็น dict
        order_data = {
            "dtime": order_result[0],
            "lab_order_id": order_result[1],
            "species": order_result[2],
            "room_code": order_result[3],
            "room_nickname": order_result[4],
            "keep_method": order_result[5],
            "speed": order_result[6],
            "name": order_result[7],
            "opd_number": order_result[8],
            "sex": order_result[9],
            "age_year": order_result[10],
            "age_month": order_result[11],
            "age_day": order_result[12],
            "breed": order_result[13],
            "sample_type": order_result[14],
            "project_name": order_result[15],
            "sample_id": order_result[16],
            "room_id": order_result[17],
            "sample_inspection": order_result[18]
        }
        
        # ดึงรายการตรวจตาม room_id
        test_items = []
        sample_id = order_data["sample_id"]
        room_id_val = order_data["room_id"]
        room_code = order_data["room_code"] if order_data["room_code"] else ""
        
        # ใช้ room_id แทน room_code เพื่อระบุห้องแลป
        # room_id: 2=Bacteria, 5=Parasite, 8=Molecular
        if room_id_val == 5:  # Parasite
            sql_test = """SELECT * FROM lab_parasite_biology WHERE sample_id = %s"""
            cursor.execute(sql_test, (sample_id,))
            test_data = cursor.fetchone()
            if test_data:
                # Parse parasite test data (columns 3 onwards, every 3 columns = t_name, t_state, t_price)
                # Structure: t1_name, t1_state, t1_price, t2_name, t2_state, t2_price, ...
                # สำหรับ Parasite: t_state เก็บจำนวน (0=ไม่เลือก, >0=เลือกและเป็นจำนวน)
                raw_test_data = test_data[3:]  # Get all columns after id, sample_id, dtime
                for i in range(0, len(raw_test_data), 3):
                    test_name = raw_test_data[i] if i < len(raw_test_data) else ""
                    test_state = int(raw_test_data[i+1]) if i+1 < len(raw_test_data) and raw_test_data[i+1] is not None else 0
                    test_price = int(raw_test_data[i+2]) if i+2 < len(raw_test_data) and raw_test_data[i+2] is not None else 0
                    # เฉพาะรายการที่ state > 0 (state คือจำนวนเลย)
                    if test_state > 0 and test_name:
                        # ลบตัวเลขในวงเล็บออก เช่น "PCV (50)" -> "PCV"
                        # แปลงเป็น string ก่อนใช้ re.sub เพื่อป้องกัน TypeError
                        test_name_str = str(test_name) if test_name is not None else ""
                        clean_name = re.sub(r'\s*\(\d+\)\s*$', '', test_name_str).strip()
                        test_items.append({
                            "test_name": clean_name,
                            "test_amount": test_state  # ใช้ state เป็นจำนวน
                        })
        
        elif room_id_val == 2:  # Bacteria
            sql_test = """SELECT * FROM lab_bacteria_biology WHERE sample_id = %s"""
            cursor.execute(sql_test, (sample_id,))
            
            # Get column names before fetching data
            col_names = [desc[0] for desc in cursor.description]
            test_data = cursor.fetchone()
            
            if test_data:
                # Parse bacteria test data using column names (structure is complex with different patterns)
                # 1. preparation_p1-p21: name, state, amount (3 columns each)
                # 2. drug_sensitivity1-41: name, state (2 columns each - no amount, set amount=7)
                # 3. bacteria_id1-12: name, state (2 columns each - set amount=7)
                # 4. lab_request1-5: name, state, price (3 columns each - set amount=7)
                
                try:
                    # Process preparation_p1-p21 (use state as amount)
                    for i in range(1, 22):  # p1 to p21
                        name_idx = col_names.index(f'preparation_p{i}_name')
                        state_idx = col_names.index(f'preparation_p{i}_state')
                        
                        test_name = test_data[name_idx] if test_data[name_idx] else ""
                        test_state = int(test_data[state_idx]) if test_data[state_idx] is not None else 0
                        
                        if test_state > 0 and test_name:
                            clean_name = re.sub(r'\s*\(\d+\)\s*$', '', test_name).strip()
                            test_items.append({
                                "test_name": clean_name,
                                "test_amount": test_state
                            })
                    
                    # Process drug_sensitivity1-41 (use state as amount)
                    for i in range(1, 42):  # 1 to 41
                        name_idx = col_names.index(f'drug_sensitivity{i}_name')
                        state_idx = col_names.index(f'drug_sensitivity{i}_state')
                        
                        test_name = test_data[name_idx] if test_data[name_idx] else ""
                        test_state = int(test_data[state_idx]) if test_data[state_idx] is not None else 0
                        
                        if test_state > 0 and test_name:
                            clean_name = re.sub(r'\s*\(\d+\)\s*$', '', test_name).strip()
                            test_items.append({
                                "test_name": clean_name,
                                "test_amount": test_state
                            })
                    
                    # Process bacteria_id1-12 (use state as amount)
                    for i in range(1, 13):  # 1 to 12
                        name_idx = col_names.index(f'bacteria_id{i}_name')
                        state_idx = col_names.index(f'bacteria_id{i}_state')
                        
                        test_name = test_data[name_idx] if test_data[name_idx] else ""
                        test_state = int(test_data[state_idx]) if test_data[state_idx] is not None else 0
                        
                        if test_state > 0 and test_name:
                            clean_name = re.sub(r'\s*\(\d+\)\s*$', '', test_name).strip()
                            test_items.append({
                                "test_name": clean_name,
                                "test_amount": test_state
                            })
                    
                    # Process lab_request1-5 (use state as amount)
                    for i in range(1, 6):  # 1 to 5
                        name_idx = col_names.index(f'lab_request{i}_name')
                        state_idx = col_names.index(f'lab_request{i}_state')
                        
                        test_name = test_data[name_idx] if test_data[name_idx] else ""
                        test_state = int(test_data[state_idx]) if test_data[state_idx] is not None else 0
                        
                        if test_state > 0 and test_name:
                            clean_name = re.sub(r'\s*\(\d+\)\s*$', '', test_name).strip()
                            test_items.append({
                                "test_name": clean_name,
                                "test_amount": test_state
                            })
                except Exception as e:
                    # If error occurs during parsing, return what we have so far
                    print(f"Error parsing bacteria data: {e}")
        
        elif room_id_val == 8:  # Molecular Biology
            sql_test = """SELECT * FROM lab_molecular_biology WHERE sample_id = %s"""
            cursor.execute(sql_test, (sample_id,))
            test_data = cursor.fetchone()
            if test_data:
                # Parse molecular test data (columns 3 onwards, every 3 columns = test_name, test_amount, test_price)
                # Structure: test1_name, test1_amount, test1_price, test2_name, test2_amount, test2_price, ...
                # สำหรับ Molecular: ไม่มี state, amount คือจำนวน (0=ไม่เลือก, >0=เลือกและเป็นจำนวน)
                raw_test_data = test_data[3:]
                for i in range(0, len(raw_test_data), 3):
                    test_name = raw_test_data[i] if i < len(raw_test_data) else ""
                    test_amount = int(raw_test_data[i+1]) if i+1 < len(raw_test_data) and raw_test_data[i+1] is not None else 0
                    test_price = int(raw_test_data[i+2]) if i+2 < len(raw_test_data) and raw_test_data[i+2] is not None else 0
                    # เฉพาะรายการที่ amount > 0 (amount คือจำนวนเลย)
                    if test_amount > 0 and test_name:
                        # ลบตัวเลขในวงเล็บออก
                        clean_name = re.sub(r'\s*\(\d+\)\s*$', '', test_name).strip()
                        test_items.append({
                            "test_name": clean_name,
                            "test_amount": test_amount  # ใช้ amount เป็นจำนวน
                        })
        
        return {
            "success": True,
            "order_data": order_data,
            "test_items": test_items
        }
        
    except mariadb.Error as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve lab order details")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@router.post("/receive_lab_order")
def receive_lab_order(request: ReceiveLabRequest):
    """
    บันทึกข้อมูลการรับแลป
    - room_action_status = 1 (รับแลป)
    - sample_status: "ปกติ" หรือ "เสียหาย/ไม่ปกติ"
    - ดึง case_id จาก lab_order โดยอัตโนมัติ
    """
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = None
    try:
        cursor = conn.cursor()
        
        # ดึงข้อมูล lab_order และ case_id
        sql_check = """
            SELECT lo.id, sr.case_id 
            FROM lab_order lo
            LEFT JOIN sample_registration sr ON lo.sample_id = sr.id
            WHERE lo.id = %s AND lo.status = 1
        """
        cursor.execute(sql_check, (request.lab_order_id,))
        result = cursor.fetchone()
        
        if not result:
            return {
                "success": False,
                "message": "ไม่พบ Lab Order นี้"
            }
        
        case_id = result[1]  # ดึง case_id จาก sample_registration
        
        # บันทึกข้อมูลการรับแลป
        sql = """
            INSERT INTO lab_receive_detail 
            (lab_order_id, case_id, receive_from_room, comment_for_sample, room_action_status,  updater) 
            VALUES (%s, %s, %s, %s, 1, %s)
        """
        
        cursor.execute(sql, (request.lab_order_id, case_id, request.receive_from_room, request.comment_for_sample, request.updater_id))
        conn.commit()
        
        return {
            "success": True,
            "message": "บันทึกการรับแลปสำเร็จ",
            "lab_order_id": request.lab_order_id
        }
        
    except mariadb.Error as e:
        if conn:
            conn.rollback()
        print(f"Database Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save receive lab data: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@router.post("/reject_lab_order")
def reject_lab_order(request: RejectLabRequest):
    """
    ปฏิเสธการรับแลป
    - room_action_status = 0 (ปฏิเสธ)
    - ดึง case_id จาก lab_order โดยอัตโนมัติ
    """
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = None
    try:
        cursor = conn.cursor()
        
        # ดึงข้อมูล lab_order และ case_id
        sql_check = """
            SELECT lo.id, sr.case_id 
            FROM lab_order lo
            LEFT JOIN sample_registration sr ON lo.sample_id = sr.id
            WHERE lo.id = %s AND lo.status = 1
        """
        cursor.execute(sql_check, (request.lab_order_id,))
        result = cursor.fetchone()
        
        if not result:
            return {
                "success": False,
                "message": "ไม่พบ Lab Order นี้"
            }
        
        case_id = result[1]  # ดึง case_id จาก sample_registration
        
        # บันทึกข้อมูลการปฏิเสธแลป
        sql = """
            INSERT INTO lab_receive_detail 
            (lab_order_id, case_id, receive_from_room, comment_for_sample, room_action_status, updater) 
            VALUES (%s, %s, %s, %s, 0, %s)
        """
        
        cursor.execute(sql, (request.lab_order_id, case_id, request.receive_from_room, request.comment_for_sample, request.updater_id))
        conn.commit()
        
        return {
            "success": True,
            "message": "บันทึกการปฏิเสธแลปสำเร็จ",
            "lab_order_id": request.lab_order_id
        }
        
    except mariadb.Error as e:
        if conn:
            conn.rollback()
        print(f"Database Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save reject lab data: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()