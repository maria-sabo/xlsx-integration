from src.classes.json_encoder import JsonEncoder


# класс для хранения документа
# будет храниться тип документа (например, 'SNILS' или 'INN')
# и номер документа
class Doc(JsonEncoder):
    type = ''
    number = ''

    def __init__(self, type, number):
        self.type = type
        self.number = number
