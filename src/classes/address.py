from src.classes.json_encoder import JsonEncoder


class Address(JsonEncoder):
    """
    Экземпляр класса хранит данные адреса регистрации пользователя

    postalCode: (String) Индекс
    regionCode: (String) Код региона
    city: (String) Город
    street: (String) Улица
    house: (String) Дом
    block: (String) Корпус
    flat: (String) Квартира
    """
    postalCode = ''
    regionCode = ''
    city = ''
    street = ''
    house = ''
    block = ''
    flat = ''
