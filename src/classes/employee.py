from src.classes.json_encoder import JsonEncoder


class Employee(JsonEncoder):
    legalEntity = ''
    department = ''
    position = ''
    headManager = ''
    hrManager = ''

    def __init__(self, legalEntity, headManager, hrManager):
        self.legalEntity = legalEntity
        self.headManager = headManager
        self.hrManager = hrManager

    def __str__(self):
        return "Юрлицо: {} \t HR-менеджер: {} \t Руководитель: {}".format(self.legalEntity, self.headManager,
                                                                          self.hrManager)
