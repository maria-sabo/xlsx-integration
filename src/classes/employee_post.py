from src.classes.json_encoder import JsonEncoder


class EmployeePost(JsonEncoder):
    clientUserId = ''
    legalEntityId = ''
    departmentId = ''
    positionId = ''
    roleIds = []
    externalId = ''

    def __init__(self, clientUserId):
        self.clientUserId = clientUserId
