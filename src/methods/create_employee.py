import json
import requests

from src.classes.add_employee import AddEmployee
from src.convert import data2class
from src.methods.create_client_user import create_client_user
from src.methods.get_for_employee import get_external_id, get_department, get_role_ids, get_position
from src.methods.data_from_server import get_external_id_lst

'''
data.token, data.client_id, client_user_id,
data.checked_legal_entity_dict,
legal_entity_excel,
position_excel, data.positions_dict, department_excel,
data.root_department_id,
data.departments_dict,
head_manager_excel,
hr_manager_excel, data.head_manager_id, data.hr_manager_id,
external_id_excel
'''


def prepare_data_for_employee(data, client_user_id, legal_entity_excel,
                              position_excel,  department_excel,
                              head_manager_excel, hr_manager_excel, external_id_excel):
    """
    Функция готовит данные для создания сотрудника из пользователя клиента, собирает данные в словарь

    :param client_user_id: Идентификатор созданного пользователя клиента
    :param data: структура данных DataCreateEmployee
        :data.checked_legal_entity_dict: Словарь, содержащий пары идентификатор-[
            сокращенное название юрлица (если есть в excel),название (если есть в excel)]
        :data.positions_dict: Словарь, содержащий идентификатор-название должности, уже записанных в сервисе
    :param legal_entity_excel: Массив с названиями юрлиц из excel-таблицы
    :param position_excel: Название должности, взятое из excel-таблицы
    :param department_excel: Название отдела, взятое из excel-таблицы
    :param head_manager_excel: Булевое значение, из excel-таблицы, является ли сотрудник руководителем
    :param hr_manager_excel: Булевое значение, из excel-таблицы, является ли сотрудник кадровиком
    :param external_id_excel: Идентификатор внешней системы, взятый из excel
    :return: Десериализованный JSON-объект (словарь), для использования в теле POST-запроса для создания сотрудника
    из пользователя клиента
    Возвращаемое значение имеет следующую структуру:
        data = {"clientUserId": client_user_id,
                "legalEntityId": legal_entity_id,
                "departmentId": department_id,
                "positionId": position_id,
                "roleIds": [role_ids],
                "externalId": external_id}
    """
    legal_entity_id = ''
    for id_name, name in data.checked_legal_entity_dict.items():
        if (name[0] == legal_entity_excel) or (name[1] == legal_entity_excel):
            legal_entity_id = id_name

    external_id_lst = get_external_id_lst(data, legal_entity_id)
    external_id = get_external_id(external_id_excel, external_id_lst)
    position_id = get_position(data, position_excel)
    department_id = get_department(data, department_excel)
    role_ids = get_role_ids(head_manager_excel, hr_manager_excel, data)
    add_employee = AddEmployee(client_user_id)
    add_employee.legalEntityId = legal_entity_id
    add_employee.departmentId = department_id
    add_employee.positionId = position_id
    add_employee.roleIds = role_ids
    add_employee.externalId = external_id
    data = json.loads(add_employee.toJSON())
    print(data)
    return data


def create_employee_from_client_user(data, data_for_creating_employee):
    """
    Функция посылает POST-запрос на создание сотрудника из пользователя клиента

    :param data: структура данных DataCreateEmployee
        :data.tenant: Название поддомена клиента
        :data.token: api-токен клиента
        :data.client_id: Идентификатор клиента в сервисе
    :param data_for_creating_employee: Словарь, содержащий данные для создания сотрудника
    :return: Идентификатор созданного сотрудника
    """
    create_employee_response = requests.post(
        'https://' + data.tenant + '.hr-link.ru/api/v1/clients/' + data.client_id + '/employees',
        headers={'User-Api-Token': data.token},
        json=data_for_creating_employee)
    response_dict = json.loads(create_employee_response.text)
    print(response_dict)

    if response_dict.get('result'):
        created_employee = response_dict.get('employee')
        created_employee_id = created_employee.get('id')
        print('Сотрудник создан.')
        return created_employee_id
    else:
        print('Сотрудник не создан.')


def create_employee_full(data):
    """
    Функция выполняет функцию по созданию пользователя клиента
    Если пользователь клиента успешно создан,
    то выполняет функцию по приготовлению данных для создания сотрудника и создает сотрудника

    :param data: Экземпляр класса DataCreateEmployee, содержащий все данные, нужные для создания пользователя клиента
    и сотрудника
    """
    data_for_creating_user = json.loads(data.user.toJSON())
    legal_entity_excel = data.employee.legalEntity
    position_excel = data.employee.position
    department_excel = data.employee.department

    head_manager_excel = data.employee.headManager
    hr_manager_excel = data.employee.hrManager

    external_id_excel = data.employee.externalId
    try:
        client_user_id = create_client_user(data, data_for_creating_user)
        if client_user_id:
            print('---')
            data_em = prepare_data_for_employee(data, client_user_id, legal_entity_excel,
                                                    position_excel, department_excel, 
                                                    head_manager_excel, hr_manager_excel, external_id_excel)
            print(data_em)
            create_employee_from_client_user(data, data_em)
            print('!!!')
        else:
            print('...')
    except:
        print('Произошла ошибка при добавлении сотрудника.')


def create_employees(data, data_users, df):
    """
    Происходит цикл по всем строкам dataframe
        Данные каждой строки записываются в экземпляры классов User, Employee
            Если они корректны (не произошло ошибки валидации),
            то они записываются в экземпляр класса DataCreateEmployee
            И вызывается функция полного создания сотрудника

    :param data: Экземпляр класса DataCreateEmployee, содержащий все данные, нужные для создания пользователя клиента
    :param data_users: Экземпляр класса DataFromServerAboutUsers, содержащий данные, взятые с сервера
    :param df: DataFrame, содержащий данные из excel-таблицы
    """
    for i, row in df.iterrows():
        print('creating employee #: ' + str(i))
        user, employee = data2class(row, data_users)
        if user and employee:
            data.user = user
            data.employee = employee
            create_employee_full(data)
        else:
            print('ERROR')
