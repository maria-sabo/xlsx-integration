import json
import requests


# получаем id текущего клиента с помощью токена
def get_client_id_by_token(token):
    current_user_response = requests.get('https://app-test1.hr-link.ru/api/v1/currentUser',
                                         headers={'User-Api-Token': token})
    s = current_user_response.text
    d = json.loads(s)
    current_user = d.get('currentUser')
    clients_of_current_user = current_user.get('clients')
    client_id = clients_of_current_user[0].get('id')
    return client_id


# после создания пользователя клиента получаем clientUserId, уже для создания сотрудника из пользователя
def get_client_user_id(token, client_id, data_for_creating_user):
    create_user_response = requests.post('https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/users',
                                         headers={'User-Api-Token': token}, json=data_for_creating_user)
    s = create_user_response.text
    d = json.loads(s)
    current_user = d.get('currentUser')
    client_user_id = current_user.get('id')
    return client_user_id


def create_employee(token, client_id, data_for_creating_employee):
    create_employee_response = requests.post('https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/employees',
                                             headers={'User-Api-Token': token}, json=data_for_creating_employee)
    s = create_employee_response.text
    d = json.loads(s)

    # ! проверить что result : true

    created_employee = d.get('employee')
    created_employee_id = created_employee.get('id')
    return created_employee_id
