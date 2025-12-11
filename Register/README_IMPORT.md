# Import Structure สำหรับโปรแกรม Register

## โครงสร้างโฟลเดอร์

```
d:\CVDTT_CM\
├── BACKEND\              # Backend ใช้ร่วมกัน
├── SERVICES_REGISTER\    # Services ใช้ร่วมกัน
├── Order_Lab_Pdf\        # PDF Generation ใช้ร่วมกัน
├── fonts\                # Fonts ใช้ร่วมกัน
└── Register\             # โปรแกรม Register
    ├── App.py           # Main entry point
    ├── App.bat          # Windows batch file
    ├── Reg.vbs          # Windows VBScript launcher
    ├── Controller\      # Controllers
    ├── View\            # Views
    ├── UI\              # UI files
    ├── barcode_utils\   # Barcode utilities
    ├── ICON\            # Icons
    └── PiC\             # Pictures
```

## การ Import ที่ถูกต้อง

### 1. **App.py** (Main Entry Point)
```python
import sys
import os

# เพิ่ม parent directory เพื่อให้สามารถ import shared modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # CVDTT_CM folder
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# ตอนนี้สามารถ import ได้แล้ว:
from Controller.main_controller import MainController
from SERVICES_REGISTER.auth_service import AuthService
from Order_Lab_Pdf.pdf_from import bacteria_order_from
```

### 2. **Controller Files**
Import modules ภายใน Register folder:
```python
from View.view_main_frame import MainWindow
from Controller.new_work_controller import NewWorkController
from barcode_utils.barcode_generator import BarcodeGenerator
```

Import shared modules (จาก parent):
```python
from SERVICES_REGISTER.auth_service import AuthService
from SERVICES_REGISTER.employee_service import EmployeeService
from Order_Lab_Pdf.pdf_from import bacteria_order_from
```

### 3. **View Files**
```python
from View.template_from_ui.main_frame import Ui_MainWindow
```

## วิธีการรันโปรแกรม

### Windows
```bash
# วิธีที่ 1: ใช้ batch file
cd d:\CVDTT_CM\Register
App.bat

# วิธีที่ 2: ใช้ VBScript (รันแบบ hidden)
Reg.vbs

# วิธีที่ 3: ใช้ Python โดยตรง
cd d:\CVDTT_CM\Register
python App.py
```

### การทดสอบ Import
```bash
cd d:\CVDTT_CM\Register
python -c "import sys; import os; sys.path.insert(0, '..'); from SERVICES_REGISTER.auth_service import AuthService; print('Import OK')"
```

## ไฟล์ที่แก้ไข

1. **d:\CVDTT_CM\Register\App.py**
   - เพิ่ม parent directory ลใน sys.path
   - ทำให้สามารถ import SERVICES_REGISTER และ Order_Lab_Pdf ได้

2. **d:\CVDTT_CM\Register\Reg.vbs**
   - แก้ไข hardcoded path
   - ใช้ dynamic path detection

## หมายเหตุ

- **SERVICES_REGISTER** และ **BACKEND** อยู่ที่ parent directory เพื่อให้โปรแกรมอื่นใช้ร่วมกันได้
- **Order_Lab_Pdf** อยู่ที่ parent directory เพื่อให้โปรแกรมอื่นใช้ร่วมกันได้
- **fonts** อยู่ที่ parent directory สำหรับ PDF generation
- ทุก Controller และ View files ใช้ relative import สำหรับ modules ภายใน Register
- App.py จะเพิ่ม parent path ให้อัตโนมัติเมื่อเริ่มโปรแกรม

## การ Deploy

เมื่อต้องการ deploy ให้แน่ใจว่า:
1. โครงสร้างโฟลเดอร์ยังคงเหมือนเดิม
2. ไม่ใช้ absolute path ใน code
3. รันจาก Register folder เสมอ

## 🧪 วิธีทดสอบ

### ทดสอบการ Import
```bash
cd d:\CVDTT_CM\Register
python test_imports.py
```

### ทดสอบการหา Fonts
```bash
cd d:\CVDTT_CM\Register
python test_fonts.py
```

### ทดสอบการหา Logo Path
```bash
cd d:\CVDTT_CM\Register
python test_logo_path.py
```

## 🔧 การแก้ไขปัญหา

### ปัญหา: Font file not found

PDF generators จะค้นหา fonts folder ตามลำดับ:
1. `d:\CVDTT_CM\fonts\` (ปกติ)
2. `d:\CVDTT_CM\fonts\` (จาก Register)
3. `Order_Lab_Pdf\pdf_from\fonts\` (fallback)

**ไฟล์ที่ต้องมีใน fonts folder:**
- TH Niramit AS.ttf
- TH Niramit AS Bold.ttf
- TH Niramit AS Italic.ttf
- TH Niramit AS Bold Italic.ttf

**วิธีแก้:**
1. ตรวจสอบว่า `d:\CVDTT_CM\fonts\` มีไฟล์ fonts หรือไม่
2. ถ้าไม่มี ให้คัดลอก fonts folder ไปวางที่ `d:\CVDTT_CM\fonts\`
3. รัน `python test_fonts.py` เพื่อทดสอบ

### ปัญหา: Logo ไม่แสดงใน PDF

PDF generators จะค้นหา logo folder ตามลำดับ:
1. `Order_Lab_Pdf/pdf_from/logo/` (ตำแหน่งเดียวกับไฟล์)
2. `d:\CVDTT_CM\Order_Lab_Pdf\pdf_from\logo\` (จาก CVDTT_CM root)
3. `d:\CVDTT_CM\Order_Lab_Pdf\pdf_from\logo\` (จาก Register)

**ไฟล์ที่ต้องมีใน logo folder:**
- logo.jpg
- group.png

**วิธีแก้:**
1. ตรวจสอบว่า `d:\CVDTT_CM\Order_Lab_Pdf\pdf_from\logo\` มีไฟล์ logo หรือไม่
2. ถ้าไม่มี ให้คัดลอก logo folder ไปวางที่ `d:\CVDTT_CM\Order_Lab_Pdf\pdf_from\logo\`
3. รัน `python test_logo_path.py` เพื่อทดสอบ
4. หาก PDF แสดง warning "logo not found" ให้ตรวจสอบ path
