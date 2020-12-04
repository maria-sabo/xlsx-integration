# проверка, все ли юрлица из excel уже есть в сервисе
import json

import requests


def check_legal_entities_excel(token, client_id, excel_column_legal_entity):
    legal_entity_response = requests.get('https://app-test1.hr-link.ru/api/v1/clients/' + client_id + '/legalEntities',
                                         headers={'User-Api-Token': token})
    response_dict = json.loads(legal_entity_response.text)
    legal_entity_dict = {}
    legal_entity_name_dict = {}
    if response_dict.get('result'):
        lst_legal_entities = response_dict.get('legalEntities')

        for legal_entity in lst_legal_entities:
            legal_entity_name_dict[legal_entity.get('id')] = legal_entity.get('name')
        print('Проверка нахождения переданных юрлиц в нашем сервисе: \n')
        for excel_legal_entity in excel_column_legal_entity:
            flag = False
            id_, name_ = '', ''
            for id_name, name in legal_entity_name_dict.items():
                if excel_legal_entity.lower() == name.lower():
                    flag = True
                    id_ = id_name
                    name_ = name
            if flag:
                print('Юрлицо: "' + excel_legal_entity + '" есть у нас в сервисе')
                legal_entity_dict[id_] = name_
            else:
                print('Юрлица: "' + str(excel_legal_entity) + '" нет у нас в сервисе, мы не выгрузим сотрудников.')
                return False
        print('\n')
    else:
        print('Ошибка получения списка юрлиц в сервисе. ' + response_dict.get('errorMessage'))
        return False
    return legal_entity_dict
