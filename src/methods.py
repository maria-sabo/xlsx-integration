import json
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
        print('Ошибка. Вероятно, уже существует такой пользователь клиента. ' + response_dict.get('errorMessage'))
        return False


# создаем сотрудника, возвращается его employeeId
def create_employee_from_client_user(token, client_id, data_for_creating_employee):
    create_employee_response = requests.post('https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/employees',
                                             headers={'User-Api-Token': token},
                                             json=data_for_creating_employee)
    # response = create_employee_response.text
    response_dict = json.loads(create_employee_response.text)

    if response_dict.get('result'):
        created_employee = response_dict.get('employee')
        created_employee_id = created_employee.get('id')
        print('Сотрудник создан.')
        return created_employee_id
    else:
        print('Сотрудник не создан.')


# список всех снилсов в сервисе
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


# все ли юрлица из excel уже есть в сервисе
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

        for excel_legal_entity in excel_column_legal_entity:
            flag = False
            id_, name_ = '', ''
            for id_name, name in legal_entity_name_dict.items():
                if excel_legal_entity == name:
                    flag = True
                    id_ = id_name
                    name_ = name
            if flag:
                print('Юрлицо: "' + excel_legal_entity + '" есть у нас в сервисе')
                legal_entity_dict[id_] = name_
            else:
                print('Юрлица: "' + str(excel_legal_entity) + '" нет у нас в сервисе, мы не выгрузим сотрудников.')
                return False
    else:
        print('Ошибка получения списка юрлиц в сервисе. ' + response_dict.get('errorMessage'))
        return False
    return legal_entity_dict


def create_position(token, client_id, position_excel):
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


def get_position(token, client_id, position_excel):
    position_excel_response = requests.get(
        'https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/employeePositions',
        headers={'User-Api-Token': token})
    response_dict = json.loads(position_excel_response.text)
    if response_dict.get('result'):
        lst_positions = response_dict.get('employeePositions')
        for position in lst_positions:
            if position.get('name') == position_excel:
                position_id = position.get('id')
                return position_id
        # если нет должности, то создаем ее
        position_id = create_position(token, client_id, position_excel)
        return position_id
    else:
        print('Ошибка: ' + response_dict.get('errorMessage'))
        return False


def get_root_department(token, client_id):
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


def create_department(token, client_id, department_excel):
    root_department = get_root_department(token, client_id)
    data_for_creating_department = {
        "parentDepartmentId": root_department,
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


def get_department(token, client_id, department_excel):
    department_excel_response = requests.get(
        'https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/departments',
        headers={'User-Api-Token': token})
    response_dict = json.loads(department_excel_response.text)
    if response_dict.get('result'):
        lst_departments = response_dict.get('clientDepartments')
        for department in lst_departments:
            if department.get('name') == department_excel:
                department_id = department.get('id')
                return department_id
        # если нет должности, то создаем ее
        department_id = create_department(token, client_id, department_excel)
        return department_id
    else:
        print('Ошибка: ' + response_dict.get('errorMessage'))
        return False


def prepare_data_for_employee(token, client_id, client_user_id, legal_entity_dict, legal_entity_excel, position_excel,
                              department_excel):
    legal_entity_id = ''
    for id_name, name in legal_entity_dict.items():
        if name == legal_entity_excel:
            legal_entity_id = id_name
    position_id = get_position(token, client_id, position_excel)
    department_id = get_department(token, client_id, department_excel)

    data = {"clientUserId": client_user_id,
            "legalEntityId": legal_entity_id,
            "departmentId": department_id,
            "positionId": position_id,
            "roleIds": []}
    return data


def create_employee_full(token, client_id, data_for_creating_user, legal_entity_excel,
                         legal_entity_dict, position_excel, department_excel):
    try:
        client_user_id = create_client_user(token, client_id, data_for_creating_user)
        if client_user_id:
            data = prepare_data_for_employee(token, client_id, client_user_id, legal_entity_dict, legal_entity_excel,
                                             position_excel, department_excel)
            create_employee_from_client_user(token, client_id, data)
            print('!!!')
        else:
            print('...')
    except:
        print('Произошла ошибка при добавлении сотрудника.')
