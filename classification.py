from sklearn.naive_bayes import BernoulliNB  # импорт НБ Бернули
from sklearn.feature_extraction.text import CountVectorizer  # импортируем класс преобразования из текста в вектор
import numpy as np
from load_file_test import FileLoader
import statistic
import time
import bd_connector

def load_educ_data_to_bd(path):
    print(bd_connector.edu_data_delete())
    file_beforehand = FileLoader.load_file(path)  # проводим предварительные преобразование обучащей выборки
    model_goods_description = file_beforehand[0]  # список с описанием товаров для обучения
    #model_goods_class_values = np.array(file_beforehand[1])  # список со значениями категорий для обучения
    educt_data_counter = bd_connector.read_prepared_data()[
        2]  # получаем id последнего добавленного в базу в таблицу подготовленных данных товара
    for i in range(len(model_goods_description)):
        data_to_add_bd = dict()
        educt_data_counter = educt_data_counter + 1
        data_to_add_bd['uid_educ'] = educt_data_counter
        data_to_add_bd['description'] = model_goods_description[i]
        data_to_add_bd['category'] = file_beforehand[1][i]
        data_to_add_bd['path'] = file_beforehand[2][i]
        bd_connector.add_good_to_prepared_data(
            data_to_add_bd)  # потоварно складываем в базу описание подготовленных для обучения товаров
    return 'Обучающие данные загружены в базу'

def teach_classifier():
    data_from_db = bd_connector.read_prepared_data() #получаем из базы описния товаров, набор категорий для них
    model_goods_description = data_from_db[0] ##набор описаний товаров
    #print(model_goods_description)

    model_goods_class_values = np.array(data_from_db[1]) ##набор категорий
    #print(model_goods_class_values)

    model_vocabular = CountVectorizer()  # инициируем пустой словарь

    model_vocabular.fit(model_goods_description)  # заполняем словарь и токенизируем
    model_goods_vectors = model_vocabular.transform(
        model_goods_description)  # создаем набор векторов обучающего множества товаров

    model = BernoulliNB()  # создаем пустую модель

    model.fit(model_goods_vectors.toarray(), model_goods_class_values)  # обучаем модель

    return model, model_vocabular  # возвращаем обученную модель и словарь


def good_preparation(path, model_vocabular):
    good_without_class_description = FileLoader.load_file(path)  # проводим предварительную обработку описания
    good_without_class_vector = model_vocabular.transform(
        good_without_class_description[0])  # переводим описание в векторную форму
    return good_without_class_vector.toarray(), good_without_class_description  # возвращаем массиф вектров с описанием товаров


def classifay(model, good_without_class_vector):
    good_class = model.predict(good_without_class_vector)
    return good_class


path = 'file_to_load/teach_file_sample.xlsx'  # обучающий файл
path2 = 'teach_test_sample.xlsx'  # боевой тестируемый файл
path3 = 'отладочный файл'  # для тестов и замеров
start_time_edu = time.time()

#загружаем данные для обучения в базу
#print(load_educ_data_to_bd(path))

#обучаем модель
#model = teach_classifier()

#готовим товары к оценке
#start_time_clas = time.time()
#goods = good_preparation(path, model[1])


#получаем результаты оценки
#result = classifay(model[0], goods[0])
#print('\nРезультаты классификации товаров:',result, '\n')

# статистика по тестированию
#for value in (statistic.quality_classification(goods[1][0],goods[1][1],result, start_time_edu, start_time_clas, goods[1][2])):
 #   print(value)



