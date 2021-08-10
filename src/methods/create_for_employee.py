import json
import numpy
import requests



def create_position(data, position_excel):
    """
    Функция посылает POST-запрос на создание должности

    :param token: api-токен клиента
    :param client_id: Идентификатор клиента в сервисе
    :param position_excel: Название должности из excel
    :return: Идентификатор созданной должности
    """
    if type(position_excel) is float and numpy.isnan(position_excel):
        return ""
    data_for_creating_position = {
        "name": position_excel
    }
    create_position_response = requests.post(
        'https://' + data.tenant + '.hr-link.ru/api/v1/clients/' + data.client_id + '/employeePositions',
        headers={'User-Api-Token': data.token},
        json=data_for_creating_position)
    response_dict = json.loads(create_position_response.text)
    if response_dict.get('result'):
        created_position = response_dict.get('employeePosition')
        created_position_id = created_position.get('id')
        print('Новая должность добавлена.')
        return created_position_id
    else:
        print('Должность не добавлена. Произошла ошибка: ' + response_dict.get('errorMessage'))


def create_department(data, department_excel):
    """
    Функцция посылает POST-запрос на создание отдела

    :param token: api-токен клиента
    :param client_id: Идентификатор клиента в сервисе
    :param department_excel: Название отдела из excel
    :param root_department_id: Идентификатор корневого отдела
    :return: Идентификатор созданного отдела
    """
    if type(department_excel) is float and numpy.isnan(department_excel):
        return ""

    data_for_creating_department = {
        "parentDepartmentId": data.root_department_id,
        "name": department_excel
    }
    create_department_response = requests.post(
        'https://' + data.tenant + '.hr-link.ru/api/v1/clients/' + data.client_id + '/departments',
        headers={'User-Api-Token': data.token},
        json=data_for_creating_department)
    response_dict = json.loads(create_department_response.text)

    if response_dict.get('result'):
        created_department = response_dict.get('clientDepartment')
        created_department_id = created_department.get('id')
        print('Новый отдел добавлен.')
        return created_department_id
    else:
        print('Отдел не добавлен. Произошла ошибка: ' + response_dict.get('errorMessage'))
