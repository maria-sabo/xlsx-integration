from src.classes.json_encoder import JsonEncoder


# экземпляр класса будет хранить полученные из excel таблицы данные для создания сотрудника из client_user
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
