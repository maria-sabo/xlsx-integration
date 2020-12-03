import json
import numpy
import requests


# получаем id текущего клиента с помощью токена


def get_client_id_by_token(token):
    current_user_response = requests.get('https://app-test1.hr-link.ru/api/v1/currentUser',
                                         headers={'User-Api-Token': token})
    response_dict = json.loads(current_user_response.text)
    if response_dict.get('result'):
        current_user = response_dict.get('currentUser')
        clients_of_current_user = current_user.get('clients')
        client_id = clients_of_current_user[0].get('id')
        return client_id
    else:
        print('Ошибка. Вероятно, передан некорректный токен.')
    return False


# создаем пользователя клиента (person), возвращается его clientUserId
def create_client_user(token, client_id, data_for_creating_user):
    create_user_response = requests.post('https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/users',
                                         headers={'User-Api-Token': token},
                                         json=data_for_creating_user)
    response_dict = json.loads(create_user_response.text)
    if response_dict.get('result'):
        current_user = response_dict.get('clientUser')
        client_user_id = current_user.get('id')
        print('Добавлен пользователь клиента.')
        return client_user_id
    else:
        print('Ошибка.' + response_dict.get('errorMessage'))
        return False


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


# проверка, все ли юрлица из excel уже есть в сервисе
def check_legal_entities_excel(token, client_id, excel_column_legal_entity):
    legal_entity_response = requests.get('https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/legalEntities',
                                         headers={'User-Api-Token': token})
    response_dict = json.loads(legal_entity_response.text)
    legal_entity_dict = {}
    legal_entity_name_dict = {}
    if response_dict.get('result'):
        lst_legal_entities = response_dict.get('legalEntities')

        for legal_entity in lst_legal_entities:
            legal_entity_name_dict[legal_entity.get('id')] = legal_entity.get('name')
        print('Проверка нахождения переданных юрлиц в нашем сервисе: \n')
        for excel_legal_entity in excel_column_legal_entity:
            flag = False
            id_, name_ = '', ''
            for id_name, name in legal_entity_name_dict.items():
                if excel_legal_entity.lower() == name.lower():
                    flag = True
                    id_ = id_name
                    name_ = name
            if flag:
                print('Юрлицо: "' + excel_legal_entity + '" есть у нас в сервисе')
                legal_entity_dict[id_] = name_
            else:
                print('Юрлица: "' + str(excel_legal_entity) + '" нет у нас в сервисе, мы не выгрузим сотрудников.')
                return False
        print('\n')
    else:
        print('Ошибка получения списка юрлиц в сервисе. ' + response_dict.get('errorMessage'))
        return False
    return legal_entity_dict


# создается новая должность
def create_position(token, client_id, position_excel):
    if type(position_excel) is float and numpy.isnan(position_excel):
        return ""
    data_for_creating_position = {
        "name": position_excel
    }
    create_position_response = requests.post(
        'https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/employeePositions',
        headers={'User-Api-Token': token},
        json=data_for_creating_position)
    response_dict = json.loads(create_position_response.text)

    if response_dict.get('result'):
        created_position = response_dict.get('employeePosition')
        created_position_id = created_position.get('id')
        print('Новая должность добавлена.')
        return created_position_id
    else:
        print('Должность не добавлена. Произошла ошибка: ' + response_dict.get('errorMessage'))


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


# получаем id переданной в excel-е должности у нас в сервисе
# если такой должности не существует, создаем ее и получаем новый id
def get_position(token, client_id, position_excel):
    dict_positions = get_positions_dict(token, client_id)
    for position_id, position_name in dict_positions.items():
        if type(position_excel) is float and numpy.isnan(position_excel):
            # если ячейка не заполнена, то
            return ""
        else:
            if position_name.lower() == position_excel.lower():
                return position_id
            else:
                # если нет должности, то создаем ее
                position_id = create_position(token, client_id, position_excel)
                return position_id


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


# создание отдела
def create_department(token, client_id, department_excel, root_department_id):
    if type(department_excel) is float and numpy.isnan(department_excel):
        return ""

    data_for_creating_department = {
        "parentDepartmentId": root_department_id,
        "name": department_excel
    }
    create_department_response = requests.post(
        'https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/departments',
        headers={'User-Api-Token': token},
        json=data_for_creating_department)
    response_dict = json.loads(create_department_response.text)

    if response_dict.get('result'):
        created_department = response_dict.get('clientDepartment')
        created_department_id = created_department.get('id')
        print('Новый отдел добавлен.')
        return created_department_id
    else:
        print('Отдел не добавлен. Произошла ошибка: ' + response_dict.get('errorMessage'))


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


# получаем id переданного в excel-е отдела у нас в сервисе
# если такого отдела не существует, создаем его и получаем новый id
def get_department(token, client_id, department_excel, root_department_id):
    dict_departments = get_departments_dict(token, client_id)
    for department_id, department_name in dict_departments.items():
        if type(department_excel) is float and numpy.isnan(department_excel):
            # если ячейка не заполнена, то
            # department_id = create_department(token, client_id, department_excel)
            return ""
        else:
            if department_name.lower() == department_excel.lower():
                return department_id
            else:
                # если нет отдела, то создаем его
                department_id = create_department(token, client_id, department_excel, root_department_id)
                return department_id


# получаем словарь существующих ролей в сервисе
# {'id': 'name'}
def get_employee_roles_dict(token):
    departments_response = requests.get(
        'https://app-test1.hr-link.ru/api/v1/employeeRoles',
        headers={'User-Api-Token': token})
    response_dict = json.loads(departments_response.text)
    employee_roles_dict = {}
    if response_dict.get('result'):
        employee_roles = response_dict.get('employeeRoles')
        for employee_role in employee_roles:
            employee_roles_dict[employee_role.get('id')] = employee_role.get('name')
        return employee_roles_dict
    else:
        print('Ошибка: ' + response_dict.get('errorMessage'))
        return False


# на основе переданных значений из excel
# возвращает список ролей для создания сотрудника
def get_role_ids(token, head_manager_excel, hr_manager_excel, employee_roles_dict):
    role_ids = []
    # employee_roles_dict = get_employee_roles_dict(token)
    for employee_role_id, employee_role_name in employee_roles_dict.items():
        if employee_role_name == 'Руководитель':
            head_manager_id = employee_role_id
        elif employee_role_name == 'Кадровик':
            hr_manager_id = employee_role_id
    if head_manager_excel and hr_manager_excel:
        role_ids.append(head_manager_id)
        role_ids.append(hr_manager_id)
    elif head_manager_excel:
        role_ids.append(head_manager_id)
    elif hr_manager_excel:
        role_ids.append(hr_manager_id)
    return role_ids


# готовим данные для создания employee
# data =      {"clientUserId": client_user_id,
#             "legalEntityId": legal_entity_id,
#             "departmentId": department_id,
#             "positionId": position_id,
#             "roleIds": []}
def prepare_data_for_employee(token, client_id, client_user_id, legal_entity_dict, legal_entity_excel, position_excel,
                              department_excel, root_department_id, head_manager_excel, hr_manager_excel,
                              employee_roles_dict):
    legal_entity_id = ''
    for id_name, name in legal_entity_dict.items():
        if name == legal_entity_excel:
            legal_entity_id = id_name
    position_id = get_position(token, client_id, position_excel)
    department_id = get_department(token, client_id, department_excel, root_department_id)
    role_ids = get_role_ids(token, head_manager_excel, hr_manager_excel, employee_roles_dict)

    data = {"clientUserId": client_user_id,
            "legalEntityId": legal_entity_id,
            "departmentId": department_id,
            "positionId": position_id,
            "roleIds": role_ids}
    return data


# создаем сотрудника
# возвращается его employeeId
def create_employee_from_client_user(token, client_id, data_for_creating_employee):
    create_employee_response = requests.post('https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/employees',
                                             headers={'User-Api-Token': token},
                                             json=data_for_creating_employee)
    response_dict = json.loads(create_employee_response.text)

    if response_dict.get('result'):
        created_employee = response_dict.get('employee')
        created_employee_id = created_employee.get('id')
        print('Сотрудник создан.')
        return created_employee_id
    else:
        print('Сотрудник не создан.')


# полное создание одного сотрудника:
# создаем client_user
# готовим данные для создания employee
# создаем employee
def create_employee_full(token, client_id, data_for_creating_user, legal_entity_dict, root_department_id,
                         employee_roles_dict, employee):
    legal_entity_excel = employee.legalEntity
    position_excel = employee.position
    department_excel = employee.department

    head_manager_excel = employee.headManager
    hr_manager_excel = employee.hrManager
    try:
        client_user_id = create_client_user(token, client_id, data_for_creating_user)
        if client_user_id:

            data = prepare_data_for_employee(token, client_id, client_user_id, legal_entity_dict, legal_entity_excel,
                                             position_excel, department_excel, root_department_id, head_manager_excel,
                                             hr_manager_excel, employee_roles_dict)
            create_employee_from_client_user(token, client_id, data)
            print('!!!')
        else:
            print('...')
    except:
        print('Произошла ошибка при добавлении сотрудника.')
