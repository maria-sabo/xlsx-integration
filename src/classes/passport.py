from src.classes.address import Address
from src.classes.json_encoder import JsonEncoder


class Passport(JsonEncoder):
    type = ''
    number = ''
    birthplace = ''
    serialNumber = ''
    issuedDate = ''
    issuingAuthority = ''
    issuingAuthorityCode = ''
    registrationAddress = Address

    def __init__(self, type, number, serialNumber):
        self.type = type
        self.number = number
        self.serialNumber = serialNumber
