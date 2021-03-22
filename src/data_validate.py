import re
from datetime import datetime

import numpy

from src.parameters import PHONE_PATTERN, EMAIL_PATTERN, AUTHORITY_CODE_PATTERN, POSTAL_CODE_PATTERN, SNILS_PATTERN, \
    REGION_CODES, RU_SERIAL_PASSPORT_PATTERN, RU_NUMBER_PASSPORT_PATTERN, INN_PATTERN


def not_null_name_validate(name):
    """
    Проверка, что ячейки "Имя" и "Фамилия" заполнены, если нет, то возвращает False

    :param name: Строковое значение
    :return: Строковое значение, либо False
    """
    if type(name) is float and numpy.isnan(name):
        print('Необходимо ввести значения в ячейки "Имя" и "Фамилия".')
        return False
    else:
        return name


def gender_validate(gender):
    """
    Проверка, что значение в ячейке м/ж, преобразует значения, в значения, которые примет сервер (FEMALE/MALE)
    если нет, то возвращает None

    :param gender: Строковое значение
    :return: 'FEMALE' либо 'MALE' либо None
    """
    if type(gender) is float and numpy.isnan(gender):
        return None
    else:
        gender_lower = gender.lower()
        if gender_lower == 'ж':
            return 'FEMALE'
        elif gender_lower == 'м':
            return 'MALE'
        else:
            print('Введен некорректный пол. Сотрудник будет создан без пола.')
            return None


def date_validate(date):
    """
    Приводит дату в формат, принимаемый сервером,
    если не удается привести к заданному формату, то возвраащет None

    :param date: Строковое значение
    :return: Строковое значение в формате, принимаемым сервером, либо None
    """
    if type(date) is float and numpy.isnan(date):
        return None
    else:
        try:
            date_format = datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")
            return str(date_format)
        except:
            print(date)
            print('Некорректно введена'
                  ' дата. Дата не будет записана. Используйте формат dd.mm.yyyy.')
            return None


def phone_validate(phone):
    """
    Проверяет корректность переданного номера телефона, приводит к формату 9xxxxxxxxx
    Возвращает номер, прошедший валидацию

    :param phone: Строковое значение
    :return: Строковое значение номера телефона, без +7/8/7, либо None
    """
    if type(phone) is float and numpy.isnan(phone):
        return None
    else:
        result = re.fullmatch(PHONE_PATTERN, phone)
        if result:
            res_phone = result.group(0).replace('-', '').replace('+', '')
            res_phone = res_phone.replace('(', '').replace(')', '')
            if len(res_phone) > 10:
                return res_phone[1:len(res_phone)]
            else:
                return res_phone
        else:
            print(
                'Некорректно введен номер телефона. Номер не будет записан.')
            return None


def email_validate(email):
    """
    Проверяет корректность переданного email (соответствие регулярному выражению)
    Если корректно, то возвращает переданный корректный email

    :param email: Строковое значение
    :return: Строковое значение email, либо None
    """
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
    """
    Проверяет корректная ли контрольная сумма у переданного СНИЛСа

    :param snils: Строковое значение
    :return: True/False
    """
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
    """
    Проверка соответствия записи СНИЛСа регулярному выражению (123-456-78912 либо вообще без "-", пробелы можно)
    Если валидация записи прошла, то проверяется корректность контрольной суммы

    :param snils: Строковое значение
    :return: Проверенное значение СНИЛС, либо False
    """
    if type(snils) is float and numpy.isnan(snils):
        print('Введите СНИЛС, иначе сотрудник не будет загружен.')
        return False
    else:
        snils = snils.replace(' ', '')
        result = re.fullmatch(SNILS_PATTERN, snils)
        if result:
            snils = result.group(0).replace('-', '')
            if is_snils_correct(snils):
                return snils
            else:
                print('Введен некорректный СНИЛС. Проблема с контрольной суммой. Сотрудник не будет загружен.')
                return False
        else:
            print('Некорректно введен СНИЛС. Формат: ххх-ххх-ххх хх (можно без "-"). Сотрудник не будет загружен.')
            return False


def is_inn_correct(inn):
    """
    Проверка корректности ИНН,
    Рассчитываются контрольные суммы по существующему алгоритму
    Возвращает True, если суммы корректные, False -- если нет

    :param inn: Строковое значение
    :return: True/False
    """
    control_sum_first = 0
    magic_arr = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    for i in range(len(magic_arr)):
        control_sum_first += magic_arr[i] * int(inn[i])
    control_sum_first = control_sum_first % 11
    control_sum_first = control_sum_first % 10

    control_sum_second = 0
    magic_arr2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    for i in range(len(magic_arr2)):
        control_sum_second += magic_arr2[i] * int(inn[i])
    control_sum_second = control_sum_second % 11
    control_sum_second = control_sum_second % 10
    return (inn[10] == str(control_sum_first)) and (inn[11] == str(control_sum_second))


def inn_validate(inn):
    """
    Проверка полного соответствия заданному паттерну (передано 12 цифр)
    Проверяется корректность контрольных сумм

    :param inn: Строковое значение
    :return: Проверенное значение ИНН
    """
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
    """
    Проверка полного соответствия регулярному выражению (серия паспорта -- 4 цифры)

    :param serial_number: Строковое значение
    :return: Проверенное значение серии паспорта
    """
    if type(serial_number) is float and numpy.isnan(serial_number):
        print('Введите серию паспорта, иначе сотрудник не будет загружен.')
    else:
        result = re.fullmatch(RU_SERIAL_PASSPORT_PATTERN, serial_number)
        if result:
            return result.group(0)
        else:
            print('Некорректно введена серия паспорта. Сотрудник не будет загружен.')


def number_validate(number):
    """
    Проверка полного соответствия регулярному выражению (номер паспорта -- 6 цифр)

    :param number: Строковое значение
    :return: Проверенное значение номера паспорта
    """
    if type(number) is float and numpy.isnan(number):
        print('Введите номер паспорта, иначе сотрудник не будет загружен.')
    else:
        result = re.fullmatch(RU_NUMBER_PASSPORT_PATTERN, number)
        if result:
            return result.group(0)
        else:
            print('Некорректно введен номер паспорта. Сотрудник не будет загружен.')


def authority_code_validate(authority_code):
    """
    Проверка полного соответствия регулярному выражению (3 цифры - 3 цифры)

    :param authority_code: Строковое значение
    :return: Проверенное значение кода подразделения, либо None
    """
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
    """
    Проверка полного соответствия регулярному выражению (6 цифр)

    :param postal_code: Строковое значение
    :return: Проверенное значение индекса, либо None
    """
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
    """
    Проверка присутствия переданной строки в заданном словаре REGION_CODES (в качестве значения),
    если присутствует -- возвращается код региона (ключ в словаре),
    если нет -- возвращается None

    :param region_name: Строковое значение
    :return: Код региона (Строковое значение из 2х цифр)
    """
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


def head_manager_validate(head_manager_flag):
    """
    Проверка переданного значения в поле "Руководитель"
    Если передано "Да", то возвращается True (независимо от регистра букв)
    Если передано "Нет", то возвращается False (независимо от регистра букв)
    Если ничего не передано -- None

    :param head_manager_flag: Строковое значение
    :return: True/False/None
    """
    if type(head_manager_flag) is float and numpy.isnan(head_manager_flag):
        print('Не введен флаг, имеет ли сотрудник роль "Руководитель". Сотрудник не будет загружен.')

        return None
    else:
        head_manager_flag_lower = head_manager_flag.lower()
        if head_manager_flag_lower == 'да':
            return True
        elif head_manager_flag_lower == 'нет':
            return False
        else:
            print('Некорректно введен флаг роли сотрудника. Сотрудник не будет загружен.')
            return None


def hr_manager_validate(hr_manager_flag):
    """
    Проверка переданного значения в поле "Кадровик"
    Если передано "Да", то возвращается True (независимо от регистра букв)
    Если передано "Нет", то возвращается False (независимо от регистра букв)
    Если ничего не передано -- None

    :param hr_manager_flag: Строковое значение
    :return: True/False/None
    """
    if type(hr_manager_flag) is float and numpy.isnan(hr_manager_flag):
        print('Не введен флаг, имеет ли сотрудник роль "Кадровик". Сотрудник не будет загружен.')
        return None
    else:
        hr_manager_flag_lower = hr_manager_flag.lower()
        if hr_manager_flag_lower == 'да':
            return True
        elif hr_manager_flag_lower == 'нет':
            return False
        else:
            print('Некорректно введен флаг роли сотрудника. Сотрудник не будет загружен.')
            return None


def external_id_validate(external_id):
    """
    Проверка заполненности ячейки "ID внешней системы"
    Возвращается значение из ячейки "ID внешней системы"
    Если ячейка пустая возвращается None

    :param external_id: Строковое значение
    :return:
    """
    if type(external_id) is float and numpy.isnan(external_id):
        # print('В данные сотрудника не будет записан external_id.')
        return None
    else:
        return external_id


def snils_exists(snils, data_users):
    """
    Проверка существования СНИЛС в списке, полученном с сервера
    Если существует в списке -- True, нет -- False

    :param snils: Строковое значение (переданный СНИЛС)
    :param data_users: Объект класса DataFromServerAboutUsers
    :return: True/False
    """
    if snils in data_users.lst_person_snils:
        print('Пользователь с таким СНИЛСом уже существует в сервисе.')
        return True
    return False


def inn_exists(inn, data_users):
    """
    Проверка существования ИНН в списке, полученном с сервера
    Если существует в списке -- True, нет -- False

    :param inn: Строковое значение (переданный ИНН)
    :param data_users: Объект класса DataFromServerAboutUsers
    :return: True/False
    """
    if inn in data_users.lst_person_inn:
        print('Пользователь с таким ИНН уже существует в сервисе.')
        return True
    return False


def passport_exists(passport, data_users):
    """
    Проверка существования паспорта в списке, полученном с сервера
    Если существует в списке -- True, нет -- False

    :param passport: Строковое значение (переданный паспорт (серия+номер))
    :param data_users: Объект класса DataFromServerAboutUsers
    :return: True/False
    """
    if passport in data_users.lst_person_passport:
        print('Пользователь с таким паспортом уже существует в сервисе.')
        return True
    return False


def email_exists(email, data_users):
    """
    Проверка существования email в списке, полученном с сервера
    Если существует в списке -- True, нет -- False

    :param email: Строковое значение (переданный email)
    :param data_users: Объект класса DataFromServerAboutUsers
    :return: True/False
    """
    if email in data_users.lst_person_email_phone:
        print('Пользователь с таким email уже существует в сервисе.')
        return True
    return False


def phone_exists(phone, data_users):
    """
    Проверка существования номера телефона в списке, полученном с сервера
    Если существует в списке -- True, нет -- False

    :param phone: Строковое значение (переданный номер телефона)
    :param data_users: Объект класса DataFromServerAboutUsers
    :return: True/False
    """
    if phone in data_users.lst_person_email_phone:
        print('Пользователь с таким phone уже существует в сервисе.')
        return True
    return False
