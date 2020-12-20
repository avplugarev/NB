import bd_connector
import bottle
from truckpad.bottle.cors import CorsPlugin, enable_cors
import bd_connector
import classification
import numpy as np
from sklearn.naive_bayes import BernoulliNB  # импорт НБ Бернули
from sklearn.feature_extraction.text import CountVectorizer  # импортируем класс преобразования из текста в вектор

app = bottle.Bottle()


# метод очистки ненужных полей из описания товара
# def clear_file_data(working_sheet):
#   good_rows = ['Class_ID', 'Уровень 1', 'Уровень 2', 'Уровень 3', 'Уровень 4', 'Уровень 5', 'Уровень 6',
#               'Наименование (<=250)', 'Техническое описание', 'Пол', 'Размер производителя  (<=10)', 'НДС',
#              'Возраст+', 'Тип чипа', 'Тип ткани', 'Тип кроя/джинсы']
# for row in working_sheet:
#   for cell in row:
#      if cell.value not in good_rows:
#         working_sheet.delete_cols(cell.column)  # удаляем столбцы, если их заголовки нам не нужны
# break
# working_sheet.delete_rows(0)
# return working_sheet

# метод очистки ненужных полей из описания товара
def get_goods_descriptions(raw_description, request_type):
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
    if request_type == 'class':  # отрефакторить у ублрать условное возвращение. теперь всего нужне пять исходный
        return goods_description, classificator_path
    elif request_type == 'confirm':
        return goods_description, classificator_path


def need_NB_class(path):
    check = bd_connector.get_category_id_from_confirmed_categ(path)
    if check == None:
        return 'yes'
    else:
        return check


# метод API получения категории по описанию товара
@enable_cors
@app.route('/api/classifier/', method=['POST'])
def get_classifier():
    global model #храним обученную ранее модель

    #model = classification.teach_classifier()  # обучаем модель

    # получаем описание товара из запроса (0 - описание и 1 - путь к категории у поставщика)
    data = get_goods_descriptions(bottle.request.json, 'class')  # отрефакторить отказ от второго параметра
    path = data[1] #путь до категории в классификаторе поставщика
    goods_description = data[0] #описание товара

    # производим классификацию
    my_response = dict()  ##заводим пустой словарь под ответы

    for i in range(len(goods_description)):
        check = need_NB_class(path)  ##для каждого поисания проверяем нужна ли классификация по NB

        if check != 'yes':
            my_response['Категория товара №{0}'.format(i + 1)] = check  ##присваиваем категорию из базы елси не нужен NB
        else:
            ##Присвоимваем категорию на оснвое NB
            ###переводим в векторную форму описания товара для классификации
            good = goods_description[i] #получаем описание отдельного товара для классификации
            good = [good] #переводим его в элемент списока
            good_without_class_vector = model[1].transform(good)

            ###перводим в массив
            good_without_class_vector = good_without_class_vector.toarray()

            ###получаем нампи массив результата классификации
            result = classification.classifay(model[0],
                                                  good_without_class_vector)
            ###получаем нампи массив результата классификации
            result = np.ndarray.tolist(result)

            ###добавляем результат в справочник массива
            my_response['Категория товара №{0}'.format(i + 1)] = result
    return my_response

# метод API для записи в базу подтвержденной модератором категории
@enable_cors
@app.route('/api/confirm_class/', method=['POST'])
def confirm_class():
    good = dict()  # пустой словарь, в который сложим данные для записи в базу
    categories = bd_connector.read_confirmed_category()  # получаем список подтвержденных категорий
    educt_data = bd_connector.read_prepared_data()  # получаем список описаний товаров для обучения
    data_raw = bottle.request.json  # получаем данные сырого запроса
    good['category'] = data_raw[0].get('category', 'None')  # записывае номер категории
    data = get_goods_descriptions([data_raw[0].get('goods_description', 'None')], 'confirm')
    good['path'] = data[1]  # путь к категории
    good['uid_path'] = categories[1] + 1  # id в таблице подтвержденных категорий
    good['uid_educ'] = educt_data[2] + 1  # id в таблице с обучающими описаниями
    good['description'] = data[0][0]  # описание товара
    bd_connector.add_category_to_dict_categories(good)
    bd_connector.add_good_to_prepared_data(good)
    return 'Данные добавлены в БД.'


# метод API авторизации
@enable_cors
@app.route("/api/login/", method=["POST"])
def do_login():
    login = bottle.request.json.get('login')
    password = bottle.request.json.get('password')
    check = bd_connector.user_login_check(login, password);
    if check == True:
        bottle.response.set_cookie("account", login, secret='some-secret-key')
        return 'OK'
    else:
        return 'login fail'


app.install(CorsPlugin(origins=['http://localhost:8000']))

if __name__ == "__main__":
    model = classification.teach_classifier()  # обучаем модель
    bottle.run(app, host="localhost", port=5000)
    #model = classification.teach_classifier()  # обучаем модель
