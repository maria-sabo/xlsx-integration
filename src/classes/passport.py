from src.classes.address import Address
from src.classes.json_encoder import JsonEncoder


# класс для хранения данных паспорта
# обязательные поля -- тип, серия, номер
# без них не создать экземпляр класса
class Passport(JsonEncoder):
    """
    Экземпляр класса хранит данные паспорта
    Поля тип, серия, номер являются обязательными при создании экземпляра класса

    type: (String) Тип паспорта, предполагается 'PASSPORT'
    number: (String) Номер паспорта
    birthplace: (String) Место рождения из паспорта
    serialNumber: (String) Серия паспорта
    issuedDate: (String) Дата выдачи паспорта
    issuingAuthority: (String) Кем выдан паспорт
    issuingAuthorityCode: (String) Код подразделения
    registrationAddress: (Address) Адрес регистрации
    """
    type = ''
    number = ''
    birthplace = ''
    serialNumber = ''
    issuedDate = ''
    issuingAuthority = ''
    issuingAuthorityCode = ''
    registrationAddress = Address

    def __init__(self, type, number, serialNumber):
        self.type = type
        self.number = number
        self.serialNumber = serialNumber
