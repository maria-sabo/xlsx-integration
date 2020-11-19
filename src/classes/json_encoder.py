import ast
import simplejson


class JsonEncoder:

    def toJSON(self):
        # return simplejson.dumps(self, default=lambda o: o.__dict__,
        #                         sort_keys=True, indent=4, ensure_ascii=False, ignore_nan=True)
        return ast.literal_eval(simplejson.dumps(self, default=lambda o: o.__dict__,
                                ensure_ascii=False, ignore_nan=True))
