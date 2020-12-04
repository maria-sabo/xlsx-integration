# получаем id переданной в excel-е должности у нас в сервисе
# если такой должности не существует, создаем ее и получаем новый id
import numpy

from src.methods.create_for_employee import create_position, create_department


def get_position(token, client_id, position_excel, positions_dict):
    # dict_positions = get_positions_dict(token, client_id)
    for position_id, position_name in positions_dict.items():
        if type(position_excel) is float and numpy.isnan(position_excel):
            # если ячейка не заполнена, то
            return ""
        else:
            if position_name.lower() == position_excel.lower():
                return position_id
    # если нет должности, то создаем ее
    position_id = create_position(token, client_id, position_excel)
    positions_dict[position_id] = position_excel
    return position_id


# получаем id переданного в excel-е отдела у нас в сервисе
# если такого отдела не существует, создаем его и получаем новый id
def get_department(token, client_id, department_excel, root_department_id, departments_dict):
    # dict_departments = get_departments_dict(token, client_id)
    for department_id, department_name in departments_dict.items():
        if type(department_excel) is float and numpy.isnan(department_excel):
            # если ячейка не заполнена, то
            # department_id = create_department(token, client_id, department_excel)
            return ""
        else:
            if department_name.lower() == department_excel.lower():
                return department_id

    # если нет отдела, то создаем его
    department_id = create_department(token, client_id, department_excel, root_department_id)
    departments_dict[department_id] = department_excel
    return department_id


# на основе переданных значений из excel
# возвращает список ролей для создания сотрудника
def get_role_ids(head_manager_excel, hr_manager_excel, head_manager_id, hr_manager_id):
    role_ids = []
    # for employee_role_id, employee_role_name in employee_roles_dict.items():
    #     if employee_role_name == 'Руководитель':
    #         head_manager_id = employee_role_id
    #     elif employee_role_name == 'Кадровик':
    #         hr_manager_id = employee_role_id
    if head_manager_excel and hr_manager_excel:
        role_ids.append(head_manager_id)
        role_ids.append(hr_manager_id)
    elif head_manager_excel:
        role_ids.append(head_manager_id)
    elif hr_manager_excel:
        role_ids.append(hr_manager_id)
    return role_ids


def get_external_id(external_id, external_id_lst):
    if external_id in external_id_lst:
        print(
            'Такой ID сотрудника во внешней системе уже существует в данном юрлице. Сотрудник создастся без '
            'external_id.')
        return None
    else:
        external_id_lst.append(external_id)
        return external_id
