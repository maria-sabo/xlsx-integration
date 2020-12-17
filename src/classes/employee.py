from src.classes.json_encoder import JsonEncoder


class Employee(JsonEncoder):
    """
    Экземпляр класса хранит информацию из excel-таблицы для создания сотрудника из пользователя клиента
    Поля юрлицо, руководитель, кадровик являются обязательными при создании экземпляра класса

    legalEntity: (String) Название юрлица
    department: (String) Название отдела
    position: (String) Название должности
    headManager: (Boolean) Является ли руководителем
    hrManager: (Boolean) Является ли кадровиком
    externalId: (String) Идентификатор во внешней системе
    """
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
