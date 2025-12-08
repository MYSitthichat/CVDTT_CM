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
        
        print(f"✅ Registered Font Family: THNiramitAS (Parasite)")
    except Exception as e:
        print(f"❌ Error registering font: {e}")
else:
    print(f"⚠️ Font file not found at: {font_path_normal}")

# --- Helper Functions ---
def set_paragraph_h1_style():
    styles = getSampleStyleSheet()
    style = styles['BodyText']
    try:
        style.fontName = 'THNiramitAS'
    except: pass
    style.fontSize = 16
    return style

def set_paragraph_style():
    styles = getSampleStyleSheet()
    style = styles['BodyText']
    try:
        style.fontName = 'THNiramitAS'
    except: pass
    style.fontSize = 12
    return style

# --- Main Logic ---
def create_parasite_biology(sample_detail, data, output_file):
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
        [logo_img, 'ใบคำขอรับบริการทดสอบปรสิตวิทยา', ''],
        ['', Paragraph("ศูนย์ชันสูตรโรคสัตว์และถ่ายทอดเทคโนโลยี คณะสัตวแพทยศาสตร์ มหาวิทยาลัยเชียงใหม่ <br/> (Center of Veterinary Diagnosis and Technology Transfer) <br/> Tel. 053-948041 Mobile 094-6362641 <br/> E-mail vet_diag@cmu.ac.th", set_paragraph_style()), ''],
    ]
    col_widths = [120, 320, 100]
    table = Table(title_data, colWidths=col_widths)
    style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS' if 'THNiramitAS' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
        ('FONTSIZE', (1, 0), (1, 1), 20),
        ('FONTSIZE', (1, 1), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (0, 0), (0, 1)),
        ('PADDING', (0, 0), (-1, -1), 0),
    ])
    table.setStyle(style)
    elements.append(table)
    
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("รายละเอียดสิ่งส่งตรวจ", set_paragraph_h1_style()))
    elements.append(Spacer(1, 12))
    
    # Sample Detail
    info = sample_detail[0]
    detail_info = [
        ['วันที่รับตัวอย่าง', info[0], 'Barcode', str(str(info[25]).zfill(10))],
        ['สิ่งที่ส่งมาตรวจ', info[20], 'ประวัติการให้ยา', info[19]],
        ['สถานะการตอบผล', info[17], 'การเก็บรักษาตัวอย่าง', info[16]],
    ]
    col_widths = [95, 155, 95, 155]
    sample_detail_table = Table(detail_info, colWidths=col_widths)
    sample_detail_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS' if 'THNiramitAS' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    sample_detail_table.setStyle(sample_detail_style)
    elements.append(sample_detail_table)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("รายละเอียดการทดสอบ", set_paragraph_h1_style()))
    elements.append(Spacer(1, 12))

    # Test Data logic (Slice 3:39)
    raw_test_data = data[0][3:39]
    test_detail = [raw_test_data[i:i+3] for i in range(0, len(raw_test_data), 3)]
    
    test_list = []
    idx = 1
    for test in test_detail:
        if len(test) > 0 and test[1] != 0: # test[1] is amount/state
            test_list.append([str(idx), test[0], test[1]])
            idx += 1

    test_list.insert(0, ['ลำดับ', 'ชื่อการทดสอบ', 'จำนวนตัวอย่างที่ตรวจ'])
    col_widths = [40, 230, 230]
    test_detail_table = Table(test_list, colWidths=col_widths)
    test_detail_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS' if 'THNiramitAS' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    test_detail_table.setStyle(test_detail_style)
    elements.append(test_detail_table)

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

# --- Mock Data & Runner ---
if __name__ == "__main__":
    # จำลองข้อมูล Sample Detail (Array ขนาดใหญ่อ้างอิงตาม index ที่ใช้ใน code)
    mock_sample = ["" for _ in range(30)]
    mock_sample[0] = "2023-10-25"    # Date
    mock_sample[25] = "99001"        # Barcode
    mock_sample[20] = "อุจจาระ"      # Type
    mock_sample[19] = "-"            # Drug History
    mock_sample[17] = "ปกติ"         # Status
    mock_sample[16] = "แช่เย็น"      # Storage
    
    sample_data_list = [mock_sample]

    # จำลองข้อมูล Test Data (ต้องมีขนาดพอดีกับ Slice 3:39 -> 36 elements)
    # Format: [Name, Amount, Price] เรียงต่อกัน
    mock_tests = [0] * 3 # Padding 3 ตัวแรก (0-2)
    
    # สร้างรายการทดสอบจำลอง 12 รายการ (12 * 3 = 36)
    tests_content = []
    for i in range(12):
        if i < 3: # สมมติว่าเลือกตรวจแค่ 3 รายการแรก
            tests_content.extend([f"การทดสอบปรสิต {i+1}", 1, 100])
        else:
            tests_content.extend(["", 0, 0])
            
    mock_tests.extend(tests_content)
    
    test_data_list = [mock_tests]

    output_filename = "test_parasite_report.pdf"
    create_parasite_biology(sample_data_list, test_data_list, output_filename)