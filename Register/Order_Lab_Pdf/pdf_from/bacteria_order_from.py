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
from reportlab.lib.fonts import addMapping

# [FIX] Import Barcode Factory
from reportlab.graphics.barcode import createBarcodeDrawing

# --- Config & Font Setup ---
# Support both development and compiled executable (Nuitka, PyInstaller)
def get_base_path():
    """Get base path for resources - works with Nuitka and PyInstaller"""
    # For Nuitka
    if '__compiled__' in globals():
        # Nuitka compiled - use executable directory
        return os.path.dirname(os.path.abspath(sys.argv[0]))
    # For PyInstaller
    elif getattr(sys, 'frozen', False):
        # PyInstaller - use _MEIPASS
        return getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(sys.argv[0])))
    # For normal Python
    else:
        # Development mode
        return os.path.dirname(os.path.abspath(__file__))

base_path = get_base_path()

# Try multiple paths to find fonts folder
fonts_folder_candidates = [
    # For Nuitka/PyInstaller - fonts in same dir as exe
    os.path.join(base_path, 'fonts'),
    # For Nuitka/PyInstaller - fonts in parent dir
    os.path.join(os.path.dirname(base_path), 'fonts'),
    # For development - Register/fonts
    os.path.join(base_path, '..', '..', 'fonts'),
    # For development - CVDTT_CM/fonts (legacy)
    os.path.join(base_path, '..', '..', '..', 'fonts'),
    # Fallback to script directory
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'fonts'),
]

fonts_folder = None
for candidate in fonts_folder_candidates:
    candidate = os.path.abspath(candidate)
    test_font = os.path.join(candidate, 'TH Niramit AS.ttf')
    if os.path.exists(test_font):
        fonts_folder = candidate
        # print(f"✓ Fonts found at: {fonts_folder}")
        break

if fonts_folder is None:
    # Final fallback
    fonts_folder = os.path.join(base_path, 'fonts')
    print(f"⚠ Font folder not found, using fallback: {fonts_folder}")

font_files = {
    'normal': 'TH Niramit AS.ttf',
    'bold': 'TH Niramit AS Bold.ttf',
    'italic': 'TH Niramit AS Italic.ttf',
    'bold_italic': 'TH Niramit AS Bold Italic.ttf'
}

font_path_normal = os.path.join(fonts_folder, font_files['normal'])

if os.path.exists(font_path_normal):
    try:
        pdfmetrics.registerFont(TTFont('THNiramitAS', os.path.join(fonts_folder, font_files['normal'])))
        pdfmetrics.registerFont(TTFont('THNiramitAS-Bold', os.path.join(fonts_folder, font_files['bold'])))
        pdfmetrics.registerFont(TTFont('THNiramitAS-Italic', os.path.join(fonts_folder, font_files['italic'])))
        pdfmetrics.registerFont(TTFont('THNiramitAS-BoldItalic', os.path.join(fonts_folder, font_files['bold_italic'])))
        
        addMapping('THNiramitAS', 0, 0, 'THNiramitAS')
        addMapping('THNiramitAS', 1, 0, 'THNiramitAS-Bold')
        addMapping('THNiramitAS', 0, 1, 'THNiramitAS-Italic')
        addMapping('THNiramitAS', 1, 1, 'THNiramitAS-BoldItalic')
    except Exception as e:
        print(f"Error registering font: {e}")
else:
    print(f"Font file not found at: {font_path_normal}")

def set_paragraph_h1_style():
    styles = getSampleStyleSheet()
    style = styles['BodyText']
    try: style.fontName = 'THNiramitAS-Bold'
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

HEADER_COLOR = colors.HexColor('#E8F4F8')

# [FIX] Helper Function: No Human Readable, Adjusted Height
def get_barcode_drawing(value, height=10*mm):
    try:
        val_str = str(value).strip()
        if not val_str or val_str.lower() == 'none': return Spacer(1, height)
        # humanReadable=False
        d = createBarcodeDrawing('Code128', value=val_str, barHeight=height, barWidth=1.2, humanReadable=False)
        return d
    except Exception as e:
        print(f"Barcode Error: {e}")
        return Paragraph("", set_paragraph_style())

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
    
    info = sample_detail[0] if sample_detail else [""]*30
    date_val = str(info[0]).replace('T', ' ') if info[0] else ""
    raw_barcode = info[25]
    if raw_barcode is None: raw_barcode = ""
    barcode_val = str(raw_barcode).zfill(12)

    # Logo - ใช้ 2 logo วางข้างๆ กัน
    logo_dir = os.path.join(os.path.dirname(__file__), "logo")
    logo1_path = os.path.join(logo_dir, "logo.jpg")
    logo2_path = os.path.join(logo_dir, "group.png")
    
    # สร้าง logo images ขนาดเท่ากัน
    logo1_img = ""
    logo2_img = ""
    logo_height = 1.0 * inch  # กำหนดความสูงเท่ากัน
    
    if os.path.exists(logo1_path):
        # logo.jpg เป็นสี่เหลี่ยมจัตุรัส
        logo1_img = Image(logo1_path, width=logo_height, height=logo_height)
    
    if os.path.exists(logo2_path):
        # group.png ปรับให้มีความสูงเท่ากันและให้ aspect ratio คงที่
        logo2_img = Image(logo2_path, width=logo_height, height=logo_height)
    
    # สร้างตารางสำหรับวาง logo 2 อัน
    logo_data = [[logo1_img, logo2_img]]
    logo_table = Table(logo_data, colWidths=[1.05*inch, 1.05*inch])
    logo_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    barcode_obj = get_barcode_drawing(barcode_val)

    title_data = [
        [logo_table, 'ใบคำขอรับบริการทดสอบแบคทีเรียวิทยาและราวิทยา', barcode_obj],
        ['', Paragraph("ศูนย์ชันสูตรโรคสัตว์และถ่ายทอดเทคโนโลยี คณะสัตวแพทยศาสตร์ มหาวิทยาลัยเชียงใหม่ <br/> (Center of Veterinary Diagnosis and Technology Transfer) <br/> Tel. 053-948041 Mobile 094-6362641 <br/> E-mail vet_diag@cmu.ac.th", set_paragraph_style()), ''],
    ]
    col_widths = [130, 243, 150]  # ปรับเพิ่มขนาดคอลัมน์ logo เป็น 130
    table = Table(title_data, colWidths=col_widths, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),
        ('FONTSIZE', (1, 0), (1, 1), 20),
        ('FONTSIZE', (1, 1), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (0, 0), (0, 1)),
        ('SPAN', (2, 0), (2, 1)), 
        ('ALIGN', (2, 0), (2, 1), 'CENTER'),
        ('ALIGN', (0, 0), (0, 1), 'CENTER'),
        
        # [FIX] ขยับบาร์โค้ดลงมา ไม่ให้ทับตัวหนังสือ
        ('VALIGN', (2, 0), (2, 1), 'BOTTOM'), 
        ('BOTTOMPADDING', (2, 0), (2, 1), 5), 
        ('TOPPADDING', (2, 0), (2, 1), 15), 
        
        ('PADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 15))

    # Sample Detail
    elements.append(Paragraph("รายละเอียดสิ่งส่งตรวจ", set_paragraph_h1_style()))
    elements.append(Spacer(1, 12))
    
    detail_info = [
        ['วันที่รับตัวอย่าง', date_val, 'Barcode', barcode_val],
        ['สิ่งที่ส่งมาตรวจ', info[20], 'ประวัติการให้ยา', info[19]],
        ['สถานะการตอบผล', info[17], 'การเก็บรักษาตัวอย่าง', info[16]],
    ]
    col_widths = [95, 166.5, 95, 166.5] 
    sample_tbl = Table(detail_info, colWidths=col_widths, hAlign='LEFT')
    sample_tbl.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    elements.append(sample_tbl)
    elements.append(Spacer(1, 20))

    # Part 1: Details
    elements.append(Paragraph("รายละเอียดการทดสอบ", set_paragraph_h1_style()))
    elements.append(Spacer(1, 10))
    
    test_list = []
    if data and len(data) > 0:
        test_data = data[0][3:66]
        test_detail = [test_data[i:i+3] for i in range(0, len(test_data), 3)]
        idx = 1
        for test in test_detail:
            if len(test) > 0 and test[1] != 0:
                test_list.append([str(idx), test[0], test[2]])
                idx += 1
    
    test_list.insert(0, ['ลำดับ', 'ชื่อการทดสอบ', 'จำนวนตัวอย่างที่ตรวจ'])
    
    tbl1 = Table(test_list, colWidths=[40, 333, 150], hAlign='LEFT')
    tbl1.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'), 
        ('ALIGN', (0, 0), (0, -1), 'CENTER'), 
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
        ('FONTNAME', (0, 0), (-1, 0), 'THNiramitAS-Bold'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(tbl1)
    
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=1, color="black", spaceBefore=5, spaceAfter=5))

    # Part 2: Drug Sens
    elements.append(Paragraph("ทดสอบความไวของยา", set_paragraph_h1_style()))
    elements.append(Spacer(1, 10))
    
    active_drugs = []
    if data and len(data) > 0:
        drug_data = data[0][66:148]
        raw_drug_list = [drug_data[i:i+2] for i in range(0, len(drug_data), 2)]
        idx = 1
        for test in raw_drug_list:
            if len(test) > 0 and test[1] != 0:
                active_drugs.append([str(idx), test[0]])
                idx += 1

    two_col_drugs = []
    two_col_drugs.append(['ลำดับ', 'รายการ', 'ลำดับ', 'รายการ']) 
    
    if len(active_drugs) > 0:
        for i in range(0, len(active_drugs), 2):
            item1 = active_drugs[i]
            if i + 1 < len(active_drugs):
                item2 = active_drugs[i+1]
                two_col_drugs.append([item1[0], item1[1], item2[0], item2[1]])
            else:
                two_col_drugs.append([item1[0], item1[1], '', ''])
    else:
        two_col_drugs.append(['', '', '', ''])

    # Calculated to fit 523
    drug_col_widths = [35, 226.5, 35, 226.5] 
    
    tbl2 = Table(two_col_drugs, colWidths=drug_col_widths, hAlign='LEFT')
    tbl2.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
        ('FONTNAME', (0, 0), (-1, 0), 'THNiramitAS-Bold'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(tbl2)
    elements.append(Spacer(1, 20))

    # Part 3 & 4: Side-by-Side
    bac_list = [['ลำดับ', 'การระบุแบคทีเรีย']]
    if data and len(data) > 0:
        bac_data = data[0][148:172]
        bac_raw = [bac_data[i:i+2] for i in range(0, len(bac_data), 2)]
        idx = 1
        for test in bac_raw:
            if len(test) > 0 and test[1] != 0:
                bac_list.append([str(idx), test[0]])
                idx += 1
            
    req_list = [['ลำดับ', 'LABORATORY REQUEST FOR']]
    if data and len(data) > 0:
        req_data = data[0][172:187]
        req_raw = [req_data[i:i+3] for i in range(0, len(req_data), 3)]
        idx = 1
        for test in req_raw:
            if len(test) > 0 and test[1] != 0:
                req_list.append([str(idx), test[0]])
                idx += 1
    
    if len(bac_list) == 1: bac_list.append(['', ''])
    if len(req_list) == 1: req_list.append(['', ''])

    sub_col_widths = [35, 220]
    sub_tbl_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
        ('FONTNAME', (0, 0), (-1, 0), 'THNiramitAS-Bold'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'), 
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ])

    t_bac = Table(bac_list, colWidths=sub_col_widths)
    t_bac.setStyle(sub_tbl_style)

    t_req = Table(req_list, colWidths=sub_col_widths)
    t_req.setStyle(sub_tbl_style)

    p_bac = Paragraph("การระบุแบคทีเรีย", set_paragraph_h1_style())
    p_req = Paragraph("LABORATORY REQUEST FOR", set_paragraph_h1_style())
    
    container_data = [
        [p_bac, '', p_req],
        [t_bac, '', t_req]
    ]
    
    container_table = Table(container_data, colWidths=[255, 13, 255], hAlign='LEFT')
    container_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ]))
    
    elements.append(container_table)

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

if __name__ == "__main__":
    mock_sample = ["" for _ in range(30)]
    mock_sample[0] = "2023-11-15 10:30:00"
    mock_sample[25] = "0000001542"
    mock_sample[20] = "Swab"
    mock_sample[19] = "Amoxy"
    mock_sample[17] = "เร่งด่วน"
    mock_sample[16] = "แช่เย็น"
    
    mock_tests = [0] * 3
    for i in range(5): mock_tests.extend([f"Test {i+1}", 1, 100])
    while len(mock_tests) < 187: mock_tests.extend(["", 0, 0])

    output_filename = "test_bacteria_final.pdf"
    create_bacteriology([mock_sample], [mock_tests], output_filename)