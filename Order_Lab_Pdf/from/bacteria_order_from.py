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

# --- Config & Font Setup ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..')) 
fonts_folder = os.path.join(project_root, 'fonts')

# ตรวจสอบว่ามีโฟลเดอร์จริงไหม
if not os.path.exists(fonts_folder):
    fonts_folder = os.path.join(current_dir, 'fonts')

# ชื่อไฟล์ฟอนต์
font_files = {
    'normal': 'TH Niramit AS.ttf',
    'bold': 'TH Niramit AS Bold.ttf',
    'italic': 'TH Niramit AS Italic.ttf',
    'bold_italic': 'TH Niramit AS Bold Italic.ttf'
}

font_path_normal = os.path.join(fonts_folder, font_files['normal'])

if os.path.exists(font_path_normal):
    try:
        # ลงทะเบียนฟอนต์ทั้ง 4 แบบ
        pdfmetrics.registerFont(TTFont('THNiramitAS', os.path.join(fonts_folder, font_files['normal'])))
        pdfmetrics.registerFont(TTFont('THNiramitAS-Bold', os.path.join(fonts_folder, font_files['bold'])))
        pdfmetrics.registerFont(TTFont('THNiramitAS-Italic', os.path.join(fonts_folder, font_files['italic'])))
        pdfmetrics.registerFont(TTFont('THNiramitAS-BoldItalic', os.path.join(fonts_folder, font_files['bold_italic'])))
        
        # จับกลุ่มรวมเป็น Family
        from reportlab.lib.fonts import addMapping
        addMapping('THNiramitAS', 0, 0, 'THNiramitAS')
        addMapping('THNiramitAS', 1, 0, 'THNiramitAS-Bold')
        addMapping('THNiramitAS', 0, 1, 'THNiramitAS-Italic')
        addMapping('THNiramitAS', 1, 1, 'THNiramitAS-BoldItalic')
        
        print(f"✅ Registered Font Family: THNiramitAS (Bacteria)")
    except Exception as e:
        print(f"❌ Error registering font: {e}")
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
def create_bacteriology(sample_detail, data, output_file):
    left_margin = 0.5 * inch
    right_margin = 0.5 * inch
    top_margin = 0.25 * inch
    bottom_margin = 0.25 * inch

    pdf_file = SimpleDocTemplate(output_file, pagesize=A4,
                                 leftMargin=left_margin, rightMargin=right_margin,
                                 topMargin=top_margin, bottomMargin=bottom_margin)

    elements = []
    
    # ใช้ logo ที่อยู่ในโฟลเดอร์เดียวกัน: Order_Lab_Pdf/from/logo/logo.jpg
    current_dir = os.path.dirname(__file__)
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
        [logo_img, 'ใบคำขอรับบริการทดสอบแบคทีเรียวิทยาและราวิทยา', ''],
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

    # Sample Detail
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
        ('FONTSIZE', (0, 0), (-1, -1), 12), # ปรับจาก 14 ให้เท่ากัน
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(sample_tbl)
    elements.append(Spacer(1, 20))

    # --- Section 1: รายละเอียดการทดสอบ (3:66) ---
    elements.append(Paragraph("รายละเอียดการทดสอบ", set_paragraph_h1_style()))
    elements.append(Spacer(1, 12))
    
    test_data = data[0][3:66]
    test_detail = [test_data[i:i+3] for i in range(0, len(test_data), 3)]
    test_list = []
    idx = 1
    for test in test_detail:
        if len(test) > 0 and test[1] != 0:
            test_list.append([str(idx), test[0], test[2]]) # ใช้ test[2] ตามต้นฉบับ
            idx += 1
    
    test_list.insert(0, ['ลำดับ', 'ชื่อการทดสอบ', 'จำนวนตัวอย่างที่ตรวจ'])
    col_widths = [40, 230, 230]
    tbl1 = Table(test_list, colWidths=col_widths)
    tbl1.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS' if 'THNiramitAS' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ]))
    elements.append(tbl1)
    
    elements.append(Spacer(1, 25))
    elements.append(HRFlowable(width="100%", thickness=1, color="black", spaceBefore=10, spaceAfter=10))

    # --- Section 2: ความไวของยา (66:148) ---
    elements.append(Paragraph("ทดสอบความไวของยา", set_paragraph_h1_style()))
    elements.append(Spacer(1, 15))
    
    drug_data = data[0][66:148]
    drug_detail = [drug_data[i:i+2] for i in range(0, len(drug_data), 2)]
    drug_list = []
    idx = 1
    for test in drug_detail:
        if len(test) > 0 and test[1] != 0:
            drug_list.append([str(idx), test[0]])
            idx += 1
            
    drug_list.insert(0, ['ลำดับ', 'รายการ'])
    col_widths = [40, 150]
    tbl2 = Table(drug_list, colWidths=col_widths, hAlign='LEFT')
    tbl2.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS' if 'THNiramitAS' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ]))
    elements.append(tbl2)

    # --- Section 3: การระบุแบคทีเรีย (148:172) ---
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("การระบุแบคทีเรีย", set_paragraph_h1_style()))
    elements.append(Spacer(1, 15))

    bac_data = data[0][148:172]
    bac_detail = [bac_data[i:i+2] for i in range(0, len(bac_data), 2)]
    bac_list = []
    idx = 1
    for test in bac_detail:
        if len(test) > 0 and test[1] != 0:
            bac_list.append([str(idx), test[0]])
            idx += 1
            
    bac_list.insert(0, ['ลำดับ', 'รายการ'])
    tbl3 = Table(bac_list, colWidths=[40, 150], hAlign='LEFT')
    tbl3.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS' if 'THNiramitAS' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ]))
    elements.append(tbl3)

    # --- Section 4: LAB REQUEST (172:187) ---
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("LABORATORY REQUEST FOR", set_paragraph_h1_style()))
    elements.append(Spacer(1, 15))

    req_data = data[0][172:187]
    req_detail = [req_data[i:i+3] for i in range(0, len(req_data), 3)]
    req_list = []
    idx = 1
    for test in req_detail:
        if len(test) > 0 and test[1] != 0:
            req_list.append([str(idx), test[0]])
            idx += 1
            
    req_list.insert(0, ['ลำดับ', 'รายการ'])
    tbl4 = Table(req_list, colWidths=[40, 180], hAlign='LEFT')
    tbl4.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS' if 'THNiramitAS' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ]))
    elements.append(tbl4)

    # Footer
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
    # Mock Sample Data
    mock_sample = ["" for _ in range(30)]
    mock_sample[0] = "2023-11-15"
    mock_sample[25] = "99002"
    mock_sample[20] = "Swab"
    mock_sample[19] = "Amoxy"
    mock_sample[17] = "เร่งด่วน"
    mock_sample[16] = "แช่เย็น"
    
    # Mock Test Data (Total Length > 187)
    mock_tests = [0] * 3
    
    # 1. Main Tests (3:66 -> 63 items -> 21 rows of 3)
    for i in range(21):
        if i < 2: 
            mock_tests.extend([f"Bacteria Test {i+1}", 1, 5]) # Name, State, Amount
        else:
            mock_tests.extend(["", 0, 0])
            
    # 2. Drug Sens (66:148 -> 82 items -> 41 rows of 2)
    for i in range(41):
        if i < 3:
            mock_tests.extend([f"Drug {i+1}", 1])
        else:
            mock_tests.extend(["", 0])
            
    # 3. Bacteria ID (148:172 -> 24 items -> 12 rows of 2)
    for i in range(12):
        if i < 1:
            mock_tests.extend([f"E. Coli", 1])
        else:
            mock_tests.extend(["", 0])
            
    # 4. Lab Req (172:187 -> 15 items -> 5 rows of 3)
    for i in range(5):
        if i < 1:
            mock_tests.extend([f"Extra Lab", 1, 100])
        else:
            mock_tests.extend(["", 0, 0])

    output_filename = "test_bacteria_report.pdf"
    create_bacteriology([mock_sample], [mock_tests], output_filename)