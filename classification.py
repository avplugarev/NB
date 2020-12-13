from sklearn.naive_bayes import BernoulliNB  # импорт НБ Бернули
from sklearn.feature_extraction.text import CountVectorizer  # импортируем класс преобразования из текста в вектор
import numpy as np
from load_file_test import FileLoader
import statistic
import time


def teach_classifier(path):
    file_beforehand = FileLoader.load_file(path) # проводим предварительные преобразование обучащей выборки
    model_goods_description = file_beforehand[0]  # список с описанием товаров для обучения
    model_goods_class_values = np.array(file_beforehand[1])  # список со значениями категорий для обучения
    model_vocabular = CountVectorizer()  # инициируем пустой словарь

    model_vocabular.fit(model_goods_description)  # заполняем словарь и токенизируем
    # print(model_vocabular.vocabulary_)
    model_goods_vectors = model_vocabular.transform(
        model_goods_description)  # создаем набор векторов обучающего множества товаров
    # print(model_goods_vectors.shape)
    model = BernoulliNB()  # создаем пустую модель
    model.fit(model_goods_vectors.toarray(), model_goods_class_values)  # обучаем модель
    return model, model_vocabular  # возвращаем обученную модель и словарь


def good_preparation(path, model_vocabular):
    good_without_class_description = FileLoader.load_file(path)  # проводим предварительную обработку описания
    # print(good_without_class_description[0])
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

#обучаем модель
model = teach_classifier(path)

#готовим товары к оценке
start_time_clas = time.time()
goods = good_preparation(path, model[1])

#получаем результаты оценки
result = classifay(model[0], goods[0])
print('\nРезультаты классификации товаров:',result, '\n')

# статистика по тестированию
for value in (statistic.quality_classification(goods[1][0],goods[1][1],result, start_time_edu, start_time_clas, goods[1][2])):
    print(value)



