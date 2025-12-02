import os
import tempfile
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageQt import ImageQt

from PySide6 import QtPrintSupport, QtCore, QtGui
from PySide6.QtPrintSupport import QPrintPreviewDialog
from PySide6.QtGui import QPageSize
from PySide6.QtCore import QSizeF

class BarcodeGenerator:
    def __init__(self):
        self.temp_folder = tempfile.gettempdir()
        self.barcode_file_path = os.path.join(self.temp_folder, "barcode.png")
        
        # Setup Fonts
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.font_path = os.path.join(current_dir, "TH Niramit AS Bold.ttf")
        
        self.using_fallback_font = False
        
        if not os.path.exists(self.font_path):
            self.using_fallback_font = True
            windows_font_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
            possible_fonts = [
                os.path.join(windows_font_dir, 'tahoma.ttf'),
                os.path.join(windows_font_dir, 'arial.ttf')
            ]
            for f in possible_fonts:
                if os.path.exists(f):
                    self.font_path = f
                    break

    def generate(self, data_rows):
        if not data_rows: return
        
        row = data_rows[0]
        date = row[0]
        sample_code = row[1]
        species = row[2]
        lab_name = row[3]
        collect = row[4]
        speed = row[5]

        label_img = self.generate_sticker_label(
            sample_code=sample_code, 
            species=species, 
            date=date, 
            lab_name=lab_name, 
            speed=speed, 
            collect=collect
        )
        label_img.save(self.barcode_file_path, 'PNG')

    def generate_sticker_label(self, sample_code=" ", species=" ", date=" ", lab_name=" ", speed=" ", collect=" "):
        
        if self.using_fallback_font:
            main_size = 85
            big_size = 100
        else:
            main_size = 120
            big_size = 135

        try:
            text_font = ImageFont.truetype(self.font_path, main_size)
            text_font_big = ImageFont.truetype(self.font_path, big_size)
        except OSError:
            text_font = ImageFont.load_default()
            text_font_big = ImageFont.load_default()

        background_layer = Image.new('RGB', (2000, 2000), "white")

        barcode.base.Barcode.default_writer_options['write_text'] = False
        writer = ImageWriter()
        barcode_code128 = barcode.get('code128', str(sample_code), writer=writer)
        barcode_image = barcode_code128.render({"mode": "RGBA"})
        barcode_image = barcode_image.resize((1650, 1500), Image.Resampling.LANCZOS)

        text_layer = Image.new('RGBA', (2000, 2000))
        draw = ImageDraw.Draw(text_layer)
        
        # -- Left Column --
        draw.text((50, 20), "LAB NO.:  " + str(sample_code), font=text_font, anchor='lt', fill="#000000")
        draw.text((50, 160), "SPECIES: " + str(species), font=text_font, anchor='lt', fill="#000000")
        draw.text((50, 290), "ROOM: " + str(lab_name), font=text_font, anchor='lt', fill="#000000")
        draw.text((50, 420), "DATE:  " + str(date), font=text_font, anchor='lt', fill="#000000")

        # -- Right Column --
        draw.text((1100, 10), str(collect), font=text_font, anchor='lt', fill="#000000")
        draw.text((1100, 130), str(speed), font=text_font_big, anchor='lt', fill="#000000")

        background_layer.paste(text_layer, (0, 0), text_layer)
        
        # <--- FIX 1: Moved Barcode UP (from 530 to 480) --->
        Image.Image.paste(background_layer, barcode_image, (1, 480))

        # <--- FIX 2: Reduced Crop Height (from 1200 to 950) to remove white space --->
        final_layer = background_layer.crop((0, 0, 2100, 920))
        return final_layer

    def print_barcode(self):
        if not os.path.exists(self.barcode_file_path):
            return

        im = Image.open(self.barcode_file_path)
        printer = QtPrintSupport.QPrinter()
        pageSize = QPageSize(QSizeF(50, 30), QPageSize.Millimeter)
        printer.setPageSize(pageSize)

        preview = QPrintPreviewDialog(printer)
        preview.paintRequested.connect(lambda p: self.handle_paint_request(p, im))
        preview.exec()

    def handle_paint_request(self, printer, im):
        printer.setResolution(1200)
        printer.setPageMargins(QtCore.QMargins(0, 0, 0, 0), QtGui.QPageLayout.Millimeter)
        
        im_qt = ImageQt(im).copy()
        painter = QtGui.QPainter(printer)
        
        image = QtGui.QPixmap.fromImage(im_qt).scaled(2500, 1500, QtCore.Qt.KeepAspectRatio)
        
        painter.drawPixmap(0, 0, image)
        painter.end()