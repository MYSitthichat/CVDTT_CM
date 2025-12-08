import os
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer, HRFlowable, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

# Import Barcode Factory
from reportlab.graphics.barcode import createBarcodeDrawing

# --- Config & Font Setup ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..')) 
fonts_folder = os.path.join(project_root, 'fonts')

if not os.path.exists(fonts_folder):
    fonts_folder = os.path.join(current_dir, 'fonts')

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
def get_barcode_drawing(value, height=10*mm): # ลดความสูงลงนิดหน่อย (10mm)
    try:
        val_str = str(value).strip()
        if not val_str or val_str.lower() == 'none':
            return Spacer(1, height)
            
        # humanReadable=False (เอาตัวเลขออก)
        d = createBarcodeDrawing('Code128', value=val_str, barHeight=height, barWidth=1.2, humanReadable=False)
        return d
    except Exception as e:
        print(f"Barcode Gen Error: {e}")
        return Paragraph("", set_paragraph_style())

# --- Helper: Category ---
def get_test_category(test_name):
    name = test_name.upper()
    if any(k in name for k in ['AI;', 'IBV', 'IBDV', 'ILT', 'NDV', 'PDD', 'PBFDV', 'CHLAMYDIA', 'PASTEURELLA', 'MG ']): return 'AVIAN (สัตว์ปีก)'
    if any(k in name for k in ['ANAPLASMA', 'BABESIA', 'EHRLICHIA', 'THEILERIA', 'HAEMOBARTONELLA', 'LEISHMANIA', 'TRYPANOSOMA', 'HEPATOZOON']): return 'BLOOD PARASITE (พยาธิในเลือด)'
    if any(k in name for k in ['FELV', 'FIP', 'FIV', 'PANLEUKOPENIA']): return 'FELINE (แมว)'
    if any(k in name for k in ['CDV', 'CPV']): return 'CANINE (สุนัข)'
    if any(k in name for k in ['EEHV']): return 'ELEPHANT (ช้าง)'
    if any(k in name for k in ['KHV', 'TILV', 'CEV']): return 'AQUATIC ANIMAL (สัตว์น้ำ)'
    if any(k in name for k in ['BLV', 'FMDV', 'LSDV', 'BVD']): return 'BOVINE (โค-กระบือ)'
    if any(k in name for k in ['CSF', 'PRRSV', 'PCV', 'PED']): return 'PORCINE (สุกร)'
    if any(k in name for k in ['EHV', 'AHS']): return 'EQUINE (ม้า)'
    return 'OTHERS (อื่นๆ/Molecular Biology)'

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
    
    info = sample_detail[0] if sample_detail else [""]*30
    date_val = str(info[0]).replace('T', ' ') if info[0] else ""
    raw_barcode = info[25]
    if raw_barcode is None: raw_barcode = ""
    barcode_val = str(raw_barcode).zfill(12)

    # Logo
    logo_candidates = [
        os.path.join(os.path.dirname(__file__), "logo", "logo.jpg"),
        os.path.join(os.path.dirname(__file__), "cvdtt_logo.png"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "Pic", "cvdtt_logo.png")
    ]
    logo_img = ""
    for logo_path in logo_candidates:
        if os.path.exists(logo_path):
            logo_img = Image(logo_path, width=1.5*inch, height=1*inch)
            break

    barcode_obj = get_barcode_drawing(barcode_val)

    title_data = [
        [logo_img, 'ใบคำขอรับบริการทดสอบอณูชีววิทยา', barcode_obj],
        ['', Paragraph("ศูนย์ชันสูตรโรคสัตว์และถ่ายทอดเทคโนโลยี คณะสัตวแพทยศาสตร์ มหาวิทยาลัยเชียงใหม่ <br/> (Center of Veterinary Diagnosis and Technology Transfer) <br/> Tel. 053-948041 Mobile 094-6362641 <br/> E-mail vet_diag@cmu.ac.th", set_paragraph_style()), ''],
    ]
    
    col_widths = [110, 263, 150]
    
    table = Table(title_data, colWidths=col_widths, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),
        ('FONTSIZE', (1, 0), (1, 1), 20),
        ('FONTSIZE', (1, 1), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        
        # Merge Logo
        ('SPAN', (0, 0), (0, 1)),
        
        # Merge Barcode
        ('SPAN', (2, 0), (2, 1)), 
        ('ALIGN', (2, 0), (2, 1), 'CENTER'),
        
        # [FIX] ขยับบาร์โค้ดลงมา (ใช้ BOTTOM หรือปรับ Padding)
        ('VALIGN', (2, 0), (2, 1), 'BOTTOM'), 
        ('BOTTOMPADDING', (2, 0), (2, 1), 5), # ดันขึ้นมาจากขอบล่างนิดนึง
        ('TOPPADDING', (2, 0), (2, 1), 15),   # ดันลงมาจากขอบบนเยอะๆ (แก้ทับตัวหนังสือ)
        
        ('PADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 15))

    # Extract Laboratory Request values from data
    # When using SELECT *, the structure is:
    # Index 0 = id, 1 = sample_id, 2 = dtime, 3-185 = test data (61 tests × 3)
    # Index 186 = cPCR_req, 187 = qPCR_req, 188 = extraction_req, 189 = status, 190 = updater
    lab_req_text = []
    if data and len(data) > 0:
        cPCR_req = data[0][186] if len(data[0]) > 186 else 0
        qPCR_req = data[0][187] if len(data[0]) > 187 else 0
        extraction_req = data[0][188] if len(data[0]) > 188 else 0
        
        if cPCR_req == 1:
            lab_req_text.append("cPCR")
        if qPCR_req == 1:
            lab_req_text.append("qPCR")
        if extraction_req == 1:
            lab_req_text.append("Extraction")
    
    lab_request_display = ", ".join(lab_req_text) if lab_req_text else "-"
    
    # Sample Detail
    elements.append(Paragraph("รายละเอียดสิ่งส่งตรวจ", set_paragraph_h1_style()))
    elements.append(Spacer(1, 12))
    
    detail_info = [
        ['วันที่รับตัวอย่าง', date_val, 'Barcode', barcode_val],
        ['สิ่งที่ส่งมาตรวจ', info[20], 'ประวัติการให้ยา', info[19]],
        ['สถานะการตอบผล', info[17], 'การเก็บรักษาตัวอย่าง', info[16]],
        ['Laboratory Request', lab_request_display, '', ''],
    ]
    col_widths = [95, 166.5, 95, 166.5] 
    sample_tbl = Table(detail_info, colWidths=col_widths, hAlign='LEFT')
    sample_tbl.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # Merge cells for Laboratory Request
        ('SPAN', (1, 3), (3, 3)),
        ('BACKGROUND', (0, 3), (0, 3), HEADER_COLOR),
        ('FONTNAME', (0, 3), (0, 3), 'THNiramitAS-Bold'),
    ]))
    elements.append(sample_tbl)
    elements.append(Spacer(1, 20))

    # Test Details (Grouped)
    elements.append(Paragraph("รายละเอียดการทดสอบ", set_paragraph_h1_style()))
    elements.append(Spacer(1, 10))

    raw_tests = []
    if data and len(data) > 0:
        test_data = data[0][3:185]
        test_chunks = [test_data[i:i+3] for i in range(0, len(test_data), 3)]
        for chunk in test_chunks:
            if len(chunk) > 1 and chunk[1] != 0:
                raw_tests.append({'name': str(chunk[0]), 'amount': chunk[1], 'price': chunk[2] if len(chunk) > 2 else 0})

    grouped_tests = {}
    category_order = ['AVIAN (สัตว์ปีก)', 'BLOOD PARASITE (พยาธิในเลือด)', 'FELINE (แมว)', 'CANINE (สุนัข)', 
                      'PORCINE (สุกร)', 'BOVINE (โค-กระบือ)', 'ELEPHANT (ช้าง)', 'AQUATIC ANIMAL (สัตว์น้ำ)', 
                      'EQUINE (ม้า)', 'OTHERS (อื่นๆ/Molecular Biology)']
    
    for t in raw_tests:
        cat = get_test_category(t['name'])
        if cat not in grouped_tests: grouped_tests[cat] = []
        grouped_tests[cat].append(t)

    global_idx = 1
    has_data = False
    
    for category in category_order:
        if category in grouped_tests and len(grouped_tests[category]) > 0:
            has_data = True
            
            # Header
            header_data = [[category]]
            header_tbl = Table(header_data, colWidths=[523], hAlign='LEFT')
            header_tbl.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#D1E8F5')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'), 
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10)
            ]))
            
            list_data = [['ลำดับ', 'ชื่อการทดสอบ', 'จำนวนตัวอย่างที่ตรวจ']]
            for item in grouped_tests[category]:
                list_data.append([str(global_idx), item['name'], str(item['amount'])])
                global_idx += 1
            
            content_tbl = Table(list_data, colWidths=[40, 333, 150], hAlign='LEFT')
            content_tbl.setStyle(TableStyle([
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
            
            elements.append(KeepTogether([header_tbl, content_tbl]))
            elements.append(Spacer(1, 15))

    if not has_data:
        elements.append(Paragraph("- ไม่มีรายการทดสอบ -", set_paragraph_style()))

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
    # Mock
    mock_sample = ["" for _ in range(30)]
    mock_sample[0] = "2025-12-08 13:25:42"
    mock_sample[25] = "0000001540"
    mock_sample[20] = "น้ำไขสันหลัง"
    mock_sample[19] = "-"
    mock_sample[17] = "ปกติ"
    mock_sample[16] = "แช่แข็ง (Freeze)"

    # Mock test data with proper structure to match database SELECT *
    # Structure: [id, sample_id, dtime, test1_name, test1_amount, test1_price, ..., cPCR_req, qPCR_req, extraction_req, status, updater]
    mock_tests = [1, 1540, "2025-12-08 13:25:42"]  # id, sample_id, dtime
    
    test_cases = [("NDV - cPCR", 2, 0), ("PDD", 2, 0), ("FeLV", 2, 0), ("FIP", 2, 0), ("CDV", 2, 0), ("Melioidosis", 2, 0)]
    for name, amt, price in test_cases: 
        mock_tests.extend([name, amt, price])
    
    # Fill remaining test slots (61 tests total, 6 used, 55 remaining)
    while len(mock_tests) < 186:  # 3 + (61 × 3) = 186
        mock_tests.extend(["", 0, 0])
    
    # Add Laboratory Request values: cPCR=1, qPCR=1, extraction=1
    mock_tests.extend([1, 1, 1])  # cPCR_req (186), qPCR_req (187), extraction_req (188)
    mock_tests.extend([1, 1])  # status (189), updater (190)
            
    output_filename = "test_molecular_final.pdf"
    create_molecular_biology([mock_sample], [mock_tests], output_filename)
    print(f"PDF generated: {output_filename}")
    print(f"Mock data length: {len(mock_tests)}")
    print(f"cPCR={mock_tests[186]}, qPCR={mock_tests[187]}, Extraction={mock_tests[188]}")