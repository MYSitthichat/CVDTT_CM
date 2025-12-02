import mariadb
import yaml
import os
import sys
import reportlab
# create a PDF file using reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Frame, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


current_dir = os.path.dirname(os.path.abspath(__file__)) # .../Order_detail
project_root = os.path.dirname(current_dir)              # .../cmu-lms
fonts_folder = os.path.join(project_root, 'fonts')

font_filename = 'THNiramitAS.ttf' 
font_path = os.path.join(fonts_folder, font_filename)

# print(f"--- FONT DEBUG ---")
# print(f"Looking for font at: {font_path}")

if os.path.exists(font_path):
    # File exists, register it
    try:
        pdfmetrics.registerFont(TTFont('THNiramitAS', font_path))
        # print("✅ Font registered successfully.")
    except Exception as e:
        print(f"❌ Error registering font: {e}")
else:
    # File does NOT exist, print available files to help debug
    # print(f"❌ ERROR: File not found.")
    if os.path.exists(fonts_folder):
        # print(f"Files actually found in '{fonts_folder}':")
        for file in os.listdir(fonts_folder):
            print(f" - {file}")
    else:
        print(f"❌ The folder '{fonts_folder}' does not exist.")
    
    # print("⚠️ Using default Helvetica as fallback.")
    
    
# print("------------------")

def create_parasite_biology(sample_detail, data, output_file):
    """This function is used to create the hematology test detail."""
    left_margin = 0.5 * inch
    right_margin = 0.5 * inch
    top_margin = 0.25 * inch
    bottom_margin = 0.25 * inch

    # Create a SimpleDocTemplate object with custom margins
    pdf_file = SimpleDocTemplate(output_file, pagesize=A4,
                                 leftMargin=left_margin, rightMargin=right_margin,
                                 topMargin=top_margin, bottomMargin=bottom_margin)

    elements = []
    cvdtt_logo = os.path.join(os.path.dirname(__file__), "cvdtt_logo.png")
    title_data = [
        [Image(cvdtt_logo, width=1.5*inch, height=1*inch),
         'ใบคำขอรับบริการทดสอบปรสิตวิทยา', ''],
        ['', Paragraph("ศูนย์ชันสูตรโรคสัตว์และถ่ายทอดเทคโนโลยี คณะสัตวแพทยศาสตร์ มหาวิทยาลัยเชียงใหม่ <br/> (Center of Veterinary Diagnosis and Technology Transfer) <br/> Tel. 053-948041 Mobile 094-6362641 <br/> E-mail vet_diag@cmu.ac.th", set_paragraph_style()), ''],
    ]
    col_widths = [120, 320, 100]  # Adjust the widths as needed
    # Create a table from the data
    table = Table(title_data, colWidths=col_widths)

    # Define the style for the table
    style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),  # Specify the font name
        ('FONTSIZE', (1, 0), (1, 1), 20),
        ('FONTSIZE', (1, 1), (-1, -1), 10),
        # Background color for the first row
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        # Center alignment for all cells
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # Middle vertical alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('SPAN', (1, 0), (1, 1)),
        ('SPAN', (0, 0), (0, 1)),
        # zero padding
        ('PADDING', (0, 0), (-1, -1), 0),
        # show grid
        # ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table.setStyle(style)

    # Add the table to the list of elements
    elements.append(table)
    # add space
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("รายละเอียดสิ่งส่งตรวจ",
                    set_paragraph_h1_style()))
    elements.append(Spacer(1, 12))
    # Add the sample detail
    sample_detail = sample_detail[0]
    # print(sample_detail)
    detail_info = [
        ['วันที่รับตัวอย่าง', sample_detail[0],
            'Barcode', str(str(sample_detail[25]).zfill(10))],
        ['สิ่งที่ส่งมาตรวจ', sample_detail[20],
            'ประวัติการให้ยา', sample_detail[19]],
        ['สถานะการตอบผล', sample_detail[17],
            'การเก็บรักษาตัวอย่าง', sample_detail[16]],
    ]
    col_widths = [95, 155, 95, 155]  # Adjust the widths as needed
    # Create sample detail table
    sample_detail_table = Table(detail_info, colWidths=col_widths)
    sample_detail_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),  # Specify the font name
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        # Background color for the first row
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        # Center alignment for all cells
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # Middle vertical alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # show grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    sample_detail_table.setStyle(sample_detail_style)
    elements.append(sample_detail_table)

    # add space
    elements.append(Spacer(1, 10))

    # add paragraph
    elements.append(Paragraph("รายละเอียดการทดสอบ", set_paragraph_h1_style()))
    elements.append(Spacer(1, 12))
    # add test detail

    test_data = data[0][3:39]

    # python reshape list from 1*183 to 61*3

    test_detail = [test_data[i:i+3] for i in range(0, len(test_data), 3)]

    test_list = []

    for i, test in enumerate(test_detail):
        if len(test) > 0 and test[1] != 0:
            # print(test)
            test_list.append([test[0], test[1]])

    test_detail = test_list
    test_list = []
    for i, test in enumerate(test_detail):
        if len(test) > 0 and test[1] != 0:
            test_list.append([str(i+1), test[0], test[1]])

    test_list.insert(0, ['ลำดับ', 'ชื่อการทดสอบ', 'จำนวนตัวอย่างที่ตรวจ'])
    col_widths = [40, 230, 230]  # Adjust the widths as needed
    # Create test detail table
    test_detail_table = Table(test_list, colWidths=col_widths)
    test_detail_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),  # Specify the font name
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        # Background color for the first row
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        # Center alignment for all cells
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        # Middle vertical alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # show grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    test_detail_table.setStyle(test_detail_style)
    elements.append(test_detail_table)

    # add paragraph for signature and date at the bottom
    # add horizontal line
    elements.append(Spacer(1, 25))
    line = HRFlowable(width="100%", thickness=1,
                      color="black", spaceBefore=10, spaceAfter=10)
    elements.append(line)
    elements.append(Paragraph("สำหรับห้องปฏิบัติการ",
                    set_paragraph_h1_style()))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph(
        "ลงชื่อ.................................................... ผู้รับสิ่งส่งตรวจ", set_paragraph_style()))
    elements.append(Paragraph(
        "วันที่............/............/............", set_paragraph_style()))
    elements.append(line)
    # # Build the PDF

    pdf_file.build(elements)


def create_bacteriology(sample_detail, data, output_file):
    """This function is used to create the bacteriology test detail."""
    left_margin = 0.5 * inch
    right_margin = 0.5 * inch
    top_margin = 0.25 * inch
    bottom_margin = 0.25 * inch

    # Create a SimpleDocTemplate object with custom margins
    pdf_file = SimpleDocTemplate(output_file, pagesize=A4,
                                 leftMargin=left_margin, rightMargin=right_margin,
                                 topMargin=top_margin, bottomMargin=bottom_margin)

    elements = []
    cvdtt_logo = os.path.join(os.path.dirname(__file__), "cvdtt_logo.png")
    title_data = [
        [Image(cvdtt_logo, width=1.5*inch, height=1*inch),
         'ใบคำขอรับบริการทดสอบแบคทีเรียวิทยาและราวิทยา', ''],
        ['', Paragraph("ศูนย์ชันสูตรโรคสัตว์และถ่ายทอดเทคโนโลยี คณะสัตวแพทยศาสตร์ มหาวิทยาลัยเชียงใหม่ <br/> (Center of Veterinary Diagnosis and Technology Transfer) <br/> Tel. 053-948041 Mobile 094-6362641 <br/> E-mail vet_diag@cmu.ac.th", set_paragraph_style()), ''],
    ]
    col_widths = [120, 320, 100]  # Adjust the widths as needed
    # Create a table from the data
    table = Table(title_data, colWidths=col_widths)

    # Define the style for the table
    style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),  # Specify the font name
        ('FONTSIZE', (1, 0), (1, 1), 20),
        ('FONTSIZE', (1, 1), (-1, -1), 10),
        # Background color for the first row
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        # Center alignment for all cells
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # Middle vertical alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('SPAN', (1, 0), (1, 1)),
        ('SPAN', (0, 0), (0, 1)),
        # zero padding
        ('PADDING', (0, 0), (-1, -1), 0),
        # show grid
        # ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table.setStyle(style)

    # Add the table to the list of elements
    elements.append(table)
    # add space
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("รายละเอียดสิ่งส่งตรวจ",
                    set_paragraph_h1_style()))
    elements.append(Spacer(1, 12))
    # Add the sample detail
    sample_detail = sample_detail[0]
    print((sample_detail))
    detail_info = [
        ['วันที่รับตัวอย่าง', sample_detail[0],
            'Barcode', str(str(sample_detail[25]).zfill(10))],
        ['สิ่งที่ส่งมาตรวจ', sample_detail[20],
            'ประวัติการให้ยา', sample_detail[19]],
        ['สถานะการตอบผล', sample_detail[17],
            'การเก็บรักษาตัวอย่าง', sample_detail[16]],
    ]
    col_widths = [95, 155, 95, 155]  # Adjust the widths as needed
    # Create sample detail table
    sample_detail_table = Table(detail_info, colWidths=col_widths)
    sample_detail_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),  # Specify the font name
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        # Background color for the first row
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        # Center alignment for all cells
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # Middle vertical alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # show grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    sample_detail_table.setStyle(sample_detail_style)
    elements.append(sample_detail_table)

    # add space
    elements.append(Spacer(1, 10))

    # add space
    elements.append(Spacer(1, 10))

    # add paragraph
    elements.append(Paragraph("รายละเอียดการทดสอบ", set_paragraph_h1_style()))
    elements.append(Spacer(1, 12))
    # add test detail
    test_data = data[0][3:66]
    # python reshape list from 1*183 to 61*3

    test_detail = [test_data[i:i+3] for i in range(0, len(test_data), 3)]
    test_list = []

    for i, test in enumerate(test_detail):
        if len(test) > 0 and test[1] != 0:
            test_list.append([test[0], test[1], test[2]],)

    test_detail = test_list
    test_list = []
    for i, test in enumerate(test_detail):
        if len(test) > 0 and test[1] != 0:
            test_list.append([str(i+1), test[0], test[2]])

    test_list.insert(0, ['ลำดับ', 'ชื่อการทดสอบ', 'จำนวนตัวอย่างที่ตรวจ'])
    col_widths = [40, 230, 230]  # Adjust the widths as needed
    # Create test detail table
    test_detail_table = Table(test_list, colWidths=col_widths)
    test_detail_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),  # Specify the font name
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        # Background color for the first row
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        # Center alignment for all cells
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        # Middle vertical alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # show grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    test_detail_table.setStyle(test_detail_style)
    elements.append(test_detail_table)

    elements.append(Spacer(1, 25))
    line = HRFlowable(width="100%", thickness=1,
                      color="black", spaceBefore=10, spaceAfter=10)
    elements.append(line)

    elements.append(Paragraph("ทดสอบความไวของยา",
                    set_paragraph_h1_style()))
    elements.append(Spacer(1, 15))

    test_data = data[0][66:148]

    test_detail = [test_data[i:i+2] for i in range(0, len(test_data), 2)]
    test_list = []
    for i, test in enumerate(test_detail):
        if len(test) > 0 and test[1] != 0:
            test_list.append([test[0], test[1]])

    test_detail = test_list
    test_list = []
    for i, test in enumerate(test_detail):
        if len(test) > 0 and test[1] != 0:
            test_list.append([str(i+1), test[0],])

    test_list.insert(0, ['ลำดับ', 'รายการ',])
    col_widths = [40, 150,]  # Adjust the widths as needed
    # Create test detail table
    test_detail_table = Table(
        test_list, colWidths=col_widths, hAlign='LEFT', vAlign='TOP',)
    test_detail_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),  # Specify the font name
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        # Background color for the first row
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        # Center alignment for all cells
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        # Middle vertical alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # show grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black)

    ])

    test_detail_table.setStyle(test_detail_style)
    elements.append(test_detail_table)

    elements.append(Paragraph("การระบุแบคทีเรีย",
                    set_paragraph_h1_style()))
    elements.append(Spacer(1, 15))

    test_data = data[0][148:172]

    test_detail = [test_data[i:i+2] for i in range(0, len(test_data), 2)]
    test_list = []
    for i, test in enumerate(test_detail):
        if len(test) > 0 and test[1] != 0:
            test_list.append([test[0], test[1]])

    test_detail = test_list
    test_list = []
    for i, test in enumerate(test_detail):
        if len(test) > 0 and test[1] != 0:
            test_list.append([str(i+1), test[0],])

    test_list.insert(0, ['ลำดับ', 'รายการ',])
    col_widths = [40, 150,]  # Adjust the widths as needed
    # Create test detail table
    test_detail_table = Table(
        test_list, colWidths=col_widths, hAlign='LEFT', vAlign='TOP',)
    test_detail_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),  # Specify the font name
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        # Background color for the first row
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        # Center alignment for all cells
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        # Middle vertical alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # show grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    test_detail_table.setStyle(test_detail_style)
    elements.append(test_detail_table)

    elements.append(Paragraph("LABORATORY REQUEST FOR",
                    set_paragraph_h1_style()))
    elements.append(Spacer(1, 15))

    test_data = data[0][172:187]
    test_detail = [test_data[i:i+3] for i in range(0, len(test_data), 3)]
    test_list = []
    for i, test in enumerate(test_detail):
        if len(test) > 0 and test[1] != 0:
            test_list.append([test[0], test[1],])

    test_detail = test_list
    test_list = []
    for i, test in enumerate(test_detail):
        if len(test) > 0 and test[1] != 0:
            test_list.append([str(i+1), test[0],])

    test_list.insert(0, ['ลำดับ', 'รายการ',])
    col_widths = [40, 180,]  # Adjust the widths as needed
    # Create test detail table
    test_detail_table = Table(
        test_list, colWidths=col_widths, hAlign='LEFT', vAlign='TOP',)
    test_detail_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),  # Specify the font name
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        # Background color for the first row
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        # Center alignment for all cells
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        # Middle vertical alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # show grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    test_detail_table.setStyle(test_detail_style)
    elements.append(test_detail_table)

    elements.append(Spacer(1, 25))
    line = HRFlowable(width="100%", thickness=1,
                      color="black", spaceBefore=10, spaceAfter=10)
    elements.append(line)
    elements.append(Paragraph("สำหรับห้องปฏิบัติการ",
                    set_paragraph_h1_style()))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph(
        "ลงชื่อ.................................................... ผู้รับสิ่งส่งตรวจ", set_paragraph_style()))
    elements.append(Paragraph(
        "วันที่............/............/............", set_paragraph_style()))
    elements.append(line)

    # Build the PDF
    pdf_file.build(elements)

# ==================================================================================================================


def create_molecular_biology(sample_detail, data, output_file):
    """This function is used to create the molecular biology test detail."""
    left_margin = 0.5 * inch
    right_margin = 0.5 * inch
    top_margin = 0.25 * inch
    bottom_margin = 0.25 * inch

    # Create a SimpleDocTemplate object with custom margins
    pdf_file = SimpleDocTemplate(output_file, pagesize=A4,
                                 leftMargin=left_margin, rightMargin=right_margin,
                                 topMargin=top_margin, bottomMargin=bottom_margin)

    elements = []
    cvdtt_logo = os.path.join(os.path.dirname(__file__), "cvdtt_logo.png")
    title_data = [
        [Image(cvdtt_logo, width=1.5*inch, height=1*inch),
         'ใบคำขอรับบริการทดสอบอณูชีววิทยา', ''],
        ['', Paragraph("ศูนย์ชันสูตรโรคสัตว์และถ่ายทอดเทคโนโลยี คณะสัตวแพทยศาสตร์ มหาวิทยาลัยเชียงใหม่ <br/> (Center of Veterinary Diagnosis and Technology Transfer) <br/> Tel. 053-948041 Mobile 094-6362641 <br/> E-mail vet_diag@cmu.ac.th", set_paragraph_style()), ''],
    ]
    col_widths = [120, 320, 100]  # Adjust the widths as needed
    # Create a table from the data
    table = Table(title_data, colWidths=col_widths)

    # Define the style for the table
    style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),  # Specify the font name
        ('FONTSIZE', (1, 0), (1, 1), 20),
        ('FONTSIZE', (1, 1), (-1, -1), 10),
        # Background color for the first row
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        # Center alignment for all cells
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # Middle vertical alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('SPAN', (1, 0), (1, 1)),
        ('SPAN', (0, 0), (0, 1)),
        # zero padding
        ('PADDING', (0, 0), (-1, -1), 0),
        # show grid
        # ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Add the table to the list of elements
    elements.append(table)
    # add space
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("รายละเอียดสิ่งส่งตรวจ",
                    set_paragraph_h1_style()))
    elements.append(Spacer(1, 12))
    # Add the sample detail
    sample_detail = sample_detail[0]
    detail_info = [
        ['วันที่รับตัวอย่าง', sample_detail[0],
            'Barcode', str(str(sample_detail[25]).zfill(10))],
        ['สิ่งที่ส่งมาตรวจ', sample_detail[20],
            'ประวัติการให้ยา', sample_detail[19]],
        ['สถานะการตอบผล', sample_detail[17],
            'การเก็บรักษาตัวอย่าง', sample_detail[16]],
    ]
    col_widths = [95, 155, 95, 155]  # Adjust the widths as needed
    # Create sample detail table
    sample_detail_table = Table(detail_info, colWidths=col_widths)
    sample_detail_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),  # Specify the font name
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        # Background color for the first row
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        # Center alignment for all cells
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # Middle vertical alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # show grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    sample_detail_table.setStyle(sample_detail_style)
    elements.append(sample_detail_table)

    # add space
    elements.append(Spacer(1, 10))

    # add paragraph
    elements.append(Paragraph("รายละเอียดการทดสอบ", set_paragraph_h1_style()))
    elements.append(Spacer(1, 12))
    # add test detail

    test_data = data[0][3:185]

    # python reshape list from 1*183 to 61*3

    test_detail = [test_data[i:i+3] for i in range(0, len(test_data), 3)]
    test_list = []

    for i, test in enumerate(test_detail):
        if len(test) > 0 and test[1] != 0:
            test_list.append([test[0], test[1]])

    test_detail = test_list
    test_list = []
    for i, test in enumerate(test_detail):
        if len(test) > 0 and test[1] != 0:
            test_list.append([str(i+1), test[0], test[1]])

    test_list.insert(0, ['ลำดับ', 'ชื่อการทดสอบ', 'จำนวนตัวอย่างที่ตรวจ'])
    col_widths = [40, 230, 230]  # Adjust the widths as needed
    # Create test detail table
    test_detail_table = Table(test_list, colWidths=col_widths)
    test_detail_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'THNiramitAS'),  # Specify the font name
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        # Background color for the first row
        ('BACKGROUND', (0, 0), (-1, -1), '#FFFFFF'),
        # Center alignment for all cells
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        # Middle vertical alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # show grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    test_detail_table.setStyle(test_detail_style)
    elements.append(test_detail_table)

    # add paragraph for signature and date at the bottom
    # add horizontal line
    elements.append(Spacer(1, 25))
    line = HRFlowable(width="100%", thickness=1,
                      color="black", spaceBefore=10, spaceAfter=10)
    elements.append(line)
    elements.append(Paragraph("สำหรับห้องปฏิบัติการ",
                    set_paragraph_h1_style()))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph(
        "ลงชื่อ.................................................... ผู้รับสิ่งส่งตรวจ", set_paragraph_style()))
    elements.append(Paragraph(
        "วันที่............/............/............", set_paragraph_style()))
    elements.append(line)
    # # Build the PDF
    pdf_file.build(elements)


def set_paragraph_h1_style():
    """This function is used to set the paragraph style."""
    styles = getSampleStyleSheet()
    style = styles['BodyText']  # You can choose other styles as needed
    style.fontName = 'THNiramitAS'  # Set the desired font name
    style.fontSize = 16  # Set the desired font size
    return style


def set_paragraph_style():
    """This function is used to set the paragraph style."""
    styles = getSampleStyleSheet()
    style = styles['BodyText']  # You can choose other styles as needed
    style.fontName = 'THNiramitAS'  # Set the desired font name
    style.fontSize = 12  # Set the desired font size
    return style
# =================================================================================================


def get_molecular_biology_test_detail(id):
    """This function is used to get the detail of the molecular biology test."""
    pass


def select_data_from_db(sql_cmd, parameters):
    """This function is used to select data from the database."""
    # read server_config.yml and sql_cmd.yml
    server_config_file = os.path.join(
        os.path.dirname(__file__), "server_config.yml")
    with open(server_config_file, "r", encoding='utf-8') as ymlfile:
        server_config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    # connect to database
    conn = mariadb.connect(
        user=server_config["user"],
        password=server_config["password"],
        host=server_config["host"],
        port=server_config["port"],
        database=server_config["database"]
    )
    cur = conn.cursor()
    # get data
    cur.execute(sql_cmd, [str(parameters)])
    data = cur.fetchall()
    conn.close()
    return data


if __name__ == "__main__":
    sql_cmd_file = os.path.join(os.path.dirname(__file__), "sql_cmd.yml")
    with open(sql_cmd_file, "r", encoding='utf-8') as ymlfile:
        sql_cmd = yaml.load(ymlfile, Loader=yaml.FullLoader)
    cmd = sql_cmd["get_sample_data"]
    sample_data = select_data_from_db(cmd, 95)
    cmd = sql_cmd["get_bacteria_biology_tests"]
    test_data = select_data_from_db(cmd, 268)
    # parasite test id number 191

    # morecular_biology_test_id = 185
    # bacteriology_test_id = 190

    # print(test_data)

    # if run from script the path is relative to the script else it is relative to the exe file
    output_file = ""
    if getattr(sys, 'frozen', False):
        # frozen
        output_file = os.path.join(os.path.dirname(sys.executable),
                                   "bacterie_biology_test_detail.pdf")

    else:
        # unfrozen
        output_file = os.path.join(os.path.dirname(
            __file__), "bacterie_biology_test_detail.pdf")

    if len(test_data) > 0 or len(sample_data) > 0:
        create_bacteriology(sample_data, test_data, output_file)
