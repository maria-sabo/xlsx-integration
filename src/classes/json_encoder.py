import simplejson


# экземпляр класса можно будет сериализовать
# ignore_nan = True -- nan-ы из ячеек станут null
class JsonEncoder:

    def toJSON(self):
        return simplejson.dumps(self, default=lambda o: o.__dict__,
                                ensure_ascii=False, ignore_nan=True)
