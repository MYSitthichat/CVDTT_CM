"""
สคริปต์แก้ไข Path ของฟอร์ม - ใช้งานง่าย
รันแล้วเลือกฟอร์มที่ต้องการแก้ไข
"""
import requests
import os

API_URL = "http://127.0.0.1:8000"
UPDATER_ID = 1

def show_all_forms():
    """แสดงฟอร์มทั้งหมด"""
    print("\n" + "=" * 80)
    print("รายการฟอร์มทั้งหมด")
    print("=" * 80 + "\n")
    
    try:
        # ดึงฟอร์มทุกห้อง
        response = requests.get(f"{API_URL}/report_information/all_by_status", 
                              params={"status": 1}, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            forms = data.get('data', [])
            
            if not forms:
                print("❌ ไม่พบฟอร์มในระบบ")
                return []
            
            print(f"พบทั้งหมด {len(forms)} ฟอร์ม:\n")
            
            for idx, form in enumerate(forms, 1):
                room_name = form.get('room_name', 'N/A')
                report_name = form.get('report_name', 'N/A')
                report_path = form.get('report_path', 'N/A')
                form_id = form.get('id', 'N/A')
                
                # ตรวจสอบว่าไฟล์มีจริงหรือไม่
                file_exists = os.path.exists(report_path) and os.path.isfile(report_path)
                status_icon = "✓" if file_exists else "✗"
                
                print(f"[{idx}] {status_icon} {room_name} - {report_name}")
                print(f"    ID: {form_id}")
                print(f"    Path: {report_path}")
                if not file_exists:
                    print(f"    ⚠ ไฟล์ไม่พบ!")
                print()
            
            return forms
        else:
            print(f"❌ Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {str(e)}")
        return []

def update_form_path(form_id, form_name, room_id, new_path):
    """Update path โดยการลบแล้วเพิ่มใหม่"""
    try:
        # 1. ลบฟอร์มเก่า (soft delete)
        print(f"\n  กำลังปิดใช้งานฟอร์มเก่า (ID: {form_id})...", end=" ")
        del_response = requests.delete(
            f"{API_URL}/report_information/delete",
            params={"report_id": form_id, "updater_id": UPDATER_ID},
            timeout=5
        )
        
        if del_response.status_code != 200:
            print(f"✗ ลบไม่สำเร็จ")
            return False
        print("✓")
        
        # 2. เพิ่มฟอร์มใหม่พร้อม path ใหม่
        print(f"  กำลังเพิ่มฟอร์มใหม่...", end=" ")
        add_data = {
            "report_name": form_name,
            "room_id": room_id,
            "report_path": new_path,
            "updater_id": UPDATER_ID
        }
        
        add_response = requests.post(
            f"{API_URL}/report_information/add",
            json=add_data,
            timeout=5
        )
        
        if add_response.status_code == 200:
            print("✓")
            return True
        else:
            print(f"✗ เพิ่มไม่สำเร็จ: {add_response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def main():
    print("=" * 80)
    print("โปรแกรมแก้ไข Path ของฟอร์ม")
    print("=" * 80)
    
    # แสดงรายการฟอร์ม
    forms = show_all_forms()
    
    if not forms:
        input("\nกด Enter เพื่อปิด...")
        return
    
    # เลือกฟอร์มที่ต้องการแก้
    print("=" * 80)
    while True:
        choice = input("เลือกฟอร์มที่ต้องการแก้ไข (กรอกหมายเลข หรือ 'q' เพื่อออก): ").strip()
        
        if choice.lower() == 'q':
            print("\nยกเลิกการแก้ไข")
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(forms):
                selected_form = forms[idx]
                
                print("\n" + "-" * 80)
                print(f"ฟอร์มที่เลือก: {selected_form['report_name']}")
                print(f"ห้อง: {selected_form['room_name']}")
                print(f"Path เดิม: {selected_form['report_path']}")
                print("-" * 80)
                
                # กรอก path ใหม่
                print("\nกรอก Path ใหม่ของไฟล์")
                print("(ใช้ / หรือ \\ ก็ได้, เช่น: D:/folder/file.docx)")
                new_path = input("Path ใหม่: ").strip()
                
                if not new_path:
                    print("❌ ไม่ได้กรอก path")
                    continue
                
                # แปลง \ เป็น /
                new_path = new_path.replace("\\", "/")
                
                # ตรวจสอบว่าไฟล์มีจริงหรือไม่
                if not os.path.exists(new_path):
                    print(f"\n⚠ เตือน: ไม่พบไฟล์ที่ path นี้")
                    confirm = input("ต้องการบันทึกต่อไปหรือไม่? (y/n): ").strip().lower()
                    if confirm != 'y':
                        print("ยกเลิกการแก้ไข")
                        continue
                elif not os.path.isfile(new_path):
                    print(f"\n❌ Path นี้ไม่ใช่ไฟล์")
                    continue
                
                # ยืนยันการแก้ไข
                print("\n" + "=" * 80)
                print("ยืนยันการแก้ไข:")
                print(f"  ฟอร์ม: {selected_form['report_name']}")
                print(f"  Path เดิม: {selected_form['report_path']}")
                print(f"  Path ใหม่: {new_path}")
                print("=" * 80)
                
                confirm = input("\nยืนยันการแก้ไข? (y/n): ").strip().lower()
                
                if confirm == 'y':
                    print("\nกำลังแก้ไข...")
                    success = update_form_path(
                        selected_form['id'],
                        selected_form['report_name'],
                        selected_form['room_id'],
                        new_path
                    )
                    
                    if success:
                        print("\n✓ แก้ไขสำเร็จ!")
                    else:
                        print("\n✗ แก้ไขไม่สำเร็จ")
                else:
                    print("\nยกเลิกการแก้ไข")
                
                # ถามว่าต้องการแก้ไขต่อหรือไม่
                print("\n" + "=" * 80)
                continue_edit = input("ต้องการแก้ไขฟอร์มอื่นอีกหรือไม่? (y/n): ").strip().lower()
                if continue_edit != 'y':
                    break
                    
                # แสดงรายการใหม่
                forms = show_all_forms()
                if not forms:
                    break
                    
            else:
                print("❌ หมายเลขไม่ถูกต้อง")
        except ValueError:
            print("❌ กรุณากรอกตัวเลข")
    
    print("\n" + "=" * 80)
    print("ปิดโปรแกรม")
    print("=" * 80)
    input("\nกด Enter เพื่อปิด...")

if __name__ == "__main__":
    main()
