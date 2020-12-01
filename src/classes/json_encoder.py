import simplejson


class JsonEncoder:

    def toJSON(self):
        return simplejson.dumps(self, default=lambda o: o.__dict__,
                                ensure_ascii=False, ignore_nan=True)
