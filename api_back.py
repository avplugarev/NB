import bd_connector
import bottle
from truckpad.bottle.cors import CorsPlugin, enable_cors

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


@enable_cors
@app.route('/api/classifier/', method=['POST'])
def get_classifier():
    good_allowed_inputs = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6',
                 'name', 'composition', 'technicalDescription', 'gender', 'variantCode', 'vat',
                 'age', 'trackingType', 'material', 'jeansCut']
    gender = {0:'любой_пол', 1:'мужчинам', 2:'женщинам'}
    vat = {0: 'медицина', 10: 'детский', 20: 'товар_с_обычным_налогом'}
    trackingType = {'LOT': 'без_чипа', 'DMX': 'обувь', 'datamatrix': 'обувь', 'MEX': 'мех', 'обычный': 'без_чипа',
                    'LPR':'легпром', 'PRF':'парфюм', 'легпром':'легпром', 'парфюм':'парфюм'}
    material = {1:'текстиль', 2:'трикотаж', 3:'другое'}
    inputs=['gender','vat', 'trackingType', 'material']
    goods_description = []  # пустой список под описагния товаров

    goods_description_raw = bottle.request.json
    for value in goods_description_raw:
        for i in range(len(inputs)):
            if value.get(inputs[i], 'None') != 'None':
                temp=value.get(inputs[i])
                if i ==0:
                    value['gender']=gender[temp]
                elif i ==1:
                    value['vat'] = vat[temp]
                elif i ==2:
                    value['trackingType'] = trackingType[temp]
                elif i ==3:
                    value['material'] = material[temp]

        good = str()
        for j in range(len(good_allowed_inputs)):
            if value.get(good_allowed_inputs[j], 'None') !='None':
                if value != None:
                    good = good + ' ' + str(value[good_allowed_inputs[j]])
        goods_description.append(good)
    print(goods_description)

    return 'OK'





app.install(CorsPlugin(origins=['http://localhost:8000']))

if __name__ == "__main__":
    bottle.run(app, host="localhost", port=5000)