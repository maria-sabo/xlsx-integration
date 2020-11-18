from src.classes.json_encoder import JsonEncoder


class UserPost(JsonEncoder):
    lastName = ''
    firstName = ''
    patronymic = ''
    gender = ''
    birthdate = ''
    phone = ''
    email = ''

    # SNILS, INN, PASSPORT (внутри PASSPORT registrationAddress)
    personalDocuments = []

    def __init__(self, lastName):
        self.lastName = lastName

    def __str__(self):
        return "Имя: {} \t Фамилия: {}\t Дата рождения: {}\t".format(self.firstName, self.lastName,
                                                                     self.birthdate)
