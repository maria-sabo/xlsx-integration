import json
import simplejson


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, int):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class JsonEncoder:

    def toJSON(self):
        return simplejson.dumps(self, default=lambda o: o.__dict__,
                                sort_keys=True, indent=4, ensure_ascii=False, ignore_nan=True)
