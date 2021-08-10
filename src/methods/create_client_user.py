import json
import requests



def get_client_id_by_token(data):#token):
    """
    Функция посылает GET-запрос на получение текущего пользователя,
    из ответа на запрос берет идентификатор текущего пользователя по заданному токену

    :param token: api-токен клиента
    :return: Идентификатор клиента, либо False (если что-то пошло не так, например, неедйствительный токен, то False)
    """
    current_user_response = requests.get('https://' + data.tenant + '.hr-link.ru/api/v1/currentUser',
                                         headers={'User-Api-Token': data.token})
    response_dict = json.loads(current_user_response.text)
    if response_dict.get('result'):
        current_user = response_dict.get('currentUser')
        clients_of_current_user = current_user.get('clients')
        client_id = clients_of_current_user[0].get('id')
        return client_id
    else:
        print('Ошибка. Вероятно, передан некорректный токен.')
    return False


def create_client_user(data, data_for_creating_user):
    """
    Функция посылает POST-запрос на создание пользователя клиента

    :param token: api-токен клиента
    :param client_id: Идентификатор клиента в сервисе
    :param data_for_creating_user: JSON-объект, содержащий данные для создания пользователя клиента
    :return: Идентификатор созданного пользователя клиента, либо False (если что-то пошло не так -- False)
    """
    create_user_response = requests.post('https://' + data.tenant + '.hr-link.ru/api/v1/clients/' + data.client_id + '/users',
                                         headers={'User-Api-Token': data.token},
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
