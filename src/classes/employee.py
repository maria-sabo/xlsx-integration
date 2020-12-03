from src.classes.json_encoder import JsonEncoder


class Employee(JsonEncoder):
    legalEntity = ''
    department = ''
    position = ''
    headManager = None
    hrManager = None
    externalId = ''

    def __init__(self, legalEntity, headManager, hrManager):
        self.legalEntity = legalEntity
        self.headManager = headManager
        self.hrManager = hrManager
