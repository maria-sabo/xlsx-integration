import pandas as pd
import numpy

from src.classes.user import User
from src.classes.address import Address
from src.classes.doc import Doc
from src.classes.employee import Employee
from src.classes.passport import Passport
from src.data_validate import gender_validate, date_validate, phone_validate, authority_code_validate, \
    postal_code_validate, snils_validate


def get_snils(row):
    return row['СНИЛС']


def data2class(row):
    user = User(row['Фамилия'])
    user.firstName = row['Имя']
    user.patronymic = row['Отчество']

    user.gender = gender_validate(row['Пол'])
    user.birthdate = date_validate(row['Дата рождения'])
    user.phone = phone_validate(row['Номер телефона'])
    user.email = row['Электронная почта']

    user.personalDocuments = []
    passport = Passport('PASSPORT', row['Паспорт:Номер'], row['Паспорт:Серия'])
    passport.issuedDate = date_validate(row['Паспорт:Дата выдачи'])
    passport.issuingAuthority = row['Паспорт:Кем выдан']
    passport.issuingAuthorityCode = authority_code_validate(row['Паспорт:Код подразделения'])
    passport.birthplace = row['Паспорт:Место рождения']

    address = Address()
    address.postalCode = postal_code_validate(row['Адрес регистрации:Почтовый индекс'])
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

    return user, employee


def xlsx2df(excel_name):
    df = pd.read_excel(excel_name, sheet_name=0)

    df.drop([0, 1], inplace=True)
    df.drop(df.columns[0], axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.columns = df.columns.str.replace('\n', '')
    df.columns = df.columns.str.strip()

    df = df.astype(str)
    df.replace('nan', numpy.nan, inplace=True)
    return df
