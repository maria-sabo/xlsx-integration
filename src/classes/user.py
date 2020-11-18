from src.classes.address import Address
from src.classes.json_encoder import JsonEncoder
from src.classes.passport import Passport


class User(JsonEncoder):
    lastName = ''
    firstName = ''
    patronymic = ''
    gender = ''
    birthdate = ''
    phone = ''

    passport = Passport

    personalDocuments = []
    registrationAddress = Address

    legalEntity = ''
    department = ''
    position = ''
    headManager = ''
    hrManager = ''

    def __init__(self, lastName):
        self.lastName = lastName

    def __str__(self):
        return "Имя: {} \t Фамилия: {}\t Дата рождения: {}\t".format(self.firstName, self.lastName,
                                                                     self.birthdate)
