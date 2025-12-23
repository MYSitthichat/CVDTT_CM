import mariadb

try:
    # เชื่อมต่อฐานข้อมูล
    conn = mariadb.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='cvdtt_lab',
        port=3306
    )
    
    cursor = conn.cursor()
    
    # ดึงโครงสร้างของตาราง
    cursor.execute('DESCRIBE report_information')
    columns = cursor.fetchall()
    
    print('\n' + '='*120)
    print('โครงสร้างตาราง report_information')
    print('='*120)
    print(f"\n{'ชื่อคอลัมน์':<30} {'ชนิดข้อมูล':<25} {'Null':<8} {'Key':<8} {'Default':<15} {'Extra'}")
    print('-'*120)
    
    for col in columns:
        field = col[0]
        col_type = col[1]
        null_val = col[2]
        key_val = col[3]
        default_val = str(col[4]) if col[4] is not None else 'NULL'
        extra = col[5]
        print(f"{field:<30} {col_type:<25} {null_val:<8} {key_val:<8} {default_val:<15} {extra}")
    
    # นับจำนวนแถวในตาราง
    cursor.execute('SELECT COUNT(*) FROM report_information')
    count = cursor.fetchone()[0]
    print(f"\n{'='*120}")
    print(f"จำนวนข้อมูลทั้งหมด: {count} รายการ")
    print('='*120)
    
    # แสดงตัวอย่างข้อมูล 5 แถวแรก (ถ้ามี)
    if count > 0:
        cursor.execute('SELECT * FROM report_information LIMIT 5')
        sample_data = cursor.fetchall()
        print(f"\nตัวอย่างข้อมูล 5 แถวแรก:")
        print('-'*120)
        for row in sample_data:
            print(row)
    
    cursor.close()
    conn.close()
    
except mariadb.Error as e:
    print(f"เกิดข้อผิดพลาดในการเชื่อมต่อ MariaDB: {e}")
except Exception as e:
    print(f"เกิดข้อผิดพลาด: {e}")
