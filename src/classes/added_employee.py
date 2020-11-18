from src.classes.json_encoder import JsonEncoder


class EmployeePost(JsonEncoder):
    clientUserId = ''
    legalEntityId = ''
    departmentId = ''
    positionId = ''
    roleIds = []

    def __init__(self, clientUserId, legalEntityId):
        self.clientUserId = clientUserId
        self.legalEntityId = legalEntityId

    def __str__(self):
        return "clientUserId: {} \t legalEntityId: {}".format(self.clientUserId, self.legalEntityId)
