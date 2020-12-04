import json
import requests


# получаем список всех снилсов в сервисе
def lst_snils(token, client_id):
    snils_response = requests.get('https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/employees',
                                  headers={'User-Api-Token': token})
    response_dict = json.loads(snils_response.text)
    lst_person_snils = []

    if response_dict.get('result'):
        lst_employees = response_dict.get('employees')
        for employee in lst_employees:
            personal_documents = employee.get('personalDocuments')
            for personal_document in personal_documents:
                if personal_document['type'] == "SNILS":
                    lst_person_snils.append(personal_document['number'])
        return lst_person_snils
    else:
        print('Ошибка. Не удалось получить сотрудников и их СНИЛСы. ' + response_dict.get('errorMessage'))
        return False


# получаем словарь должностей ({'position_id': 'position_name'})
def get_positions_dict(token, client_id):
    positions_response = requests.get(
        'https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/employeePositions',
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


# получаем id корневого отдела (по идее лучше бы это выполнить 1 раз при запуске программы, а то при создании нового
# отдела это вызывается каждый раз)
def get_root_department_id(token, client_id):
    root_department_response = requests.get(
        'https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/departments',
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


# получаем словарь отделов ({'department_id': 'department_name'})
def get_departments_dict(token, client_id):
    departments_response = requests.get(
        'https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/departments',
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


# получаем словарь существующих ролей в сервисе
# {'id': 'name'}
def get_employee_role_ids(token):
    departments_response = requests.get(
        'https://app-test1.hr-link.ru/api/v1/employeeRoles',
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


# получаем список существующих external_id для переданного legal_entity_id
def get_external_id_lst(token, client_id, legal_entity_id):
    employee_response = requests.get('https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/employees',
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
