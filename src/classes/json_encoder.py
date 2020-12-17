import simplejson


class JsonEncoder:
    """
    Класс, от которого будут наследоваться другие классы
    Наследуемые от него классы можно будет сериализовать

    def toJSON(self): Метод, позволдяющий сериализовать экземпляр класса, ignore_nan = True -- nan-ы из ячеек
    не будут сериализованы
    """

    def toJSON(self):
        return simplejson.dumps(self, default=lambda o: o.__dict__,
                                ensure_ascii=False, ignore_nan=True)
