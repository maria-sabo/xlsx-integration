from src.classes.json_encoder import JsonEncoder


class Doc(JsonEncoder):
    """
    Экземпляр класса хранит тип и номер документа
    Оба поля являются обязательными при создании экземпляра класса

    type: (String) Тип документа ('SNILS', 'INN')
    number: (String) Номер документа
    """
    type = ''
    number = ''

    def __init__(self, type, number):
        self.type = type
        self.number = number
