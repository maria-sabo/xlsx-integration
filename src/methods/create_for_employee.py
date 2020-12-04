import json

import numpy
import requests


# создание должности
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
