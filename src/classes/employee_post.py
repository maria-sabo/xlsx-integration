from src.classes.json_encoder import JsonEncoder


class EmployeePost(JsonEncoder):
    clientUserId = ''
    legalEntityId = ''
    departmentId = ''
    positionId = ''
    roleIds = []

    def __init__(self, clientUserId):
        self.clientUserId = clientUserId
