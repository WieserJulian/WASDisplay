import logging
import platform

import win32ui
from utils.Emergency import Emergency
from utils.config import Config

from utils.util_functions import reformat_austrian_phone_number


def print_emergency(emergency: Emergency):
    match platform.system():
        case 'Windows':
            for _ in range(Config().settings.settings.printer.amount):
                try:
                    windows_print(emergency)
                except win32ui.error as e:
                    logging.error("Printing failed", e)
        case 'Linux':
            for _ in range(Config().settings.settings.printer.amount):
                try:
                    linux_print(emergency)
                except Exception as e:
                    logging.error("Printing failed", e)
        case _:
            raise Exception("Wrong OS")


def windows_print(emergency: Emergency):
    from win32printing import Printer

    text = {
        "height": 24,
    }
    h1 = {
        "height": 45,
        "bold": True
    }
    with Printer(linegap=2, margin=(21.1, 22.2, 10, 0),
                 auto_page=True) as printer:
        printer.auto_page = True
        printer.text("Einsatz Informationen", font_config=h1, align="center")
        printer.text("{} Alst. {}".format(emergency.operationName, emergency.level), font_config=text)
        printer.text("Ort: {}".format(emergency.location), font_config=text)
        printer.text("Anrufer: {}".format(emergency.name), font_config=text)
        if emergency.caller is not None:
            cal = reformat_austrian_phone_number(emergency.caller)
            printer.text("Telefonnummer: {}".format(cal), font_config=text)
        printer.text("Von {}".format(emergency.origin), font_config=text)
        printer.text("ID: {} {}".format(emergency.id, emergency.receiveTad), font_config=text)


def linux_make_pdf(emergency: Emergency):
    from fpdf import FPDF

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=45)
    pdf.cell(200, 10, txt="Einsatz Informationen", ln=1, align='L')
    pdf.set_font("Arial", size=20)

    pdf.cell(200, 10, txt="{} Alst. {}".format(emergency.name, emergency.level), ln=2, align='L')
    pdf.cell(200, 10, txt="Anrufer: {}".format(emergency.name), ln=3, align='L')
    if emergency.caller is not None:
        cal = reformat_austrian_phone_number(emergency.caller)
        pdf.cell(200, 10, txt="Telefonnummer: {}".format(cal), ln=4, align='L')
    pdf.cell(200, 10, txt="Von {}".format(emergency.origin), ln=5, align='L')
    pdf.cell(200, 10, txt="ID: {} {}".format(emergency.id, emergency.receiveTad), ln=6, align='L')

    pdf.output("{}.pdf".format(emergency.id))


def linux_print(emergency: Emergency):
    linux_make_pdf(emergency)
    import subprocess
    with open("/tmp/{}.pdf".format(emergency.id), "rb") as file:
        subprocess.run(["/usr/bin/lpr"], stdin=file)
