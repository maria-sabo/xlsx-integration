# -*- coding: utf-8 -*-

import json
import sys
import requests
from src.convert import xlsx2df, data2class, get_snils
from src.methods import get_client_id_by_token, create_employee_full, check_legal_entities_excel, lst_snils, \
    get_employee_roles_dict, get_role_ids, get_root_department_id

ARGS_COUNT = 3


def main():
    print('Welcome: ' + requests.get('https://app-test1.hr-link.ru/api/v1/version').text + '\n')

    if sys.argv.__len__() == ARGS_COUNT:
        excel_name = sys.argv[1]
        token = sys.argv[2]

        client_id = get_client_id_by_token(token)
        root_department_id = get_root_department_id(token, client_id)
        employee_roles_dict = get_employee_roles_dict(token)

        if client_id:
            df = xlsx2df(excel_name)
            excel_column_legal_entity = df['Юрлицо'].values
            legal_entity_dict = check_legal_entities_excel(token, client_id, excel_column_legal_entity)
            lst_person_snils = lst_snils(token, client_id)

            if legal_entity_dict:
                for i, row in df.iterrows():
                    print('creating employee #: ' + str(i))
                    snils = get_snils(row)

                    if snils and not (snils in lst_person_snils):
                        user, employee = data2class(row)
                        if user and employee:
                            data_for_creating_user = json.loads(user.toJSON())
                            create_employee_full(token, client_id, data_for_creating_user, legal_entity_dict,
                                                 root_department_id,
                                                 employee_roles_dict, employee)
                            lst_person_snils.append(snils)
                    else:
                        print('Пользователь с таким СНИЛСом уже существует в сервисе. Или введен некорректный СНИЛС.')
        else:
            print('Клиент не найден.')
    else:
        print(
            'Введите три аргумента: \n - путь к запускаемому файлу (main.py) \n - путь к xlsx файлу, из которого будут '
            'выгружаться сотрудники \n - токен клиента')


if __name__ == main():
    main()
