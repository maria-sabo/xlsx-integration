from src.classes.employee import Employee
from src.classes.user import User


class DataCreateEmployee:
    """
    Экземпляр класса хранит данные для полного создания сотрудника


    token: (String) api-токен клиента
    client_id: (String) Идентификатор клиента
    user: (User) Данные, взятые из excel, для создания пользователя клиента
    checked_legal_entity_dict: (Dict) Словарь, содержащий пары идентификатор:название юрлица
    positions_dict: (Dict) Словарь, содержащий пары идентификатор:название должности
    root_department_id: (String) Идентификатор корневого отдела
    departments_dict: (Dict) Словарь, содержащий пары идентификатор:название отдела
    head_manager_id: (String) Идентификатор роди "Руководитель"
    hr_manager_id: (String) Идентификатор роли "Кадровик"
    employee: (Employee) Данные, взятые из excel, для создания сотрудника из пользователя клиента
    """
    tenant = ''
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
