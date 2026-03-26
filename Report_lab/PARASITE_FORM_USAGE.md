# คำแนะนำการติดตั้งและใช้งาน Parasite Form System

## ขั้นตอนการติดตั้ง

### 1. ติดตั้ง Python Packages ที่จำเป็น

```bash
pip install python-docx
```

### 2. สร้างตาราง report_form ใน Database

รันคำสั่ง SQL จากไฟล์ `create_report_form_table.sql` ใน MariaDB:

```bash
mysql -u root -p cvdtt_lab < create_report_form_table.sql
```

หรือเข้า phpMyAdmin/HeidiSQL แล้ว import ไฟล์ SQL

### 3. รัน Backend API Server

```bash
cd BACKEND
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. รัน Report Lab Application

```bash
cd Report_lab
python App.py
```

## วิธีการใช้งาน Parasite Form

### 1. เลือกเคส (Lab Order)
- มองหา LAB ORDER ID ในรายการบาร์โค้ดทางซ้าย
- Double click หรือพิมพ์บาร์โค้ดในช่องค้นหา
- กดปุ่ม **"เลือกรายการนี้"** เพื่อยืนยันการเลือก

### 2. เลือกประเภทฟอร์ม
เลือก Radio Button:
- **Faces** - ฟอร์มสำหรับตรวจอุจจาระทั่วไป
- **Faces Dog Cat** - ฟอร์มสำหรับตรวจอุจจาระสุนัข/แมว
- **Blood** - ฟอร์มสำหรับตรวจเลือด
- **Identification** - ฟอร์มสำหรับระบุตัวตน

### 3. เลือกข้อมูลเพิ่มเติม (สำหรับ Faces และ Faces Dog Cat เท่านั้น)
- **Select Color**: เลือกสี (Black, Brown, Yellow, Green, Others)
- **Select Consistency**: เลือกความเหนียว (Hard, Formed, Soft, Mushy, Loose, Diarrhoeic, Watery)
- **Select Method**: เลือกวิธีการตรวจ (Flotation, Sedimentation, Others)

### 4. แสดงตัวอย่างฟอร์ม
- กดปุ่ม **"FORM PREVIEW"**
- ระบบจะเติมข้อมูลอัตโนมัติ:
  - **เลขที่ตัวอย่าง**: รูปแบบ D{วัน}-{lab_order_id} (เช่น D22-1601)
  - **วันที่รับตัวอย่าง**: ดึงจาก case_registration
  - **เลขที่รายงาน**: เลข ID ถัดไปจาก report_form table
  - ข้อมูล dropdown ที่เลือกไว้
- ฟอร์มจะแสดงเป็น PDF ในหน้าจอ

### 5. บันทึกฟอร์ม
- กดปุ่ม **"บันทึก"**
- เลือกตำแหน่งที่ต้องการบันทึกไฟล์
- ไฟล์จะถูกบันทึกเป็น **.docx** (สามารถแก้ไขได้)
- ตำแหน่งไฟล์จะถูกบันทึกลง database (report_form table)

## โครงสร้างข้อมูลที่เติมในฟอร์ม

### ข้อมูลที่เติมอัตโนมัติ:
1. **เลขที่รายงาน** - จาก report_form.id (auto increment)
2. **เลขที่ตัวอย่าง** - รูปแบบ D{day}-{lab_order_id}
   - D22 = วันที่ 22
   - 1601 = lab_order_id
3. **วันที่รับตัวอย่าง** - จาก case_registration.dtime
4. **Color, Consistency, Method** - จาก dropdown ที่เลือก

### ข้อมูลที่ผู้ใช้ต้องกรอกเอง:
- ชื่อสัตว์ (Animal name)
- ผลการตรวจ Parasite
- หมายเหตุอื่นๆ

## Database Schema

### Table: report_form
```sql
- id (INT, AUTO_INCREMENT) - เลขที่รายงาน
- dtime (TIMESTAMP) - วันที่สร้างรายงาน
- lab_order_id (INT) - รหัส Lab Order
- location (VARCHAR) - ที่อยู่ไฟล์ที่บันทึก
- comment (TEXT) - หมายเหตุ
- state (INT) - สถานะการทำงาน
- status (INT) - สถานะใช้งาน (1=active, 0=inactive)
- recorder (INT) - ผู้บันทึก (employee_id)
- approver (INT) - ผู้อนุมัติ (employee_id)
```

## API Endpoints ใหม่

### GET /report_form/latest_id
ดึง ID ล่าสุดเพื่อสร้างเลขที่รายงาน

### GET /report_form/by_lab_order/{lab_order_id}
ดึงข้อมูล report_form จาก lab_order_id

### POST /report_form/create
สร้าง report_form ใหม่

### PUT /report_form/update
อัพเดท report_form

### GET /report_form/lab_order_details/{lab_order_id}
ดึงข้อมูล lab_order พร้อม case_registration

## หมายเหตุ

- ฟอร์ม Word template ต้องมี placeholder เช่น {{เลขที่รายงาน}}, {{เลขที่ตัวอย่าง}}, {{วันที่รับตัวอย่าง}}
- ไฟล์ชั่วคราวจะถูกเก็บใน folder `temp_file_report`
- ไฟล์ที่บันทึกจะเป็น .docx เพื่อให้สามารถแก้ไขได้
- ควรสำรองฐานข้อมูลก่อนรัน SQL script
