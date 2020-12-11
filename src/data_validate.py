import re
from datetime import datetime

import numpy

from src.parameters import PHONE_PATTERN, EMAIL_PATTERN, AUTHORITY_CODE_PATTERN, POSTAL_CODE_PATTERN, SNILS_PATTERN, \
    REGION_CODES, RU_SERIAL_PASSPORT_PATTERN, RU_NUMBER_PASSPORT_PATTERN, INN_PATTERN


# проверка, что ячейки "Имя" и "Фамилия" заполнены
def not_null_name_validate(name):
    if type(name) is float and numpy.isnan(name):
        print('Необходимо ввести значения в ячейки "Имя" и "Фамилия".')
        return False
    else:
        return name


# валидация занчений из ячейки "Пол"
# преобразует значения, в значения, которые примет сервер (FEMALE/MALE)
def gender_validate(gender):
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


# валидация даты
# приводит дату в формат, принимаемый сервером
# если не удается привести к заданному формату, то возвраащет None
# (дата не будет отправлена на сервер при создании client_user)
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


# валидация номер телефона
# если номер телефона полностью соответуствует регулярному выражению, то
# он будет записан при создании client_user
def phone_validate(phone):
    if type(phone) is float and numpy.isnan(phone):
        return None
    else:
        result = re.fullmatch(PHONE_PATTERN, phone)
        if result:
            # добавить преобразование к единому формату, например 9xxxxxxxxx
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


# валидация email
# если email полностью соответуствует регулярному выражению, то
# он будет записан при создании client_user
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


# проверка корректности СНИЛС
# рассчитывается контрольная сумма по существующему алгоритму
# возвращает True, если сумма корректная, False -- если нет
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


# валидация СНИЛС
# проверка соответствия записи СНИЛСа регулярному выражению (123-456-78912 либо вообще без "-", пробелы можно)
# если валидация записи прошла, то проверяется корректность контрольной суммы
def snils_validate(snils):
    if type(snils) is float and numpy.isnan(snils):
        print('Введите СНИЛС, иначе сотрудник не будет загружен.')
        return False
    else:
        snils = snils.replace(' ', '')
        # проверка что запись снилса корректная (123-456-78912 либо вообще без "-")
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


# проверка корректности ИНН
# рассчитываются контрольные суммы по существующему алгоритму
# возвращает True, если суммы корректные, False -- если нет
def is_inn_correct(inn):
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


# проверяетя полное соответствие заданному паттерну (передано 12 цифр)
# проверяется коррекность контрольных сумм
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


# проверяется полное соответствие регулярному выражению (серия паспорта -- 4 цифры)
def serial_number_validate(serial_number):
    if type(serial_number) is float and numpy.isnan(serial_number):
        print('Введите серию паспорта, иначе сотрудник не будет загружен.')
    else:
        result = re.fullmatch(RU_SERIAL_PASSPORT_PATTERN, serial_number)
        if result:
            return result.group(0)
        else:
            print('Некорректно введена серия паспорта. Сотрудник не будет загружен.')


# проверяется полное соответствие регулярному выражению (номер паспорта -- 6 цифр)
def number_validate(number):
    if type(number) is float and numpy.isnan(number):
        print('Введите номер паспорта, иначе сотрудник не будет загружен.')
    else:
        result = re.fullmatch(RU_NUMBER_PASSPORT_PATTERN, number)
        if result:
            return result.group(0)
        else:
            print('Некорректно введен номер паспорта. Сотрудник не будет загружен.')


# валидация authority_code
# запись соответствует 3 цифры - 3 цифры
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


# валидация индекса
# запись соответствует 6 цифрам
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


# валидация кода региона
# берется строковое значение из excel-таблицы
# проверяется присутствие в заданном словаре REGION_CODES
# возвращается код региона
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


# валидация поля "Руководитель"
# если передано "Да", то возвращается True
# если передано "Нет", то возвращается False
def head_manager_validate(head_manager_flag):
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


# валидация поля "Кадровик"
# если передано "Да", то возвращается True
# если передано "Нет", то возвращается False
def hr_manager_validate(hr_manager_flag):
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


# валидация поля ID внешней системы
def external_id_validate(external_id):
    if type(external_id) is float and numpy.isnan(external_id):
        # print('В данные сотрудника не будет записан external_id.')
        return None
    else:
        return external_id


# проверка существования СНИЛС в списке, полученном с сервера
# печать ошибки, если пользователь с таким СНИЛС уже загружен
def snils_exists(snils, data_users):
    if snils in data_users.lst_person_snils:
        print('Пользователь с таким СНИЛСом уже существует в сервисе.')
        return True
    return False


# проверка существования ИНН в списке, полученном с сервера
# печать ошибки, если пользователь с таким ИНН уже загружен
def inn_exists(inn, data_users):
    if inn in data_users.lst_person_inn:
        print('Пользователь с таким ИНН уже существует в сервисе.')
        return True
    return False


# проверка существования номера и серии паспорта в списке, полученном с сервера
# печать ошибки, если пользователь с таким паспортом уже загружен
def passport_exists(passport, data_users):
    if passport in data_users.lst_person_passport:
        print('Пользователь с таким паспортом уже существует в сервисе.')
        return True
    return False


# проверка существования email в списке, полученном с сервера
# печать ошибки, если пользователь с таким email уже загружен
def email_exists(email, data_users):
    if email in data_users.lst_person_email_phone:
        print('Пользователь с таким email уже существует в сервисе.')
        return True
    return False


# проверка существования номера телефона в списке, полученном с сервера
# печать ошибки, если пользователь с таким телефоном уже загружен
def phone_exists(phone, data_users):
    if phone in data_users.lst_person_email_phone:
        print('Пользователь с таким phone уже существует в сервисе.')
        return True
    return False
