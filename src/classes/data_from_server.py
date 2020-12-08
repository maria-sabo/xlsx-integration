# экземпляр класса будет хранить данные,
# полученные с сервера

#     root_department_id -- id корневого отдела

#     head_manager_id -- id роли "Руководитель"

#     hr_manager_id -- id роли "Кадровик"

#     checked_legal_entity_dict -- словарь {'id': 'legal_entity_name', ...} хранит данные
#     об уже записанных на сервере юрлицах

#     positions_dict -- словарь {'id': 'position_name', ...} хранит данные о записанных на сервере должностях,
#     при добавлении новой должности, ее 'id': 'position_name' записывается в словарь
#
#     departments_dict -- словарь {'id': 'department_name', ...} хранит данные о записанных на сервере отделах,
#     при добавлении нового отдела, его 'id': 'department_name' записывается в словарь
class DataFromServer:
    root_department_id = ''

    head_manager_id = ''
    hr_manager_id = ''
    checked_legal_entity_dict = ''
    positions_dict = ''

    departments_dict = ''
    # lst_person_snils = ''
