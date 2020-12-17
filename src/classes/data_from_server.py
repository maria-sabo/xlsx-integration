
class DataFromServer:
    """
    Экземпляр класса хранит данные, взятые с сервера

    root_department_id: Идентификатор корневого отдела
    head_manager_id: Идентификатор роли "Руководитель"
    hr_manager_id: Идентификатор роли "Кадровик"
    checked_legal_entity_dict: Словарь, содержащий пары идентификатор:название юрлица
    positions_dict: Словарь, содержащий пары идентификатор:название должности
    departments_dict: Словарь, содержащий пары идентификатор:название отдела
    """
    root_department_id = ''
    head_manager_id = ''
    hr_manager_id = ''
    checked_legal_entity_dict = ''
    positions_dict = ''
    departments_dict = ''
