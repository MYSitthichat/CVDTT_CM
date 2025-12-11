"""
ไฟล์ทดสอบการหา fonts folder
"""

import os
import sys

# เพิ่ม parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

print("=" * 70)
print("ทดสอบการหา Fonts Folder")
print("=" * 70)

# Simulate from PDF generator perspective
pdf_from_dir = os.path.join(parent_dir, 'Order_Lab_Pdf', 'pdf_from')
print(f"\nSimulating from: {pdf_from_dir}")

# Test font path candidates
fonts_folder_candidates = [
    os.path.join(pdf_from_dir, '..', '..', 'fonts'),  # CVDTT_CM/fonts
    os.path.join(pdf_from_dir, '..', '..', '..', 'fonts'),  # From Register -> CVDTT_CM/fonts
    os.path.join(pdf_from_dir, 'fonts'),  # Fallback
]

print("\nทดสอบ Fonts Folder Candidates:")
print("-" * 70)

found_fonts = None
for i, candidate in enumerate(fonts_folder_candidates, 1):
    abs_path = os.path.abspath(candidate)
    exists = os.path.exists(abs_path)
    
    # Check for font file
    test_font = os.path.join(abs_path, 'TH Niramit AS.ttf')
    font_exists = os.path.exists(test_font)
    
    status = "✓ FOUND" if exists and font_exists else "✗ NOT FOUND"
    print(f"{i}. {status}")
    print(f"   Path: {abs_path}")
    print(f"   Exists: {exists}")
    print(f"   Font File: {font_exists}")
    
    if exists and font_exists and found_fonts is None:
        found_fonts = abs_path
        print(f"   >>> SELECTED! <<<")
    print()

print("=" * 70)
if found_fonts:
    print(f"✓ Fonts folder พบที่: {found_fonts}")
    
    # List all fonts
    try:
        font_files = [f for f in os.listdir(found_fonts) if f.endswith('.ttf')]
        print(f"\nพบ Font Files ({len(font_files)} files):")
        for font in sorted(font_files):
            print(f"  - {font}")
    except Exception as e:
        print(f"Error listing fonts: {e}")
else:
    print("✗ ไม่พบ fonts folder!")
    print("\nกรุณาตรวจสอบว่า fonts folder อยู่ที่:")
    print("  d:\\CVDTT_CM\\fonts\\")

print("=" * 70)

# Test importing PDF modules
print("\nทดสอบ Import PDF Generators:")
print("-" * 70)

try:
    from Order_Lab_Pdf.pdf_from import bacteria_order_from
    print("✓ bacteria_order_from imported successfully")
except Exception as e:
    print(f"✗ bacteria_order_from import failed: {e}")

try:
    from Order_Lab_Pdf.pdf_from import molecular_order_from
    print("✓ molecular_order_from imported successfully")
except Exception as e:
    print(f"✗ molecular_order_from import failed: {e}")

try:
    from Order_Lab_Pdf.pdf_from import parasite_order_from
    print("✓ parasite_order_from imported successfully")
except Exception as e:
    print(f"✗ parasite_order_from import failed: {e}")

print("=" * 70)
print("\nกด Enter เพื่อปิด...")
input()
