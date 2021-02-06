import bottle
from truckpad.bottle.cors import CorsPlugin, enable_cors
import module_load_data as module_load
import module_data_classification
import module_model_education as module_educ
import numpy as  np
import bd_connector as bd

app = bottle.Bottle()

class API_back:

    def __init__(self):
        self.raw_data = list()
        self.results = dict()

    def get_goods_descr(self, data):
        pass

    def need_NB_class(path):
        check = bd.get_category_id_from_confirmed_categ(path)
        if check == None:
            return 'yes'
        else:
            return check

# метод API получения категории по описанию товара
@enable_cors
@app.route('/api/classifier/', method=['POST'])
def get_classifier():
    global model2  # храним обученную ранее модель

    # получаем описание товара из запроса (0 - описание и 1 - путь к категории у поставщика)
    data = module_load.DataLoader.import_api_data(bottle.request.json)
    paths = data.goods_supplier_classes  # путь до категорий в классификаторе поставщика
    goods_description = data.goods_description  # описание товара
    # производим классификацию
    my_response = dict()  ## заводим пустой словарь под ответы
    for i in range(len(goods_description)):
        path = ' '.join(paths[i])
        check = API_back.need_NB_class(path[i]) ## для каждого поисания проверяем нужна ли классификация по NB
        if check != 'yes':
            my_response[
                'Категория товара №{0}'.format(i + 1)] = check  ## присваиваем категорию из базы елси не нужен NB
        else:
            ## Присвоимваем категорию на оснвое NB
            ### переводим в векторную форму описания товара для классификации
            good = goods_description[i]  # получаем описание отдельного товара для классификации
            good = [good]  # переводим его в элемент списока
            ### перводим в массив
            dood_without_class_vector = module_load.DataPreprocessed.goods_vectors(good, model2.vocabular)
            ### получаем нампи массив результата классификации
            result = module_data_classification.Classify.get_class(model2.model, dood_without_class_vector)
            ### получаем нампи массив результата классификации
            result = np.ndarray.tolist(result)
            ### добавляем результат в справочник массива
            my_response['Категория товара №{0}'.format(i + 1)] = result
    return my_response

# метод API для записи в базу подтвержденной модератором категории
@enable_cors
@app.route('/api/confirm_class/', method=['POST'])
def confirm_class():
    good = dict()  # пустой словарь, в который сложим данные для записи в базу
    categories = bd.read_confirmed_category() # получаем список подтвержденных категорий
    educt_data = bd.read_prepared_data() # получаем список описаний товаров для обучения
    data_raw = bottle.request.json  # получаем данные сырого запроса
    data = module_load.DataLoader.import_api_data([data_raw[0].get('goods_description', 'None')])
    path = data.goods_supplier_classes  # путь до категорий в классификаторе поставщика
    goods_description = data.goods_description  # описание товара
    good['category'] = data_raw[0].get('category', 'None')  # записывае номер категории
    good['path'] = ' '.join(path[0]) # путь к категории - пока только одной - сдалать цикл на несколько
    good['uid_path'] = categories[1] + 1  # id в таблице подтвержденных категорий
    good['uid_educ'] = educt_data[2] + 1  # id в таблице с обучающими описаниями
    good['description'] = ' '.join(goods_description) # описание товара
    bd.add_category_to_dict_categories(good)
    bd.add_good_to_prepared_data(good)

    return 'Данные добавлены в БД.'

# метод API авторизации
@enable_cors
@app.route("/api/login/", method=["POST"])
def do_login():
    login = bottle.request.json.get('login')
    password = bottle.request.json.get('password')
    check = bd.user_login_check(login, password);
    if check == True:
        bottle.response.set_cookie("account", login, secret='some-secret-key')
        return 'OK'
    else:
        return 'login fail'


app.install(CorsPlugin(origins=['http://localhost:8000']))

if __name__ == "__main__":
    model2 = module_educ.ModelEducation()
    model2 = module_educ.ModelEducation.teach_classifier(model2)
    bottle.run(app, host="localhost", port=5000)