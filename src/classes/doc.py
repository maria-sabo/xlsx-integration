from src.classes.json_encoder import JsonEncoder


class Doc(JsonEncoder):
    type = ''
    number = ''

    def __init__(self, type, number):
        self.type = type
        self.number = number
