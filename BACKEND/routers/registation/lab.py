# routers/lab.py
from fastapi import APIRouter, HTTPException
import mariadb
from database import get_db_connection
from schemas import (MolecularBiologyData, ParasiteBiologyData, BacteriaBiologyData, 
                     LabOrder, UpdateTrackingLabOrder)

router = APIRouter(tags=["Lab"])

@router.get("/get_room_details")
def get_room_details():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, code, name, thai_name, nickname FROM room_information WHERE status = 1")
        rooms = [{"id": row[0], "code": row[1], "name": row[2], "thai_name": row[3], "nickname": row[4]} for row in cursor]
        return {"lab_rooms": rooms}
    finally:
        conn.close()

@router.post("/add_new_lab_order")
def add_lab_order(lab_order: LabOrder):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lab_order (sample_id, room_id, comments, state, status, updater) VALUES (?, ?, ?, ?, ?, ?)", 
                       (lab_order.sample_id, lab_order.room_id, lab_order.comments, lab_order.state, lab_order.status, lab_order.updater))
        conn.commit()
        return {"status": "success", "sample_id": lab_order.sample_id}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to add lab order: {str(e)}")
    finally:
        conn.close()

@router.post("/update_tracking_lab_order")
def update_tracking_lab_order(lab_order: UpdateTrackingLabOrder):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tracking_lab_order (lab_order_id, tracking_info, receiver, updater) VALUES (?, ?, ?, ?)", 
                       (lab_order.lab_order_id, lab_order.tracking_info, lab_order.receiver, lab_order.updater))
        conn.commit()
        return {"status": "success", "lab_order_id": lab_order.lab_order_id}
    finally:
        conn.close()

@router.post("/save_molecular_biology")
def save_molecular_biology(data: MolecularBiologyData):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        test_data = []
        for i in range(1, 62): 
            if i <= len(data.tests):
                test = data.tests[i-1]
                test_data.extend([
                    test.get('name', ''),
                    test.get('quantity', 0),
                    test.get('total_price', 0)
                ])
            else:
                test_data.extend(['', 0, 0])
                
        sql = """INSERT INTO lab_molecular_biology 
        (sample_id, test1_name, test1_amount, test1_price, test2_name, test2_amount, test2_price, 
        test3_name, test3_amount, test3_price, test4_name, test4_amount, test4_price, 
        test5_name, test5_amount, test5_price, test6_name, test6_amount, test6_price, 
        test7_name, test7_amount, test7_price, test8_name, test8_amount, test8_price, 
        test9_name, test9_amount, test9_price, test10_name, test10_amount, test10_price, 
        test11_name, test11_amount, test11_price, test12_name, test12_amount, test12_price, 
        test13_name, test13_amount, test13_price, test14_name, test14_amount, test14_price, 
        test15_name, test15_amount, test15_price, test16_name, test16_amount, test16_price, 
        test17_name, test17_amount, test17_price, test18_name, test18_amount, test18_price, 
        test19_name, test19_amount, test19_price, test20_name, test20_amount, test20_price, 
        test21_name, test21_amount, test21_price, test22_name, test22_amount, test22_price, 
        test23_name, test23_amount, test23_price, test24_name, test24_amount, test24_price, 
        test25_name, test25_amount, test25_price, test26_name, test26_amount, test26_price, 
        test27_name, test27_amount, test27_price, test28_name, test28_amount, test28_price, 
        test29_name, test29_amount, test29_price, test30_name, test30_amount, test30_price, 
        test31_name, test31_amount, test31_price, test32_name, test32_amount, test32_price, 
        test33_name, test33_amount, test33_price, test34_name, test34_amount, test34_price, 
        test35_name, test35_amount, test35_price, test36_name, test36_amount, test36_price, 
        test37_name, test37_amount, test37_price, test38_name, test38_amount, test38_price, 
        test39_name, test39_amount, test39_price, test40_name, test40_amount, test40_price, 
        test41_name, test41_amount, test41_price, test42_name, test42_amount, test42_price, 
        test43_name, test43_amount, test43_price, test44_name, test44_amount, test44_price, 
        test45_name, test45_amount, test45_price, test46_name, test46_amount, test46_price, 
        test47_name, test47_amount, test47_price, test48_name, test48_amount, test48_price, 
        test49_name, test49_amount, test49_price, test50_name, test50_amount, test50_price, 
        test51_name, test51_amount, test51_price, test52_name, test52_amount, test52_price, 
        test53_name, test53_amount, test53_price, test54_name, test54_amount, test54_price, 
        test55_name, test55_amount, test55_price, test56_name, test56_amount, test56_price, 
        test57_name, test57_amount, test57_price, test58_name, test58_amount, test58_price, 
        test59_name, test59_amount, test59_price, test60_name, test60_amount, test60_price, 
        test61_name, test61_amount, test61_price, cPCR_req, qPCR_req, extraction_req, updater) 
        VALUES (""" + ",".join(["?"] * 188) + ")"
        
        params = [data.sample_id] + test_data + [
            data.cPCR_req, 
            data.qPCR_req, 
            data.extraction_req, 
            data.updater
        ]
        
        if len(params) != 188:
            raise ValueError(f"Parameter mismatch: Expected 188, got {len(params)}")
        
        cursor.execute(sql, params)
        conn.commit()
        
        return {
            "status": "success",
            "message": "Molecular biology data saved successfully",
            "sample_id": data.sample_id,
            "tests_count": len(data.tests)
        }
        
    except mariadb.Error as e:
        print(f"Database Error: {e}")
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save molecular biology data: {str(e)}")
    finally:
        conn.close()


@router.post("/save_parasite_biology")
def save_parasite_biology(data: ParasiteBiologyData):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        test_data = []
        for i in range(1, 13):
            if i <= len(data.tests):
                test = data.tests[i-1]
                name_with_price = test.get('name', '')
                quantity = test.get('quantity', 0)
                price = test.get('price', 0)
                
                test_data.extend([
                    name_with_price,  
                    quantity,         
                    price             
                ])
            else:
                test_data.extend(['', 0, 0])
        sql = """INSERT INTO lab_parasite_biology 
        (sample_id, t1_name, t1_state, t1_price, t2_name, t2_state, t2_price, 
         t3_name, t3_state, t3_price, t4_name, t4_state, t4_price, 
         t5_name, t5_state, t5_price, t6_name, t6_state, t6_price, 
         t7_name, t7_state, t7_price, t8_name, t8_state, t8_price, 
         t9_name, t9_state, t9_price, t10_name, t10_state, t10_price, 
         t11_name, t11_state, t11_price, t12_name, t12_state, t12_price, updater) 
        VALUES (""" + ",".join(["?"] * 38) + ")"
        
        params = [data.sample_id] + test_data + [data.updater]
        
        if len(params) != 38:
            raise ValueError(f"Parameter mismatch: Expected 38, got {len(params)}")
        
        cursor.execute(sql, params)
        conn.commit()
        
        return {
            "status": "success",
            "message": "Parasite biology data saved successfully",
            "sample_id": data.sample_id,
            "tests_count": len(data.tests)
        }
        
    except mariadb.Error as e:
        print(f"Parasite Biology Database Error: {e}")
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save parasite biology data: {str(e)}")
    except ValueError as e:
        print(f"Parasite Biology Validation Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()


@router.post("/save_bacteria_biology")
def save_bacteria_biology(data: BacteriaBiologyData):
    """Save bacteria biology test data to database"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        columns = ["sample_id"]
        values = [data.sample_id]
        
        for i in range(1, 22):
            if i <= len(data.sample_preparation):
                item = data.sample_preparation[i-1]
                columns.extend([f"preparation_p{i}_name", f"preparation_p{i}_state", f"preparation_p{i}_amount"])
                values.extend([item.get('name', ''), item.get('state', 0), item.get('amount', 0)])
            else:
                columns.extend([f"preparation_p{i}_name", f"preparation_p{i}_state", f"preparation_p{i}_amount"])
                values.extend(['', 0, 0])
        
        for i in range(1, 42):
            if i <= len(data.drug_sensitivity):
                item = data.drug_sensitivity[i-1]
                columns.extend([f"drug_sensitivity{i}_name", f"drug_sensitivity{i}_state"])
                values.extend([item.get('name', ''), item.get('state', 0)])
            else:
                columns.extend([f"drug_sensitivity{i}_name", f"drug_sensitivity{i}_state"])
                values.extend(['', 0])
                
        for i in range(1, 13):
            if i <= len(data.bacteria_identification):
                item = data.bacteria_identification[i-1]
                columns.extend([f"bacteria_id{i}_name", f"bacteria_id{i}_state"])
                values.extend([item.get('name', ''), item.get('state', 0)])
            else:
                columns.extend([f"bacteria_id{i}_name", f"bacteria_id{i}_state"])
                values.extend(['', 0])
                
        for i in range(1, 6):
            if i <= len(data.lab_request):
                item = data.lab_request[i-1]
                columns.extend([f"lab_request{i}_name", f"lab_request{i}_state", f"lab_request{i}_price"])
                values.extend([item.get('name', ''), item.get('state', 0), item.get('price', 0)])
            else:
                columns.extend([f"lab_request{i}_name", f"lab_request{i}_state", f"lab_request{i}_price"])
                values.extend(['', 0, 0])
                
        columns.extend(["remark", "updater"])
        values.extend([data.remark, data.updater])
        placeholders = ",".join(["?"] * len(values))
        sql = f"INSERT INTO lab_bacteria_biology ({','.join(columns)}) VALUES ({placeholders})"
        
        cursor.execute(sql, values)
        conn.commit()
        
        return {
            "status": "success",
            "message": "Bacteria biology data saved successfully",
            "sample_id": data.sample_id
        }
        
    except mariadb.Error as e:
        print(f"Bacteria Biology Database Error: {e}")
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save bacteria biology data: {str(e)}")
    except Exception as e:
        print(f"Bacteria Biology Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
