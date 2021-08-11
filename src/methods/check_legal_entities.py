import json
import requests

def check_legal_entities_excel(data, excel_column_legal_entity):
    """
    Проверяет существует ли каждое значение (название юрлица) из столбца "Юрлицо" excel-таблицы  в сервисе
        Если все названия юрлиц есть в сервисе, то функция возвращает словарь пар идентификатор-список
        (в списке будут находиться названия, которые присутствовали в excel-таблице,
        то есть одному индентификатору будет соответствовать список, содержащий либо только 'Название',
        либо только 'Сокращенное название', либо 'Название' и 'Сокращенное название' )
        Если хотя бы одного названия юрлица из столбца "Юрлицо" excel-таблицы нет в сервисе, то возвращает False

    :param data: Экземпляр класса DataCreateEmployee
        :data.tenant: Название поддомена клиента
        :data.token: api-токен клиента
        :data.client_id: Идентификатор клиента в сервисе
    :param excel_column_legal_entity: Массив строк из столбца "Юрлицо" excel-таблицы
    :return: Словарь {'id':['name', 'name'], 'id2': ['name2', 'name2'], ...}, либо False
    """
    legal_entity_response = requests.get(
        'https://' + data.tenant + '.hr-link.ru/api/v1/clients/' + data.client_id + '/legalEntities',
        headers={'User-Api-Token': data.token})
    response_dict = json.loads(legal_entity_response.text)
    legal_entity_dict = {}
    legal_entity_name_dict = {}
    if response_dict.get('result'):
        lst_legal_entities = response_dict.get('legalEntities')

        for legal_entity in lst_legal_entities:
            legal_entity_name_dict[legal_entity.get('id')] = [legal_entity.get('name'), legal_entity.get('shortName')]
        print('Проверка нахождения переданных юрлиц в нашем сервисе: \n')
        for excel_legal_entity in excel_column_legal_entity:
            flag = False
            id_, name_ = '', ''
            for id_name, name_lst in legal_entity_name_dict.items():

                if str(excel_legal_entity).lower() == name_lst[0].lower():
                    flag = True
                    id_ = id_name
                    name_ = name_lst[0]
                elif str(excel_legal_entity).lower() == str(name_lst[1]).lower():
                    flag = True
                    id_ = id_name
                    name_ = name_lst[1]
            if flag:
                print('Юрлицо: "' + excel_legal_entity + '" есть у нас в сервисе')
                if id_ in legal_entity_dict:
                    legal_entity_dict[id_].append(name_)
                    legal_entity_dict[id_] = list(set(legal_entity_dict[id_]))
                else:
                    legal_entity_dict[id_] = [name_]
            else:
                print('Юрлица: "' + str(excel_legal_entity) + '" нет у нас в сервисе, мы не выгрузим сотрудников.')
                return False
        print('\n')
    else:
        print('Ошибка получения списка юрлиц в сервисе. ' + response_dict.get('errorMessage'))
        return False

    return legal_entity_dict
