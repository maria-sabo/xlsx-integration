from src.classes.json_encoder import JsonEncoder


class User(JsonEncoder):
    """
    Экземпляр класса хранит данные для создания пользователя клиента
    Поля имя, фамилия являются обязательными при создании экземпляра класса

    lastName: (String) Фамилия
    firstName: (String) Имя
    patronymic: (String) Отчество
    gender: (String) Пол
    birthdate: (String) Дата рождения
    phone: (String) Телефон
    email: (String)
    personalDocuments: (List) Список, содержащий документы пользователя (SNILS, INN, PASSPORT)
    """
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
