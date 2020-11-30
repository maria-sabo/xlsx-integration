import re
from datetime import datetime

import numpy

from src.parameters import PHONE_PATTERN, EMAIL_PATTERN, AUTHORITY_CODE_PATTERN, POSTAL_CODE_PATTERN, SNILS_PATTERN, \
    REGION_CODES


def gender_validate(gender):
    if gender == 'Ж':
        return 'FEMALE'
    elif gender == 'M':
        return 'MALE'
    else:
        print('Введен некорректный пол. Сотрудник будет создан без пола.')
        return None


def date_validate(date):
    try:
        date_format = datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")
        return str(date_format)
    except:
        print('Неккорентно введена дата. Дата не будет записана. Используйте формат dd.mm.yyyy.')
        return None


def phone_validate(phone):
    if not numpy.isnan(phone):
        # result = _compile(PHONE_PATTERN).fullmatch(phone)
        result = re.fullmatch(PHONE_PATTERN, phone)
        if result:
            return result.group(0)
        else:
            print(
                'Некорректно введен номер телефона. Номер не будет записан.')
            return None
    else:
        return None


def email_validate(email):
    if not numpy.isnan(email):
        result = re.fullmatch(EMAIL_PATTERN, email)
        if result:
            return result.group(0)
        else:
            print(
                'Некорректно введен email. Email не будет записан.')
            return None
    return None


def snils_validate(snils):
    if snils:
        return snils
    else:
        return None
    # '^(\\d{3})-?(\\d{3})-?(\\d{3})(\\d{2})$'


def inn_validate(inn):
    pass


def serial_number_validate(serial_number):
    pass


def number_validate(number):
    pass


def authority_code_validate(authority_code):
    if not numpy.isnan(authority_code):
        result = re.fullmatch(AUTHORITY_CODE_PATTERN, authority_code)
        if result:
            return result.group(0)
        else:
            print(
                'Некорректно введен код подразделения. Код подразделения не будет записан.')
            return None
    return None


def postal_code_validate(postal_code):
    if not numpy.isnan(postal_code):
        result = re.fullmatch(POSTAL_CODE_PATTERN, postal_code)
        if result:
            return result.group(0)
        else:
            print(
                'Некорректно введен индекс. Индекс не будет записан.')
            return None
    return None


# будет две цифры, перевести в код, составить словарь
def region_code_validate(region_code):
    pass
