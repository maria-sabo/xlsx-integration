import numpy
from src.methods.create_for_employee import create_position, create_department


def get_position(token, client_id, position_excel, positions_dict):
    """
    Функция возвращает идентификатор должности, переданной в excel-таблице
        Если значение из ячейки "Должность" не заполнено, то возвращается '',
        Если значение из ячейки excel-таблицы уже существует на сервере, то берется существующий идентификатор
        Если значение из ячейки excel-таблицы не было записано на сервере,
        то вызывается функция создания новой должности и возвращается новый созданный идентификатор

    :param token: api-токен клиента
    :param client_id: Идентификатор клиента в сервисе
    :param position_excel: Название должности из excel-таблицы
    :param positions_dict: Словарь типа {'position_id': 'position_name', ...}, полученный с сервера
    :return: Идентификатор должности
    """
    for position_id, position_name in positions_dict.items():
        if type(position_excel) is float and numpy.isnan(position_excel):
            return ""
        else:
            if position_name.lower() == position_excel.lower():
                return position_id
    position_id = create_position(token, client_id, position_excel)
    positions_dict[position_id] = position_excel
    return position_id


def get_department(token, client_id, department_excel, root_department_id, departments_dict):
    """
    Функция возвращает идентификатор отдела, переданного в excel-таблице
        Если значение из ячейки "Отдел" не заполнено, то возвращается '',
        Если значение из ячейки excel-таблицы уже существует на сервере, то берется существующий идентификатор
        Если значение из ячейки excel-таблицы не было записано на сервере,
        то вызывается функция создания нового отдела и возвращается новый созданный идентификатор

    :param token: api-токен клиента
    :param client_id: Идентификатор клиента в сервисе
    :param department_excel: Название таблицы из excel-таблицы
    :param root_department_id: Идентификатор корневого отдела у клиента
    :param departments_dict: Словарь типа {'department_id': 'department_name', ...}, полученный с сервера
    :return: Идентификатор отдела
    """
    for department_id, department_name in departments_dict.items():
        if type(department_excel) is float and numpy.isnan(department_excel):
            return ""
        else:
            if department_name.lower() == department_excel.lower():
                return department_id
    department_id = create_department(token, client_id, department_excel, root_department_id)
    departments_dict[department_id] = department_excel
    return department_id


def get_role_ids(head_manager_excel, hr_manager_excel, head_manager_id, hr_manager_id):
    """
    Функция возвращает список идентификаторов ролей, на основе переданных 'да/нет' в excel-таблице
    (да - передаем идентификатор, нет - не передаем)

    :param head_manager_excel: Значение из ячейки excel (Во время валидации переведено в True/False)
    :param hr_manager_excel: Значение из ячейки excel (Во время валидации переведено в True/False)
    :param head_manager_id: Идентификатор роли "Руководитель" с сервера
    :param hr_manager_id: Идентификатор роли "Кадровик" с сервера
    :return: Список идентификаторов ролей
    """
    role_ids = []
    if head_manager_excel and hr_manager_excel:
        role_ids.append(head_manager_id)
        role_ids.append(hr_manager_id)
    elif head_manager_excel:
        role_ids.append(head_manager_id)
    elif hr_manager_excel:
        role_ids.append(hr_manager_id)
    return role_ids


def get_external_id(external_id_excel, external_id_lst):
    """
    Функция возвращает ID сотрудника во внешней системе
    Если переданный идентификатор уже есть в списке идентификаторов юрлица, в котором сотрудник, то
    возвращается None
    Если идентификатора нет в системе, то возвращается переданный в excel-таблице

    :param external_id_excel: Значение ячейки "ID сотрудника во внешней системе" excel-таблицы
    :param external_id_lst: Список идентификаторов сотрудников во внешней системе для юрлица, в котором сотрудник
    :return: Идентификатор сотрудника во внешней системе, либо None (если идентификатор уже есть в системе)
    """
    if external_id_excel in external_id_lst:
        print(
            'Такой ID сотрудника во внешней системе уже существует в данном юрлице. Сотрудник создастся без '
            'external_id.')
        return None
    else:
        external_id_lst.append(external_id_excel)
        return external_id_excel
