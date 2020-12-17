import bd_connector
import bottle
from truckpad.bottle.cors import CorsPlugin, enable_cors
import bd_connector

app = bottle.Bottle()


def clear_file_data(working_sheet):
    good_rows = ['Class_ID', 'Уровень 1', 'Уровень 2', 'Уровень 3', 'Уровень 4', 'Уровень 5', 'Уровень 6',
                 'Наименование (<=250)', 'Техническое описание', 'Пол', 'Размер производителя  (<=10)', 'НДС',
                 'Возраст+', 'Тип чипа', 'Тип ткани', 'Тип кроя/джинсы']
    for row in working_sheet:
        for cell in row:
            if cell.value not in good_rows:
                working_sheet.delete_cols(cell.column)  # удаляем столбцы, если их заголовки нам не нужны
        break
    working_sheet.delete_rows(0)
    return working_sheet


def get_goods_descriptions(raw_description,request_type):
    # зводим словари для обработки описания товара
    ##словарь разрешенных полей
    good_allowed_inputs = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6',
                           'name', 'composition', 'technicalDescription', 'gender', 'items', 'vat',
                           'age', 'trackingType', 'material', 'jeansCut']
    ##cловари справочников для замены
    gender = {0: 'любой_пол', 1: 'мужчинам', 2: 'женщинам'}
    vat = {0: 'медицина', 10: 'детский', 20: 'товар_с_обычным_налогом'}
    trackingType = {'LOT': 'без_чипа', 'DMX': 'обувь', 'datamatrix': 'обувь', 'MEX': 'мех', 'обычный': 'без_чипа',
                    'LPR': 'легпром', 'PRF': 'парфюм', 'легпром': 'легпром', 'парфюм': 'парфюм'}
    material = {1: 'текстиль', 2: 'трикотаж', 3: 'другое'}
    inputs = ['gender', 'vat', 'trackingType', 'material', 'items']

    goods_description = []  # пустой список под описания товаров

    for value in raw_description:
        # заменяемм цифровые значения полей описания товара на текстовые значения из справочников
        for i in range(len(inputs)):
            if value.get(inputs[i], 'None') != 'None':
                temp = value.get(inputs[i])
                sizes = str()
                if i == 0:
                    value['gender'] = gender[temp]
                elif i == 1:
                    value['vat'] = vat[temp]
                elif i == 2:
                    value['trackingType'] = trackingType[temp]
                elif i == 3:
                    value['material'] = material[temp]
                elif i == 4:
                    for k in range(len(value['items'])):
                        temp2 = value['items'][k]
                        temp2 = temp2.get('variantCode')
                        sizes = sizes + ' ' + temp2
                    value['items'] = sizes

        classificator_path = str()  # пустой классификатор
        for l in range(6):
            if value.get(good_allowed_inputs[l], 'None') != 'None':
                if value.get(good_allowed_inputs[l]) == '' or value.get(good_allowed_inputs[l]) == 'None':
                    classificator_path = classificator_path + ' None'
                else:
                    classificator_path = classificator_path + ' ' + value.get(good_allowed_inputs[l])

        # отфильтровываемм в описании товара только нужные поля
        good = str()  # переменная под описние отдельного поля
        for j in range(len(good_allowed_inputs)):
            if value.get(good_allowed_inputs[j], 'None') != 'None':
                if value != None:
                    good = good + ' ' + str(value[good_allowed_inputs[j]])
        goods_description.append(good)
    if request_type == 'class':
        return goods_description
    elif request_type =='confirm':
        return goods_description, classificator_path


@enable_cors
@app.route('/api/classifier/', method=['POST'])
def get_classifier():
    goods_description = get_goods_descriptions(bottle.request.json, 'class')

    return goods_description


@enable_cors
@app.route('/api/confirm_class/', method=['POST'])
def confirm_class():
    path = dict()
    categories=bd_connector.read_confirmed_category()
    print(categories)
    data_raw = bottle.request.json
    path['category'] = data_raw[0].get('category', 'None')
    data=get_goods_descriptions([data_raw[0].get('goods_description', 'None')], 'confirm')
    path['path']=data[1]
    path['uid']=categories[1]+1
    good=data[0]
    bd_connector.add_category_to_dict_categories(path)

    print('пвть\n', path)
    print('дескриптор\n', good)
    return 'ok'


app.install(CorsPlugin(origins=['http://localhost:8000']))

if __name__ == "__main__":
    bottle.run(app, host="localhost", port=5000)
