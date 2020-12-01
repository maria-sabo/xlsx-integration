import re
from datetime import datetime

import numpy

from src.parameters import PHONE_PATTERN, EMAIL_PATTERN, AUTHORITY_CODE_PATTERN, POSTAL_CODE_PATTERN, SNILS_PATTERN, \
    REGION_CODES, RU_SERIAL_PASSPORT_PATTERN, RU_NUMBER_PASSPORT_PATTERN, INN_PATTERN


def gender_validate(gender):
    if type(gender) is float and numpy.isnan(gender):
        return None
    else:
        if gender == 'Ж':
            return 'FEMALE'
        elif gender == 'M':
            return 'MALE'
        else:
            print('Введен некорректный пол. Сотрудник будет создан без пола.')
            return None


def date_validate(date):
    if type(date) is float and numpy.isnan(date):
        return None
    else:
        try:
            date_format = datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")
            return str(date_format)
        except:
            print('Неккорентно введена дата. Дата не будет записана. Используйте формат dd.mm.yyyy.')
            return None


def phone_validate(phone):
    if type(phone) is float and numpy.isnan(phone):
        return None
    else:
        result = re.fullmatch(PHONE_PATTERN, phone)
        if result:
            return result.group(0)
        else:
            print(
                'Некорректно введен номер телефона. Номер не будет записан.')
            return None


def email_validate(email):
    if type(email) is float and numpy.isnan(email):
        return None
    else:
        result = re.fullmatch(EMAIL_PATTERN, email)
        if result:
            return result.group(0)
        else:
            print('Некорректно введен email. Email не будет записан.')
            return None


def is_snils_correct(snils):
    controlSum = None
    snils = snils.replace('-', '')
    number = snils[0:9]
    control_number = int(snils[9:11])
    sum = 0
    j = 9
    for digit in number:
        sum = sum + int(digit) * j
        j = j - 1
    if sum > 101:
        sum = sum % 101
    if sum < 100:
        controlSum = sum
    elif sum == 100 or sum == 101:
        controlSum = 0
    result = (control_number == controlSum)
    return result


def snils_validate(snils):
    if type(snils) is float and numpy.isnan(snils):
        print('Введите СНИЛС, иначе сотрудник не будет загружен.')
    else:
        snils = snils.replace(' ', '')
        # проверка что запись снилса корректная (123-456-78912 либо вообще без "-")
        result = re.fullmatch(SNILS_PATTERN, snils)
        if result:
            if is_snils_correct(result.group(0)):
                return result.group(0)
            else:
                print('Введен некорректный СНИЛС. Проблема с контрольной суммой. Сотрудник не будет загружен.')
        else:
            print('Некорректно введен СНИЛС. Формат: ххх-ххх-ххх хх. Сотрудник не будет загружен.')


def is_inn_correct(inn):
    control_sum_first = 0
    arr = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    for i in range(len(arr)):
        control_sum_first += arr[i] * int(inn[i])
    control_sum_first = control_sum_first % 11
    control_sum_first = control_sum_first % 10

    control_sum_second = 0
    arr2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    for i in range(len(arr2)):
        control_sum_second += arr2[i] * int(inn[i])
    control_sum_second = control_sum_second % 11
    control_sum_second = control_sum_second % 10
    return (inn[10] == str(control_sum_first)) and (inn[11] == str(control_sum_second))


def inn_validate(inn):
    if type(inn) is float and numpy.isnan(inn):
        print('Введите ИНН ФЛ, иначе сотрудник не будет загружен.')
    else:
        result = re.fullmatch(INN_PATTERN, inn)
        if result:
            if is_inn_correct(result.group(0)):
                return result.group(0)
            else:
                print('Введен некорректный ИНН ФЛ. Проблема с контрольной суммой. Сотрудник не будет загружен.')
        else:
            print('Некорректно введен ИНН ФЛ. Сотрудник не будет загружен.')


def serial_number_validate(serial_number):
    if type(serial_number) is float and numpy.isnan(serial_number):
        print('Введите серию паспорта, иначе сотрудник не будет загружен.')
    else:
        result = re.fullmatch(RU_SERIAL_PASSPORT_PATTERN, serial_number)
        if result:
            return result.group(0)
        else:
            print('Некорректно введена серия паспорта. Сотрудник не будет загружен.')


def number_validate(number):
    if type(number) is float and numpy.isnan(number):
        print('Введите номер паспорта, иначе сотрудник не будет загружен.')
    else:
        result = re.fullmatch(RU_NUMBER_PASSPORT_PATTERN, number)
        if result:
            return result.group(0)
        else:
            print('Некорректно введен номер паспорта. Сотрудник не будет загружен.')


def authority_code_validate(authority_code):
    if type(authority_code) is float and numpy.isnan(authority_code):
        return None
    else:
        result = re.fullmatch(AUTHORITY_CODE_PATTERN, authority_code)
        if result:
            return result.group(0)
        else:
            print('Некорректно введен код подразделения. Код подразделения не будет записан.')
            return None


def postal_code_validate(postal_code):
    if type(postal_code) is float and numpy.isnan(postal_code):
        return None
    else:
        result = re.fullmatch(POSTAL_CODE_PATTERN, postal_code)
        if result:
            return result.group(0)
        else:
            print('Некорректно введен индекс. Индекс не будет записан.')
            return None


def region_code_validate(region_name):
    if type(region_name) is float and numpy.isnan(region_name):
        return None
    else:
        if region_name in REGION_CODES.values():
            for code, name in REGION_CODES.items():
                if name == region_name:
                    return code
        else:
            print('Некорректно введен регион. Регион не будет записан.')
            return None
