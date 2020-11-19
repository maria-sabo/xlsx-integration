import requests

from src.convert import excel2class
from src.get_client_id import get_client_id_by_token


def main():
    r = requests.get('https://app-test1.hr-link.ru/api/v1/version')
    print(r.text)

    user_api_token = '1e542e4b-ee46-4982-a2de-727450f2046d'
    client_id = get_client_id_by_token(user_api_token)
    print(client_id)

    excel2class()


if __name__ == main():
    main()
