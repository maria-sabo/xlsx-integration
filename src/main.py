import json

import pandas as pd
import requests
import numpy

from src.classes.added_user import UserPost
from src.classes.address import Address
from src.classes.doc import Doc
from src.classes.employee import Employee
from src.classes.passport import Passport
from src.get_client_id import get_client_id_by_token, get_client_user_id


def excel2class():
    df = pd.read_excel('test.xlsx', sheet_name=0)

    df.drop(df.index[0], inplace=True)
    df.drop(df.columns[0], axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)

    df.columns = df.columns.str.replace('\n', '')
    df.columns = df.columns.str.strip()

    df = df.astype(str)
    df.replace('nan', numpy.nan, inplace=True)
    print(df)

    all_users_excel_for_post = []
    info_about_user_work = []

    for i, row in df.iterrows():
        all_users_excel_for_post.insert(i, UserPost(row['*Фамилия']))
        all_users_excel_for_post[i].firstName = row['Имя']
        all_users_excel_for_post[i].patronymic = row['Отчество']
        all_users_excel_for_post[i].gender = row['Пол']
        all_users_excel_for_post[i].birthdate = row['Дата рождения']
        all_users_excel_for_post[i].phone = row['Номер телефона']

        all_users_excel_for_post[i].personalDocuments = []
        all_users_excel_for_post[i].personalDocuments.insert(i, Doc('SNILS', row['*СНИЛС']))
        all_users_excel_for_post[i].personalDocuments.append(Doc('INN', row['*ИНН ФЛ']))

        passport = Passport('PASSPORT', row['*Паспорт:Номер'], row['*Паспорт:Серия'])
        passport.issuedDate = row['Паспорт:Дата выдачи']
        passport.issuingAuthority = row['Паспорт:Кем выдан']
        passport.issuingAuthorityCode = row['Паспорт:Код подразделения']

        address = Address()
        address.postalCode = row['Адрес регистрации:Индекс']
        address.regionCode = row['Адрес регистрации:Регион']
        address.city = row['Адрес регистрации:Город']
        address.street = row['Адрес регистрации:Улица']
        address.house = row['Адрес регистрации:Дом']
        address.block = row['Адрес регистрации:Корпус/строение']
        address.flat = row['Адрес регистрации:Квартира']

        passport.registrationAddress = address
        all_users_excel_for_post[i].personalDocuments.append(passport)

        employee = Employee(row['*Юрлицо'], row['*Руководитель'], row['*Кадровый сотрудник'])
        employee.department = row['Отдел']
        employee.position = row['Должность']
        info_about_user_work.insert(i, employee)

        print(str(i) + ' person in JSON: \n')
        print(all_users_excel_for_post[i].toJSON())


def main():
    excel2class()
    data = {
        "lastName": "ФамилияJ",
        "firstName": "ИмяJ",
        "patronymic": "Отчество",
        "phone": "89223434343",
        "email": "emai234445@email.ru",
        "gender": "FEMALE",
        "birthdate": "1970-01-01",
        "personalDocuments": [
            {
                "number": "134-488-458 86",
                "type": "SNILS"
            },
            {
                "number": "961019652438",
                "type": "INN"
            },
            {
                "type": "PASSPORT",
                "serialNumber": "1488",
                "number": "888888",
                "issuedDate": "1990-01-01",
                "issuingAuthorityCode": "100-001",
                "issuingAuthority": "отделом УФМС ",
                "birthplace": "г. Москва",
                "registrationAddress": {
                    "postalCode": "185026",
                    "regionCode": "177",
                    "city": "Санкт-Петербург",
                    "street": "dd",
                    "house": "3",
                    "block": "2",
                    "flat": "12"
                }
            }
        ]
    }
    r = requests.get('https://app-test1.hr-link.ru/api/v1/version')
    print(r.text)

    user_api_token = '2abb743d-b6db-4d2f-8c49-d0feed4d5bca'
    print(get_client_id_by_token(user_api_token))

    get_client_user_id(user_api_token, get_client_id_by_token(user_api_token), data)


if __name__ == main():
    main()
