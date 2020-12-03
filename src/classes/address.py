from src.classes.json_encoder import JsonEncoder


# класс для хранения адреса регистрации
class Address(JsonEncoder):
    postalCode = ''
    regionCode = ''
    city = ''
    street = ''
    house = ''
    block = ''
    flat = ''
