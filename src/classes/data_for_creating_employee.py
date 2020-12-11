from src.classes.employee import Employee
from src.classes.user import User


# класс, хранящий данные для создания сотрудника
class DataCreateEmployee:
    token = ''
    client_id = ''

    user = User

    checked_legal_entity_dict = {}
    positions_dict = {}
    root_department_id = ''
    departments_dict = {}

    head_manager_id = ''
    hr_manager_id = ''

    employee = Employee
