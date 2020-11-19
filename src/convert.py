import pandas as pd
import numpy

from src.classes.added_user import User
from src.classes.address import Address
from src.classes.doc import Doc
from src.classes.employee import Employee
from src.classes.passport import Passport


def data2class(i, row, all_users_excel_for_post):
    info_about_user_work = []

    all_users_excel_for_post.insert(i, User(row['Фамилия']))
    all_users_excel_for_post[i].firstName = row['Имя']
    all_users_excel_for_post[i].patronymic = row['Отчество']
    all_users_excel_for_post[i].gender = row['Пол']
    all_users_excel_for_post[i].birthdate = row['Дата рождения']
    all_users_excel_for_post[i].phone = row['Номер телефона']
    all_users_excel_for_post[i].email = row['Электронная почта']

    all_users_excel_for_post[i].personalDocuments = []
    all_users_excel_for_post[i].personalDocuments.insert(i, Doc('SNILS', row['СНИЛС']))
    all_users_excel_for_post[i].personalDocuments.append(Doc('INN', row['ИНН ФЛ']))

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
    all_users_excel_for_post[i].personalDocuments.append(passport)

    employee = Employee(row['Юрлицо'], row['Руководитель'], row['Кадровый сотрудник'])
    employee.department = row['Отдел']
    employee.position = row['Должность']
    info_about_user_work.insert(i, employee)
    return all_users_excel_for_post


def excel2class():
    df = pd.read_excel('test2.xlsx', sheet_name=0)

    df.drop([0, 1], inplace=True)
    df.drop(df.columns[0], axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(df)
    df.columns = df.columns.str.replace('\n', '')
    df.columns = df.columns.str.strip()

    df = df.astype(str)
    df.replace('nan', numpy.nan, inplace=True)

    all_users_excel_for_post = []
    info_about_user_work = []

    for i, row in df.iterrows():
        data2class(i, row, all_users_excel_for_post)
    return all_users_excel_for_post
