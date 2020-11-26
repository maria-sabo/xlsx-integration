import json

import requests
from src.convert import xlsx2df, data2class
from src.get_client_id import get_client_id_by_token, create_employee_full


def main():
    r = requests.get('https://app-test1.hr-link.ru/api/v1/version')
    print('Welcome: ' + r.text + '\n')

    file_name = 'user_snils.txt'
    token = '0cbc63d4-563a-46d8-b7a4-8e04cd6d0751'

    client_id = get_client_id_by_token(token)
    if client_id:
        df = xlsx2df(file_name='test2.xlsx')

        for i, row in df.iterrows():
            user, snils = data2class(row, file_name)
            if user:
                data = json.loads(user.toJSON())
                print('creating employee #: ' + str(i))
                create_employee_full(token, client_id, data, file_name, snils)


if __name__ == main():
    main()
