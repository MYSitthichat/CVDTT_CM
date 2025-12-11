"""
ไฟล์ทดสอบการหา Logo Folder สำหรับ PDF Generation
"""

import os
import sys

# เพิ่ม parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

print("=" * 70)
print("ทดสอบการหา Logo Folder สำหรับ PDF")
print("=" * 70)

# Simulate from PDF generator perspective
pdf_from_dir = os.path.join(parent_dir, 'Order_Lab_Pdf', 'pdf_from')
print(f"\nSimulating from: {pdf_from_dir}")

# Test logo path candidates
logo_dir_candidates = [
    os.path.join(pdf_from_dir, "logo"),  # Same directory
    os.path.join(pdf_from_dir, "..", "..", "Order_Lab_Pdf", "pdf_from", "logo"),  # From CVDTT_CM
    os.path.join(pdf_from_dir, "..", "..", "..", "Order_Lab_Pdf", "pdf_from", "logo"),  # From Register
]

print("\nทดสอบ Logo Folder Candidates:")
print("-" * 70)

found_logo_dir = None
for i, candidate in enumerate(logo_dir_candidates, 1):
    abs_path = os.path.abspath(candidate)
    exists = os.path.exists(abs_path)
    
    # Check for logo files
    logo1 = os.path.join(abs_path, 'logo.jpg')
    logo2 = os.path.join(abs_path, 'group.png')
    logo1_exists = os.path.exists(logo1)
    logo2_exists = os.path.exists(logo2)
    
    status = "✓ FOUND" if exists and (logo1_exists or logo2_exists) else "✗ NOT FOUND"
    print(f"{i}. {status}")
    print(f"   Path: {abs_path}")
    print(f"   Folder Exists: {exists}")
    print(f"   logo.jpg: {'✓' if logo1_exists else '✗'}")
    print(f"   group.png: {'✓' if logo2_exists else '✗'}")
    
    if exists and (logo1_exists or logo2_exists) and found_logo_dir is None:
        found_logo_dir = abs_path
        print(f"   >>> SELECTED! <<<")
    print()

print("=" * 70)
if found_logo_dir:
    print(f"✓ Logo folder พบที่: {found_logo_dir}")
    
    # List all logo files
    try:
        logo_files = [f for f in os.listdir(found_logo_dir) if f.lower().endswith(('.jpg', '.png', '.gif'))]
        print(f"\nพบ Logo Files ({len(logo_files)} files):")
        for logo in sorted(logo_files):
            print(f"  - {logo}")
    except Exception as e:
        print(f"Error listing logos: {e}")
else:
    print("✗ ไม่พบ logo folder!")
    print("\nกรุณาตรวจสอบว่า logo folder อยู่ที่:")
    print("  d:\\CVDTT_CM\\Order_Lab_Pdf\\pdf_from\\logo\\")
    print("\nและมีไฟล์:")
    print("  - logo.jpg")
    print("  - group.png")

print("=" * 70)

# Test importing PDF modules and checking their logo paths
print("\nทดสอบ Logo Path ใน PDF Generators:")
print("-" * 70)

try:
    # Simulate the logo path detection from bacteria_order_from
    current_file_dir = pdf_from_dir
    
    logo_dir_candidates = [
        os.path.join(current_file_dir, "logo"),
        os.path.join(current_file_dir, "..", "..", "Order_Lab_Pdf", "pdf_from", "logo"),
        os.path.join(current_file_dir, "..", "..", "..", "Order_Lab_Pdf", "pdf_from", "logo"),
    ]
    
    detected_logo_dir = None
    for candidate in logo_dir_candidates:
        candidate = os.path.abspath(candidate)
        if os.path.exists(candidate):
            detected_logo_dir = candidate
            break
    
    if detected_logo_dir:
        print(f"✓ PDF Generator จะใช้ logo จาก:")
        print(f"  {detected_logo_dir}")
        
        logo1_path = os.path.join(detected_logo_dir, "logo.jpg")
        logo2_path = os.path.join(detected_logo_dir, "group.png")
        
        print(f"\n  logo.jpg: {'✓ พบ' if os.path.exists(logo1_path) else '✗ ไม่พบ'}")
        print(f"  group.png: {'✓ พบ' if os.path.exists(logo2_path) else '✗ ไม่พบ'}")
    else:
        print("✗ PDF Generator ไม่พบ logo folder!")
        
except Exception as e:
    print(f"✗ Error: {e}")

print("=" * 70)
print("\nกด Enter เพื่อปิด...")
input()
