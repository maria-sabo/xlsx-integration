import os

import pandas as pd
import numpy
import json

from src.classes.added_user import User
from src.classes.address import Address
from src.classes.doc import Doc
from src.classes.employee import Employee
from src.classes.passport import Passport


def data2class(row, file_name):
    snils = row['СНИЛС']
    if not os.path.exists(file_name):
        with open(file_name, 'w+') as f:
            f.close()
    with open(file_name, 'r') as f:
        if snils in f.read():
            print('юзер с таким снилсом уже был добавлен')
        else:
            user = User(row['Фамилия'])
            user.firstName = row['Имя']
            user.patronymic = row['Отчество']
            user.gender = row['Пол']
            user.birthdate = row['Дата рождения']
            user.phone = row['Номер телефона']
            user.email = row['Электронная почта']

            user.personalDocuments = []
            passport = Passport('PASSPORT', row['Паспорт:Номер'], row['Паспорт:Серия'])
            passport.issuedDate = row['Паспорт:Дата выдачи']
            passport.issuingAuthority = row['Паспорт:Кем выдан']
            passport.issuingAuthorityCode = row['Паспорт:Код подразделения']
            passport.birthplace = row['Паспорт:Место рождения']

            address = Address()
            address.postalCode = row['Адрес регистрации:Почтовый индекс']
            address.regionCode = row['Адрес регистрации:Регион']
            address.city = row['Адрес регистрации:Город']
            address.street = row['Адрес регистрации:Улица']
            address.house = row['Адрес регистрации:Дом']
            address.block = row['Адрес регистрации:Корпус/строение']
            address.flat = row['Адрес регистрации:Квартира']

            passport.registrationAddress = address
            user.personalDocuments.append(passport)
            user.personalDocuments.append(Doc('SNILS', row['СНИЛС']))
            user.personalDocuments.append(Doc('INN', row['ИНН ФЛ']))

            employee = Employee(row['Юрлицо'], row['Руководитель'], row['Кадровый сотрудник'])
            employee.department = row['Отдел']
            employee.position = row['Должность']

            return user, snils, employee
    f.close()
    return False, False, False


def xlsx2df(excel_name):
    df = pd.read_excel(excel_name, sheet_name=0)

    df.drop([0, 1], inplace=True)
    df.drop(df.columns[0], axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(df)
    df.columns = df.columns.str.replace('\n', '')
    df.columns = df.columns.str.strip()

    df = df.astype(str)
    df.replace('nan', numpy.nan, inplace=True)
    return df
