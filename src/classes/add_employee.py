from src.classes.json_encoder import JsonEncoder


class AddEmployee(JsonEncoder):
    """
    Экземпляр класса хранит данные для осуществления POST-запроса для создания сотрудника из пользователя клиента
    В конструкторе происходит обязательное установление clientUserId в экземпляр класса

    clientUserId: (String) Идентификатор пользователя клиента
    legalEntityId: (String) Идентификатор юрлица, в котором будет создан сотрудник
    departmentId: (String) Идентификатор отдела, в котором будет создан сотрудник
    positionId: (String) Идентификатор должности, в которой будет создан сотрудник
    roleIds: (List) Список идентификаторов ролей, назначенных сотруднику
    externalId: (String) Идентификатор во внешней системе
    """
    clientUserId = ''
    legalEntityId = ''
    departmentId = ''
    positionId = ''
    roleIds = []
    externalId = ''

    def __init__(self, clientUserId):
        self.clientUserId = clientUserId
