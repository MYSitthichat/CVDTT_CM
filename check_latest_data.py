import mariadb

# Database Configuration
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "cvdtt_lab",
    "port": 3306
}

def check_latest_data():
    try:
        conn = mariadb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("=" * 80)
        print("ตรวจสอบข้อมูลล่าสุดในฐานข้อมูล")
        print("=" * 80)
        
        # 1. เช็คข้อมูล lab_order ล่าสุด
        print("\n1. ข้อมูล lab_order ล่าสุด (TOP 10):")
        print("-" * 80)
        cursor.execute("""
            SELECT id, dtime, sample_id, room_id, status 
            FROM lab_order 
            ORDER BY id DESC 
            LIMIT 10
        """)
        rows = cursor.fetchall()
        print(f"{'ID':<10} {'dtime':<20} {'sample_id':<12} {'room_id':<10} {'status':<10}")
        print("-" * 80)
        for row in rows:
            print(f"{row[0]:<10} {str(row[1]):<20} {row[2]:<12} {row[3]:<10} {row[4]:<10}")
        
        # 2. เช็คข้อมูล lab_order ที่ status = 1 และ room_id = 2 (Bacteria)
        print("\n\n2. ข้อมูล lab_order ที่ status=1 และ room_id=2 (Bacteria) TOP 10:")
        print("-" * 80)
        cursor.execute("""
            SELECT lo.id, sr.dtime, lo.sample_id, lo.room_id, lo.status, sr.sample_inspection
            FROM lab_order lo
            LEFT JOIN sample_registration sr ON lo.sample_id = sr.id
            WHERE lo.status = 1 AND lo.room_id = 2
            ORDER BY sr.dtime DESC, lo.id DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()
        print(f"{'ID':<10} {'dtime':<20} {'sample_id':<12} {'room_id':<10} {'status':<10} {'sample':<20}")
        print("-" * 80)
        for row in rows:
            print(f"{row[0]:<10} {str(row[1]):<20} {row[2]:<12} {row[3]:<10} {row[4]:<10} {str(row[5]):<20}")
        
        # 3. เช็คข้อมูล sample_registration ล่าสุด
        print("\n\n3. ข้อมูล sample_registration ล่าสุด (TOP 10):")
        print("-" * 80)
        cursor.execute("""
            SELECT id, dtime, sample_inspection, speed 
            FROM sample_registration 
            ORDER BY dtime DESC 
            LIMIT 10
        """)
        rows = cursor.fetchall()
        print(f"{'ID':<10} {'dtime':<20} {'sample_inspection':<30} {'speed':<15}")
        print("-" * 80)
        for row in rows:
            print(f"{row[0]:<10} {str(row[1]):<20} {str(row[2]):<30} {str(row[3]):<15}")
        
        # 4. เช็คข้อมูล lab_bacteria_biology ล่าสุด
        print("\n\n4. ข้อมูล lab_bacteria_biology ล่าสุด (TOP 10):")
        print("-" * 80)
        cursor.execute("""
            SELECT id, dtime, sample_id, status 
            FROM lab_bacteria_biology 
            ORDER BY id DESC 
            LIMIT 10
        """)
        rows = cursor.fetchall()
        print(f"{'ID':<10} {'dtime':<20} {'sample_id':<12} {'status':<10}")
        print("-" * 80)
        for row in rows:
            print(f"{row[0]:<10} {str(row[1]):<20} {row[2]:<12} {row[3]:<10}")
        
        # 5. สรุปจำนวนข้อมูล
        print("\n\n5. สรุปจำนวนข้อมูล:")
        print("-" * 80)
        
        cursor.execute("SELECT COUNT(*) FROM lab_order WHERE status = 1 AND room_id = 2")
        count = cursor.fetchone()[0]
        print(f"lab_order (status=1, room_id=2): {count} รายการ")
        
        cursor.execute("SELECT COUNT(*) FROM lab_bacteria_biology WHERE status = 1")
        count = cursor.fetchone()[0]
        print(f"lab_bacteria_biology (status=1): {count} รายการ")
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM lab_bacteria_biology lbb
            LEFT JOIN lab_order lo ON lbb.sample_id = lo.sample_id AND lo.room_id = 2
            WHERE lbb.status = 1 AND lo.id IS NULL
        """)
        count = cursor.fetchone()[0]
        print(f"lab_bacteria_biology ที่ยังไม่มี lab_order: {count} รายการ")
        
        print("\n" + "=" * 80)
        
        conn.close()
        
    except mariadb.Error as e:
        print(f"Database Error: {e}")

if __name__ == "__main__":
    check_latest_data()
