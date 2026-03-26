# ไฟล์ที่สามารถลบได้

## ✅ สามารถลบได้อย่างปลอดภัย (ไฟล์ทดสอบและเครื่องมือชั่วคราว)

### สคริปต์เพิ่ม Placeholders (ทำงานเสร็จแล้ว - ไม่ต้องใช้อีก)
- `add_date_placeholders.py` - เพิ่ม placeholder วันที่ (ทำงานเสร็จแล้ว)
- `add_nested_table_placeholders.py` - เพิ่ม placeholder ใน nested table (ทำงานเสร็จแล้ว)
- `add_placeholders_all_templates.py` - เพิ่ม placeholder ทุกเทมเพลต (ทำงานเสร็จแล้ว)
- `add_placeholders_to_template.py` - เพิ่ม placeholder เริ่มต้น (ทำงานเสร็จแล้ว)
- `add_table_placeholders.py` - เพิ่ม placeholder ในตาราง (ทำงานเสร็จแล้ว)
- `clean_template_placeholders.py` - ทำความสะอาด placeholder ซ้ำ (ทำงานเสร็จแล้ว)
- `change_template_fonts.py` - เปลี่ยนฟอนต์เทมเพลต (ทำงานเสร็จแล้ว)

### เครื่องมือตรวจสอบและทดสอบ
- `check_date_placeholders.py` - เช็ค placeholder วันที่
- `check_word_template.py` - เช็คเทมเพลต Word
- `complete_search.py` - ค้นหาในเทมเพลต
- `find_nested_table.py` - หา nested table
- `inspect_table_structure.py` - ตรวจสอบโครงสร้างตาราง

### สคริปต์ทดสอบ API และฟังก์ชัน
- `test_api_dates.py` - ทดสอบ API วันที่
- `test_api_parasite.py` - ทดสอบ API parasite
- `test_date_format_iso.py` - ทดสอบรูปแบบวันที่ ISO
- `test_report_form_api.py` - ทดสอบ API report form
- `test_report_form_database.py` - ทดสอบฐานข้อมูล
- `test_thai_date_format.py` - ทดสอบรูปแบบวันที่ไทย

### เอกสารสรุป
- `SUMMARY_date_fix.py` - สรุปการแก้ไขวันที่ (เป็น Python แต่เนื้อหาเป็นเอกสาร)

---

## ⚠️ พิจารณาก่อนลบ (อาจใช้ในอนาคต)

- `add_parasite_forms_to_db.py` - เพิ่มข้อมูลฟอร์มลงฐานข้อมูล (ใช้เมื่อต้องเพิ่มฟอร์มใหม่)
- `update_form_path.py` - อัปเดต path ของฟอร์ม (ใช้เมื่อย้ายไฟล์)
- `fix_parasite_forms_complete.py` - แก้ไขฟอร์ม (ตรวจสอบก่อนว่ายังใช้งานหรือไม่)

---

## 🔒 ห้ามลบ (ไฟล์สำคัญ)

- `create_report_form_table.sql` - SQL schema สำหรับสร้างตาราง report_form
- `PARASITE_FORM_USAGE.md` - เอกสารการใช้งาน
- `WORD_TEMPLATE_GUIDE.md` - คู่มือเทมเพลต Word
- `start_api_server.bat` - สคริปต์เริ่ม API server

---

## 📁 โฟลเดอร์ชั่วคราวที่สามารถลบข้อมูลข้างในได้

- `temp_file_report/` - ไฟล์ชั่วคราวจากการ preview ฟอร์ม (ลบไฟล์ข้างในได้)
  * เก็บไว้แค่โฟลเดอร์เปล่า ระบบจะสร้างไฟล์ใหม่เมื่อใช้งาน

---

## คำแนะนำการลบ

### วิธีที่ 1: ลบทีละไฟล์ (ปลอดภัยที่สุด)
```powershell
# ลบไฟล์ทดสอบ
Remove-Item test_*.py
Remove-Item check_*.py

# ลบสคริปต์เพิ่ม placeholder
Remove-Item add_*placeholders*.py
Remove-Item clean_template_placeholders.py
Remove-Item change_template_fonts.py

# ลบเครื่องมือตรวจสอบ
Remove-Item complete_search.py
Remove-Item find_nested_table.py
Remove-Item inspect_table_structure.py
Remove-Item SUMMARY_date_fix.py
```

### วิธีที่ 2: ลบทั้งหมดพร้อมกัน
```powershell
# สร้างโฟลเดอร์เก็บไฟล์เพื่อความปลอดภัย (กรณีอยากเก็บไว้สำรอง)
New-Item -ItemType Directory -Force -Path ".\archived_scripts"

# ย้ายแทนการลบ (ปลอดภัยกว่า)
Move-Item -Path "test_*.py", "check_*.py", "add_*.py", "clean_*.py", "change_*.py", "complete_*.py", "find_*.py", "inspect_*.py", "SUMMARY_*.py" -Destination ".\archived_scripts"
```

### วิธีที่ 3: ลบไฟล์ใน temp_file_report
```powershell
# ลบไฟล์ชั่วคราวทั้งหมด (เก็บแค่โฟลเดอร์)
Remove-Item .\temp_file_report\* -Recurse -Force
```

---

## สรุป

**ลบได้เลย: 19 ไฟล์** = ประหยัดพื้นที่และทำให้โปรเจกต์สะอาด
**เก็บไว้: 4 ไฟล์ + โฟลเดอร์สำคัญ** = รักษาฟังก์ชันสำคัญไว้
