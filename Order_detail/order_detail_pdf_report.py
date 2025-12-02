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


font_path = ""
if getattr(sys, 'frozen', False):
    # frozen
    font_path = os.path.join(os.path.dirname(
        sys.executable), "TH Niramit AS.ttf")
else:
    # unfrozen
    font_path = os.path.join(os.path.dirname(__file__), "TH Niramit AS.ttf")
pdfmetrics.registerFont(TTFont('THNiramitAS', font_path))


def create_order_report(sample_detail, data, output_file):
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
        create_order_report(sample_data, test_data, output_file)
