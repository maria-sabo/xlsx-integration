from src.classes.json_encoder import JsonEncoder


# класс для хранения данных пользователя
# обязательные поля -- фамилия, имя
# без них не создать экземпляр класса
class User(JsonEncoder):
    lastName = ''
    firstName = ''
    patronymic = ''
    gender = ''
    birthdate = ''
    phone = ''
    email = ''

    # SNILS, INN, PASSPORT (внутри PASSPORT registrationAddress)
    personalDocuments = []

    def __init__(self, lastName, firstName):
        self.lastName = lastName
        self.firstName = firstName
