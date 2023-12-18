import re
from app.functions import get_clean_number

def name_validate(name):
    if all(letter.isalpha() or letter.isspace() for letter in name):
        return True
    else:
        return False


def cpf_validate(cpf):
    cpf_numbers = [int(digit) for digit in cpf if digit.isdigit()]

    if len(cpf_numbers) != 11:
        return False

    sum_ = 0
    for i in range(9):
        sum_ += cpf_numbers[i] * (10 - i)
    digit1 = (sum_ * 10) % 11
    if digit1 == 10:
        digit1 = 0

    sum_ = 0
    for i in range(10):
        sum_ += cpf_numbers[i] * (11 - i)
    digit2 = (sum_ * 10) % 11
    if digit2 == 10:
        digit2 = 0

    if digit1 == cpf_numbers[9] and digit2 == cpf_numbers[10]:
        return True
    else:
        return False


def validate_phone(phone_number):
    if len(str(int(phone_number))) == 11:

        valid_area_codes = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '21', '22', '24', '27', '28',
                            '31', '32', '33', '34', '35', '37', '38', '41', '42', '43', '44', '45', '46', '47',
                            '48', '49', '51', '53', '54', '55', '61', '62', '63', '64', '65', '66', '67', '68',
                            '69', '71', '73', '74', '75', '77', '79', '81', '82', '83', '84', '85', '86', '87',
                            '88', '89', '91', '92', '93', '94', '95', '96', '97', '98', '99']
        area_code = phone_number[:2]
        print(area_code not in valid_area_codes)
        if area_code not in valid_area_codes:
            return False
        return True
    else:
        return False
