import re


def reformat_austrian_phone_number(phone_number: str) -> str | None:
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
