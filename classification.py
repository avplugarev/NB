from sklearn.naive_bayes import BernoulliNB  # импорт НБ Бернули
from sklearn.feature_extraction.text import CountVectorizer  # импортируем класс преобразования из текста в вектор
import numpy as np
from load_file_test import FileLoader

path = 'teach_file_sample.xlsx'  # путь к загружаемому файлу
path2='teach_test_sample.xlsx'
file_beforehand=FileLoader.load_file_new(path,1)

# загружаем обучающую выборку: описание товаров
model_goods_description = file_beforehand[0]
#model_goods_description1 = ['Женщины верхняя одежда куртка джинсовая куртка', 'Мужчины верхняя одежда куртка пуховик']

# загружаем обучающую выборку: значения категорий для обучающего множества товаров
model_goods_class_values = np.array(file_beforehand[1])
#model_goods_class_values = np.array(FileLoader.load_file_new(path,1)[1])

#model_goods_class_values1 = np.array([1, 2])

# создаем пустой словарь
model_vocabular = CountVectorizer()
#model_vocabular1 = CountVectorizer()

# заполняем словарь и токенизируем
model_vocabular.fit(model_goods_description)
#print(model_vocabular.vocabulary_)
#model_vocabular1.fit(model_goods_description1)

# создаем набор векторов обучающего множества товаров
model_goods_vectors = model_vocabular.transform(model_goods_description)
#print(model_goods_vectors.shape)
#model_goods_vectors1 = model_vocabular.transform(model_goods_description1)

# создаем пустую модель
model = BernoulliNB()
#model1 = BernoulliNB()

# обучаем модель
model.fit(model_goods_vectors.toarray(), model_goods_class_values)
#model1.fit(model_goods_vectors1.toarray(), model_goods_class_values1)

# загружаем описание товара для классификации
good_without_class_description = FileLoader.load_file_new(path2,2)[0]
print(good_without_class_description)

# перводим описание товара в векторную форму используя созданный ранее словарб
good_without_class_vector = model_vocabular.transform(good_without_class_description)

# получаем предполагаемую категорию в классификаторе
good_class = model.predict(good_without_class_vector.toarray())
print('Рузультат классификации:',good_class, '\n', file_beforehand[2])

#статистика по тестированию





