import json

import requests
from src.convert import xlsx2df, data2class
from src.methods import get_client_id_by_token, create_employee_full, check_legal_entities_excel, get_root_department, \
    create_department, get_position, get_department


def main():
    r = requests.get('https://app-test1.hr-link.ru/api/v1/version')
    print('Welcome: ' + r.text + '\n')

    file_name = 'user_snils.txt'
    token = '275a7c54-e874-4e86-8006-ce18fa3d22ca'

    # получаем id клиента
    client_id = get_client_id_by_token(token)
    if client_id:
        df = xlsx2df(excel_name='test3.xlsx')
        excel_column_legal_entity = df['Юрлицо'].values
        legal_entity_dict = check_legal_entities_excel(token, client_id, excel_column_legal_entity)
        print(get_root_department(token, client_id))
        print(get_department(token, client_id, 'dkdkd'))

        if legal_entity_dict:
            for i, row in df.iterrows():
                user, snils, employee = data2class(row, file_name)
                legal_entity_excel = ''
                position_excel = ''
                department_excel = ''
                if employee:
                    legal_entity_excel = employee.legalEntity
                    position_excel = employee.position
                    department_excel = employee.department
                if user:
                    data_client_user = json.loads(user.toJSON())
                    print('creating employee #: ' + str(i))
                    create_employee_full(token, client_id, data_client_user, file_name, snils,
                                         legal_entity_excel, legal_entity_dict, position_excel, department_excel)
    else:
        print('клиент не найден')


if __name__ == main():
    main()
