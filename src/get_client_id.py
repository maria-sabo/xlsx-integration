import json
import requests


# получаем id текущего клиента с помощью токена
def get_client_id_by_token(token):
    current_user_response = requests.get('https://app-test1.hr-link.ru/api/v1/currentUser',
                                         headers={'User-Api-Token': token})
    response = current_user_response.text
    response_dict = json.loads(response)
    current_user = response_dict.get('currentUser')
    clients_of_current_user = current_user.get('clients')
    client_id = clients_of_current_user[0].get('id')
    return client_id


# после создания пользователя клиента получаем clientUserId, уже для создания сотрудника из пользователя
def get_client_user_id(token, client_id, data_for_creating_user):
    create_user_response = requests.post('https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/users',
                                         headers={'User-Api-Token': token}, json=data_for_creating_user)
    response = create_user_response.text
    response_dict = json.loads(response)
    if response_dict.get('result') == True:
        current_user = response_dict.get('clientUser')
        client_user_id = current_user.get('id')
        return client_user_id
    else:
        print('наверно есть такой юзер')


def create_employee(token, client_id, data_for_creating_employee):
    create_employee_response = requests.post('https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/employees',
                                             headers={'User-Api-Token': token}, json=data_for_creating_employee)
    response = create_employee_response.text
    response_dict = json.loads(response)

    # ! проверить что result : true
    if response_dict.get('result') == True:
        created_employee = response_dict.get('employee')
        created_employee_id = created_employee.get('id')
        print('сотрудник создан ура')
        return created_employee_id
    else:
        print('что то не так')


def prepare_data_for_employee(client_user_id):
    data = {"clientUserId": client_user_id,
            "legalEntityId": "e22411b3-75db-45ef-a37c-5a5225f21746",
            "departmentId": "",
            "positionId": "",
            "roleIds": []}
    return data


def create_employee_full(token, data_for_creating_user):
    client_id = get_client_id_by_token(token)

    client_user_id = get_client_user_id(token, client_id, data_for_creating_user)

    data_for_employee = prepare_data_for_employee(client_user_id)
    create_employee(token, client_id, data_for_employee)
