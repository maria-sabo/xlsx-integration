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
        print('наверно некорректный токен')
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
        print('добавлен пользователь клиента')
        return client_user_id
    else:
        print('наверно есть такой пользователь клиента: ' + response_dict.get('errorMessage'))
        return False


# создаем сотрудника, возвращается его employeeId
def create_employee_from_client_user(token, client_id, data_for_creating_employee):
    create_employee_response = requests.post('https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/employees',
                                             headers={'User-Api-Token': token},
                                             json=data_for_creating_employee)
    response = create_employee_response.text
    response_dict = json.loads(response)

    if response_dict.get('result'):
        created_employee = response_dict.get('employee')
        created_employee_id = created_employee.get('id')
        print('сотрудник создан ура')
        return created_employee_id
    else:
        print('сотрудник не создан')


def data_for_employee(client_user_id):
    data = {"clientUserId": client_user_id,
            "legalEntityId": "e22411b3-75db-45ef-a37c-5a5225f21746",
            "departmentId": "",
            "positionId": "",
            "roleIds": []}
    return data


def create_employee_full(token, client_id, data_for_creating_user, file_name, snils):
    client_user_id = create_client_user(token, client_id, data_for_creating_user)
    if client_user_id:
        data = data_for_employee(client_user_id)
        create_employee_from_client_user(token, client_id, data)
        with open(file_name, 'a') as f:
            f.write(snils + '\n')
        f.close()
        print('!!!')
    else:
        print('...')
