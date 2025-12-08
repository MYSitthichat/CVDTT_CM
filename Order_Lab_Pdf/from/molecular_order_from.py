import os
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- Config & Font Setup (แก้ไขใหม่) ---
# 1. หาตำแหน่งโฟลเดอร์ fonts ให้เจอ (ถอยหลัง 2 ชั้นจาก Order_Lab_Pdf/from)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..')) 
fonts_folder = os.path.join(project_root, 'fonts')

# ตรวจสอบว่ามีโฟลเดอร์จริงไหม (เผื่อกรณี Test)
if not os.path.exists(fonts_folder):
    # ลองหาใน folder ปัจจุบันดูด้วย
    fonts_folder = os.path.join(current_dir, 'fonts')

# ชื่อไฟล์ตามภาพที่คุณส่งมา
font_files = {
    'normal': 'TH Niramit AS.ttf',
    'bold': 'TH Niramit AS Bold.ttf',
    'italic': 'TH Niramit AS Italic.ttf',
    'bold_italic': 'TH Niramit AS Bold Italic.ttf'
}

font_path_normal = os.path.join(fonts_folder, font_files['normal'])

if os.path.exists(font_path_normal):
    try:
        # 2. ลงทะเบียนฟอนต์ทั้ง 4 แบบ แยกชื่อกัน
        pdfmetrics.registerFont(TTFont('THNiramitAS', os.path.join(fonts_folder, font_files['normal'])))
        pdfmetrics.registerFont(TTFont('THNiramitAS-Bold', os.path.join(fonts_folder, font_files['bold'])))
        pdfmetrics.registerFont(TTFont('THNiramitAS-Italic', os.path.join(fonts_folder, font_files['italic'])))
        pdfmetrics.registerFont(TTFont('THNiramitAS-BoldItalic', os.path.join(fonts_folder, font_files['bold_italic'])))
        
        # 3. จับกลุ่มรวมเป็น Family เดียวกัน (แก้ปัญหา ValueError)
        from reportlab.lib.fonts import addMapping
        
        # บอก ReportLab ว่า 'THNiramitAS' ประกอบด้วยสมาชิกไหนบ้าง
        # (FamilyName, bold=0/1, italic=0/1, FontName)
        addMapping('THNiramitAS', 0, 0, 'THNiramitAS')            # Normal
        addMapping('THNiramitAS', 1, 0, 'THNiramitAS-Bold')       # Bold
        addMapping('THNiramitAS', 0, 1, 'THNiramitAS-Italic')     # Italic
        addMapping('THNiramitAS', 1, 1, 'THNiramitAS-BoldItalic') # Bold & Italic
        
        print(f"✅ Registered Font Family: THNiramitAS from {fonts_folder}")
        
    except Exception as e:
        print(f"❌ Error registering font: {e}")
        # ถ้า error ให้ลองปริ้น path ออกมาดู
        print(f"Attempted path: {font_path_normal}")
else:
    print(f"⚠️ Font file not found at: {font_path_normal}")


def set_paragraph_h1_style():
    styles = getSampleStyleSheet()
    style = styles['BodyText']
    try: style.fontName = 'THNiramitAS'
    except: pass
    style.fontSize = 16
    return style

def set_paragraph_style():
    styles = getSampleStyleSheet()
    style = styles['BodyText']
    try: style.fontName = 'THNiramitAS'
    except: pass
    style.fontSize = 12
    return style

# --- Main Logic ---
def create_molecular_biology(sample_detail, data, output_file):
    left_margin = 0.5 * inch
    right_margin = 0.5 * inch
    top_margin = 0.25 * inch
    bottom_margin = 0.25 * inch

    pdf_file = SimpleDocTemplate(output_file, pagesize=A4,
                                 leftMargin=left_margin, rightMargin=right_margin,
                                 topMargin=top_margin, bottomMargin=bottom_margin)

    elements = []
    
    # ใช้ logo ที่อยู่ในโฟลเดอร์เดียวกัน: Order_Lab_Pdf/from/logo/logo.jpg
    logo_folder = os.path.join(current_dir, "logo")
    cvdtt_logo = os.path.join(logo_folder, "logo.jpg")
    
    # ตรวจสอบว่าไฟล์มีอยู่จริง
    if os.path.exists(cvdtt_logo):
        logo_img = Image(cvdtt_logo, width=1.5*inch, height=1*inch)
        print(f"✅ Logo loaded from: {cvdtt_logo}")
    else:
        print(f"⚠️ Logo not found at {cvdtt_logo}")
        print(f"   Please ensure logo.jpg exists in: {logo_folder}")
        logo_img = ""

    title_data = [
        [logo_img, 'ใบคำขอรับบริการทดสอบอณูชีววิทยา', ''],
        ['', Paragraph("ศูนย์ชันสูตรโรคสัตว์และถ่ายทอดเทคโนโลยี คณะสัตวแพทยศาสตร์ มหาวิทยาลัยเชียงใหม่ <br/> (Center of Veterinary Diagnosis and Technology Transfer) <br/> Tel. 053-948041 Mobile 094-6362641 <br/> E-mail vet_diag@cmu.ac.th", set_paragraph_style()), ''],
    ]
    col_widths = [120, 320, 100]
    table = Table(title_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS' if 'THNiramitAS' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
        ('FONTSIZE', (1, 0), (1, 1), 20),
        ('FONTSIZE', (1, 1), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (0, 0), (0, 1)),
        ('PADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("รายละเอียดสิ่งส่งตรวจ", set_paragraph_h1_style()))
    elements.append(Spacer(1, 12))
    info = sample_detail[0]
    detail_info = [
        ['วันที่รับตัวอย่าง', info[0], 'Barcode', str(str(info[25]).zfill(10))],
        ['สิ่งที่ส่งมาตรวจ', info[20], 'ประวัติการให้ยา', info[19]],
        ['สถานะการตอบผล', info[17], 'การเก็บรักษาตัวอย่าง', info[16]],
    ]
    col_widths = [95, 155, 95, 155]
    sample_tbl = Table(detail_info, colWidths=col_widths)
    sample_tbl.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS' if 'THNiramitAS' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 14), # ตามต้นฉบับใช้ 14
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(sample_tbl)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("รายละเอียดการทดสอบ", set_paragraph_h1_style()))
    elements.append(Spacer(1, 12))

    # Test Data Logic (3:185)
    test_data = data[0][3:185]
    test_detail = [test_data[i:i+3] for i in range(0, len(test_data), 3)]
    
    test_list = []
    idx = 1
    for test in test_detail:
        if len(test) > 0 and test[1] != 0:
            test_list.append([str(idx), test[0], test[1]])
            idx += 1
            
    test_list.insert(0, ['ลำดับ', 'ชื่อการทดสอบ', 'จำนวนตัวอย่างที่ตรวจ'])
    col_widths = [40, 230, 230]
    tbl1 = Table(test_list, colWidths=col_widths)
    tbl1.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS' if 'THNiramitAS' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
    ]))
    elements.append(tbl1)

    elements.append(Spacer(1, 25))
    line = HRFlowable(width="100%", thickness=1, color="black", spaceBefore=10, spaceAfter=10)
    elements.append(line)
    elements.append(Paragraph("สำหรับห้องปฏิบัติการ", set_paragraph_h1_style()))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("ลงชื่อ.................................................... ผู้รับสิ่งส่งตรวจ", set_paragraph_style()))
    elements.append(Paragraph("วันที่............/............/............", set_paragraph_style()))
    elements.append(line)

    pdf_file.build(elements)
    print(f"✅ PDF Generated: {output_file}")

if __name__ == "__main__":
    # Mock Sample
    mock_sample = ["" for _ in range(30)]
    mock_sample[0] = "2023-12-01"
    mock_sample[25] = "99003"
    mock_sample[20] = "เลือด (EDTA)"
    mock_sample[19] = "-"
    mock_sample[17] = "ปกติ"
    mock_sample[16] = "แช่เย็น"

    # Mock Test Data (Size ~ 185)
    mock_tests = [0] * 3
    # 3:185 -> 182 items -> ~60 rows of 3
    for i in range(60):
        if i < 4:
            mock_tests.extend([f"PCR Test {i+1}", 1, 500])
        else:
            mock_tests.extend(["", 0, 0])
            
    output_filename = "test_molecular_report.pdf"
    create_molecular_biology([mock_sample], [mock_tests], output_filename)