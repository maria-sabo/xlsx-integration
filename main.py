# -*- coding: utf-8 -*-

import json
import sys
import requests
from src.convert import xlsx2df, data2class, get_snils
from src.data_validate import is_inn_correct
from src.methods import get_client_id_by_token, create_employee_full, check_legal_entities_excel, lst_snils


def main():
    r = requests.get('https://app-test1.hr-link.ru/api/v1/version')
    print('Welcome: ' + r.text + '\n')

    if sys.argv.__len__() == 3:
        excel_name = sys.argv[1]
        token = sys.argv[2]
        # print(is_correct_snils('193-045-68581'))
        #print(is_inn_correct('960365629321'))

        client_id = get_client_id_by_token(token)

        if client_id:
            df = xlsx2df(excel_name)
            excel_column_legal_entity = df['Юрлицо'].values
            legal_entity_dict = check_legal_entities_excel(token, client_id, excel_column_legal_entity)
            lst_person_snils = lst_snils(token, client_id)

            if legal_entity_dict:
                for i, row in df.iterrows():
                    snils = get_snils(row)
                    if snils:
                        snils = snils.replace(' ', '').replace('-', '')

                    if not (snils in lst_person_snils):
                        user, employee = data2class(row)
                        if user and employee:
                            legal_entity_excel = employee.legalEntity
                            position_excel = employee.position
                            department_excel = employee.department

                            data_client_user = json.loads(user.toJSON())
                            print('creating employee #: ' + str(i))

                            create_employee_full(token, client_id, data_client_user, legal_entity_excel,
                                                 legal_entity_dict,
                                                 position_excel, department_excel)

                            lst_person_snils.append(snils)
                        else:
                            print('Некорректный СНИЛС, ИНН или паспорт.')
                    else:
                        print('Пользователь с таким снилсом уже существует в сервисе.')
        else:
            print('Клиент не найден.')
    else:
        print(
            'Введите три аргумента: \n - путь к запускаемому файлу (main.py) \n - путь к xlsx файлу, из которого будут '
            'выгружаться сотрудники \n - токен клиента')


if __name__ == main():
    main()
