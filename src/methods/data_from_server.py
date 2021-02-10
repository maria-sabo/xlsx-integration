import json
import requests
from src.classes.data_from_server_user import DataFromServerAboutUsers

from src.config import sub_domain


def get_positions_dict(token, client_id):
    """
    Функция посылает GET-запрос и возвращает словарь типа {'position_id': 'position_name', ...}
    с имеющимися у клиента должностями

    :param token: api-токен клиента
    :param client_id: Идентификатор клиента в сервисе
    :return: Словарь существующих у клиента должностей типа {'position_id': 'position_name', ...},
    либо False (если запрос выполнился с ошибкой)
    """
    positions_response = requests.get(
        'https://' + sub_domain + '.hr-link.ru/api/v1/clients/' + client_id + '/employeePositions',
        headers={'User-Api-Token': token})
    response_dict = json.loads(positions_response.text)
    positions_dict = {}
    if response_dict.get('result'):
        employee_positions = response_dict.get('employeePositions')
        for position in employee_positions:
            positions_dict[position.get('id')] = position.get('name')
        return positions_dict
    else:
        print('Ошибка: ' + response_dict.get('errorMessage'))
        return False


def get_root_department_id(token, client_id):
    """
    Функция посылает GET-запрос и возвращает идентификатор корневого отдела у клиента

    :param token: api-токен клиента
    :param client_id: Идентификатор клиента в сервисе
    :return: Идентификатор корневого отдела, либо False (если запрос выполнился с ошибкой)
    """
    root_department_response = requests.get(
        'https://' + sub_domain + '.hr-link.ru/api/v1/clients/' + client_id + '/departments',
        headers={'User-Api-Token': token})
    response_dict = json.loads(root_department_response.text)
    if response_dict.get('result'):
        lst_departments = response_dict.get('clientDepartments')
        for department in lst_departments:
            if department.get('parentDepartmentId') is None:
                root_department_id = department.get('id')
                return root_department_id
    else:
        print('Ошибка: ' + response_dict.get('errorMessage'))
        return False


def get_departments_dict(token, client_id):
    """
    Функция посылает GET-запрос и возращает словарь типа {'department_id': 'department_name', ...}
    с существующими у клиента отделами

    :param token: api-токен клиента
    :param client_id: Идентификатор клиента в сервисе
    :return: Словарь типа {'department_id': 'department_name', ...}, либо False (если запрос выполнился с ошибкой)
    """
    departments_response = requests.get(
        'https://' + sub_domain + '.hr-link.ru/api/v1/clients/' + client_id + '/departments',
        headers={'User-Api-Token': token})
    response_dict = json.loads(departments_response.text)
    departments_dict = {}
    if response_dict.get('result'):
        departments = response_dict.get('clientDepartments')
        for department in departments:
            departments_dict[department.get('id')] = department.get('name')
        return departments_dict
    else:
        print('Ошибка: ' + response_dict.get('errorMessage'))
        return False


def get_employee_role_ids(token):
    """
    Функция посылает GET-запрос и возвращает идентификатор роли "Руководитель", идентификатор роли "Кадровик"

    :param token: api-токен клиента
    :return: Идентификатор роли "Руководитель", идентификатор роли "Кадровик", либо False, False
    (если при запросе произошла ошибка)
    """
    departments_response = requests.get(
        'https://' + sub_domain + '.hr-link.ru/api/v1/employeeRoles',
        headers={'User-Api-Token': token})
    response_dict = json.loads(departments_response.text)
    employee_roles_dict = {}
    if response_dict.get('result'):
        employee_roles = response_dict.get('employeeRoles')
        for employee_role in employee_roles:
            employee_roles_dict[employee_role.get('id')] = employee_role.get('name')

        for employee_role_id, employee_role_name in employee_roles_dict.items():
            if employee_role_name == 'Руководитель':
                head_manager_id = employee_role_id
            elif employee_role_name == 'Кадровик':
                hr_manager_id = employee_role_id
        return head_manager_id, hr_manager_id
    else:
        print('Ошибка: ' + response_dict.get('errorMessage'))
        return False, False


def get_external_id_lst(token, client_id, legal_entity_id):
    """
    Функция посылает GET-запрос и возвращает список external_id, принадлежащих переданному юрлицу

    :param token: api-токен клиента
    :param client_id: Идентификатор клиента в сервисе
    :param legal_entity_id: Идентификатор юрлица
    :return: Список external_id, существующих у переланного юрлица
    """
    employee_response = requests.get('https://' + sub_domain + '.hr-link.ru/api/v1/clients/' + client_id + '/employees',
                                     headers={'User-Api-Token': token})
    response_dict = json.loads(employee_response.text)
    lst_external_id = []

    if response_dict.get('result'):
        lst_employees = response_dict.get('employees')
        for employee in lst_employees:
            legal_entities = employee.get('legalEntities')
            for legal_entity in legal_entities:
                legal_entity_id_server = legal_entity.get('legalEntity').get('id')
                if legal_entity_id == legal_entity_id_server:
                    lst_external_id.append(legal_entity.get('externalId'))
        lst_external_id = list(filter(None, lst_external_id))
        return lst_external_id
    else:
        print('Ошибка.' + response_dict.get('errorMessage'))
    return []


def get_lst_about_users(token, client_id):
    """
    Функция посылает GET-запрос для получения информации о всех сотрудниках клиента
    Все данные сотрудников (ИНН, СНИЛС, паспорт, email, телефон) записываются в поля(поле-список) экземпляра
    класса DataFromServerAboutUsers

    :param token: api-токен клиента
    :param client_id: Идентификатор клиента в сервисе
    :return: экземпляр класса DataFromServerAboutUsers
    """
    response = requests.get('https://' + sub_domain + '.hr-link.ru/api/v1/clients/' + client_id + '/employees',
                            headers={'User-Api-Token': token})
    response_dict = json.loads(response.text)
    data_users = DataFromServerAboutUsers

    if response_dict.get('result'):
        lst_employees = response_dict.get('employees')
        for employee in lst_employees:
            personal_documents = employee.get('personalDocuments')
            for personal_document in personal_documents:
                if personal_document['type'] == "SNILS":
                    data_users.lst_person_snils.append(personal_document['number'])
                if personal_document['type'] == "INN":
                    data_users.lst_person_inn.append(personal_document['number'])
                if personal_document['type'] == "PASSPORT":
                    data_users.lst_person_passport.append(
                        personal_document['serialNumber'] + personal_document['number'])
            notification_channels = employee.get('notificationChannels')
            for notification_channel in notification_channels:
                data_users.lst_person_email_phone.append(notification_channel['login'])
            data_users.lst_person_email_phone = list(filter(None, data_users.lst_person_email_phone))
        return data_users
    else:
        print('Ошибка. Не удалось получить сотрудников и их СНИЛСы. ' + response_dict.get('errorMessage'))
        return False
