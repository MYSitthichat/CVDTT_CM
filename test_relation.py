import mariadb

# เชื่อมต่อฐานข้อมูล
conn = mariadb.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='cvdtt_lab',
    port=3306
)
cursor = conn.cursor()

print('\n=== ตัวอย่างข้อมูล lab_order (id=1588) ===')
cursor.execute('SELECT id, sample_id, room_id FROM lab_order WHERE id = 1588')
row = cursor.fetchone()
if row:
    print(f'lab_order_id: {row[0]}, sample_id: {row[1]}, room_id: {row[2]}')
    sample_id = row[1]
    
    print(f'\n=== ตัวอย่างข้อมูล sample_registration (id={sample_id}) ===')
    cursor.execute('SELECT id, case_id, name, species, breed FROM sample_registration WHERE id = %s', (sample_id,))
    row = cursor.fetchone()
    if row:
        print(f'sample_id: {row[0]}, case_id: {row[1]}, name: {row[2]}, species: {row[3]}, breed: {row[4]}')
        case_id = row[1]
        
        print(f'\n=== ตัวอย่างข้อมูล case_registration (id={case_id}) ===')
        cursor.execute('SELECT id, sender_id, owner_id, project_name FROM case_registration WHERE id = %s', (case_id,))
        row = cursor.fetchone()
        if row:
            print(f'case_id: {row[0]}, sender_id: {row[1]}, owner_id: {row[2]}, project_name: {row[3]}')
            sender_id = row[1]
            owner_id = row[2]
            
            print(f'\n=== ตัวอย่างข้อมูล customer (sender_id={sender_id}) ===')
            cursor.execute('SELECT id, name, surname, phone, contact_address FROM customer WHERE id = %s', (sender_id,))
            row = cursor.fetchone()
            if row:
                print(f'sender - id: {row[0]}, name: {row[1]}, surname: {row[2]}, phone: {row[3]}, address: {row[4]}')
            
            print(f'\n=== ตัวอย่างข้อมูล customer (owner_id={owner_id}) ===')
            cursor.execute('SELECT id, name, surname, phone, contact_address FROM customer WHERE id = %s', (owner_id,))
            row = cursor.fetchone()
            if row:
                print(f'owner - id: {row[0]}, name: {row[1]}, surname: {row[2]}, phone: {row[3]}, address: {row[4]}')

cursor.close()
conn.close()
