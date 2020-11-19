import requests

from src.convert import excel2class
from src.get_client_id import get_client_id_by_token, get_client_user_id, create_employee, prepare_data_for_employee


def main():
    excel2class()

    r = requests.get('https://app-test1.hr-link.ru/api/v1/version')
    print(r.text)

    user_api_token = '1e542e4b-ee46-4982-a2de-727450f2046d'
    client_id = get_client_id_by_token(user_api_token)
    print(client_id)

    lst = excel2class()
    print(lst[0].toJSON())
    print(1)
    client_user_id = get_client_user_id(user_api_token, client_id, data_for_creating_user=lst[0].toJSON())
    create_employee(user_api_token, client_id, prepare_data_for_employee(client_user_id))


if __name__ == main():
    main()
