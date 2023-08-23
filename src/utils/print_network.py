import platform

from utils.Emergency import Emergency
from utils.config import Config

from utils.util_functions import reformat_austrian_phone_number


def print_emergency(emergency: Emergency):
    match platform.system():
        case 'Windows':
            windows_print(emergency)
        case 'Linux':
            linux_print(emergency)
        case _:
            raise Exception("Wrong OS")


def windows_print(emergency: Emergency):
    linux_make_pdf(emergency)
    config = Config()
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
        printer.text("Von {}".format(emergency.origin), font_config=text)
        printer.text("{} Alst. {}".format(emergency.name, emergency.level), font_config=text)
        if emergency.caller is not None:
            cal = reformat_austrian_phone_number(emergency.caller)
            printer.text("Anrufer: {}".format(cal), font_config=text)
        printer.text(emergency.operationName, font_config=text)


def linux_make_pdf(emergency: Emergency):
    from fpdf import FPDF

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=45)
    pdf.cell(200, 10, txt="Einsatz Informationen", ln=1, align='L')
    pdf.set_font("Arial", size=20)

    pdf.cell(200, 10, txt="Von {}".format(emergency.origin), ln=2, align='L')
    pdf.cell(200, 10, txt="{} Alst. {}".format(emergency.name, emergency.level), ln=3, align='L')
    if emergency.caller is not None:
        cal = reformat_austrian_phone_number(emergency.caller)
        pdf.cell(200, 10, txt="Anrufer: {}".format(cal), ln=4, align='L')
    pdf.cell(200, 10, txt=emergency.operationName, ln=5, align='L')

    pdf.output("{}.pdf".format(emergency.id))


def linux_print(emergency: Emergency):
    linux_make_pdf(emergency)
    import subprocess
    with open("/tmp/{}.pdf".format(emergency.id), "rb") as file:
        subprocess.run(["/usr/bin/lpr"], stdin=file)
