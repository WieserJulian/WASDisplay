# Python program to create
# a pdf file
import re

from fpdf import FPDF


def generate_pdf():
    def reformat_austrian_phone_number(phone_number):
        if phone_number is None:
            return phone_number
        # Remove all non-digit characters from the phone number
        digits_only = re.sub(r'\D', '', phone_number)

        # Check if the phone number is valid and has enough digits
        if not re.match(r'[0-9]*\/*(\+49)*(\+43)*(\+41)*[ ]*(\([0-9]{3,6}\))*([ ]*[0-9]|\/|\(|\)|\-|)*', digits_only):
            return phone_number

        # Reformat the phone number to the desired format
        formatted_number = f"+43 (0)6{digits_only[2:4]} {digits_only[4:7]} {digits_only[7:]}"

        return formatted_number

    # save FPDF() class into a
    # variable pdf
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size=30)

    # create a cell
    pdf.cell(200, 10, txt="EINSATZ INFOS",
             ln=1, align='C')

    pdf.set_font("Arial", size=15)
    pdf.cell(100, 10, txt="ID: {} / {}".format("E191100476", "2019-11-06 17:58:49"),
             ln=2, align='L')

    pdf.cell(100, 10, txt="Von {}".format("LFKOO"),
             ln=3, align='L')

    pdf.cell(100, 10, txt="BACH 4 RUTZENHAM RUTZENHAM",
             ln=4, align='L')

    pdf.cell(100, 10, txt="{} Alst. {}".format("TEST", "1"),
             ln=5, align='L')
    cal = reformat_austrian_phone_number("069910149977")
    pdf.cell(100, 10, txt="Anrufer: {}".format(cal),
             ln=6, align='L')

    pdf.cell(100, 10, txt="TEST WAS-ENDSTELLE 1",
             ln=7, align='L')

    # pdf.cell()
    # save the pdf with name .pdf
    pdf.output("EINSATZ_INFO.pdf")


def x():
    import win32api
    import win32print
    from glob import glob

    # A List containing the system printers
    all_printers = [printer[2] for printer in win32print.EnumPrinters(2)]
    # Ask the user to select a printer
    printer_num = int(input("Choose a printer:\n"+"\n".join([f"{n} {p}" for n, p in enumerate(all_printers)])+"\n"))
    # set the default printer
    win32print.SetDefaultPrinter(all_printers[printer_num])
    pdf_dir = r"EINSATZ_INFO.pdf"
    for f in glob(pdf_dir, recursive=True):
        win32api.ShellExecute(0, "print", f, None,  ".",  0)

    input("press any key to exit")

if __name__ == '__main__':
    x()
