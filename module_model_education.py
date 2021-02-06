from sklearn.naive_bayes import BernoulliNB  # импорт НБ Бернули
from module_load_data import DataPreprocessed as dt
from module_load_data import DataLoader as loader
import module_data_classification as mdclas
import bd_connector as bd
import numpy as np
import time

"""
    Класс обучения модели на основе загруженных данных.
"""


class ModelEducation:
    def __init__(self):
        self.model = str()
        self.vocabular = str()
        self.result = str()

    """
        метод обучения модели на основе обучающей выборки
    """

    def teach_classifier(self):
        data_from_db = bd.read_prepared_data()  # получаем из базы описния товаров, набор категорий для них
        self.vocabular = dt.get_vocabular(data_from_db[0])  # получаем словарь
        model_goods_vectors = dt.goods_vectors(data_from_db[0], self.vocabular)  # получаем описания товаров в векторах
        model_goods_class_values = np.array(data_from_db[1])  # набор категорий соответствующих товарам
        model = BernoulliNB(alpha=0.1)  # инициировали модель
        print('Начали учить модель')
        self.model = model.fit(model_goods_vectors, model_goods_class_values)  # обучаем модель
        print('Обучили модель')

        return self

    """
           метод первичной загрузки обучающих данных в БД
    """

    def load_educ_data(path):
        # загружаем данные для обучения в базу
        file = loader()
        print('Загружаем данные из файла')
        file = loader.import_file_data(file, path1)
        print(file)
        # сохраняем обучающую выборку в базу
        loader.load_educ_data_to_bd(file)
        print('Данные для обучения загружены в базу')


"""
    Класс оценки качества модели
    
    a – кол-во правильно определенных  классификатором документов для категории
    с - кол-во неправильно определенных классификатором для категории товаров =m-a
    d - кол-во, которое не нашел, а должен был найти для категории
    l - всего товар категории д.б.б. найдено =a+d
    m - сколько всего записал в категорию товаров
    R - полнота. R= a/(а+c), где "a" – кол-во правильно определенных классификатором документов к классу и "с" кол-во 
    документов, которое классификатор должен, но не определил для класса.
    P - точность P=a/(a+b), где "а" - кол-во правильно определенных и "b" -кол-во неправильно определенных документов 
    к одному классу. Из всего что записал в класс, насколько правильно 
    F-мера - содержит баланс межлу R и P  F=2pr/p+r Для общего используем макроусреднение - составляем по каждому и 
    делим на кол-во
    E - ошибка в разрезе категорий E = (c+d)/(c+d+2a)

"""


class ModelEstimation:
    def __init__(self):
        self.education_time = int()
        self.classification_time = int()
        self.general_time = int()
        self.dict_p = dict()
        self.dict_r = dict()
        self.dict_e = dict()
        self.dict_f = dict()
        self.goods_quantity = int()
        self.correct_estimates = int()
        self.error_estimates = int()
        self.f_general = int()

    """
        метод оценки качества обучения
    """
    def quality_classification(self, goods, goods_classes_by_algorithm, start_time_edu, start_time_clas):
        print('Cчитаем статистику')

        # считаем время
        self.general_time = ModelEstimation.timer(start_time_edu)
        self.education_time = start_time_edu-start_time_clas
        self.classification_time = ModelEstimation.timer(start_time_clas)

        self.goods_quantity = len(goods.goods_description)

        # считаем общее кол-во корректно и ошибок (E) + вычисляем  a, c, d
        self.correct_estimates = int(0)  # общее кол-во правильно категоризированных товаров
        self.error_estimates = int(0)  # общее кол-во ошибочно категоризированных товаров
        list_categories = set(
            goods.goods_target_classes)  # получаем список всех категорий, которые были в тестовой выборке

        dict_a = dict.fromkeys(list_categories, 0)  # сколько истинно правильно нашли для каждой категории -a
        dict_d = dict.fromkeys(list_categories, 0)  # сколько должен был найти, но не нашел для категорий - d

        for i in range(len(goods.goods_target_classes)):
            if goods.goods_target_classes[i] == goods_classes_by_algorithm[i]:
                self.correct_estimates = self.correct_estimates + 1  # обновляем общее число правильно определенных категорий
                dict_a[goods.goods_target_classes[i]] = dict_a.get(goods.goods_target_classes[i]) + 1  # считаем а
            else:
                dict_d[goods.goods_target_classes[i]] = dict_d.get(goods.goods_target_classes[i]) + 1  # считаем d
                self.error_estimates = self.error_estimates + 1  # обновляем общее число ошибочно определенных категорий

        dict_m = {}  # кол-во m (сколько всего было записано) для каждой категрии от алгоритма
        for value in list_categories:
            quantity = np.ndarray.tolist(goods_classes_by_algorithm).count(value)
            dict_m[value] = quantity

        dict_c = {}  # кол-во ошибочно определенных для категории товаров
        for value in list_categories:
            dict_c[value] = dict_m[value] - dict_a[value]  # для каждой категории из m-a

        # считаем P - точность a/(a+c) и R - полнота a/(a+d)
        self.dict_p = dict.fromkeys(list_categories, 0)  # P - точность
        self.dict_r = dict.fromkeys(list_categories, 0)  # R - полнота
        self.dict_e = dict.fromkeys(list_categories, 0)  # E - ошибки

        for value in list_categories:
            if dict_a[value] == 0:
                self.dict_p[value] = 0
                self.dict_r[value] = 0
            else:
                self.dict_p[value] = dict_a[value] / (dict_a[value] + dict_c[value])
                self.dict_r[value] = dict_a[value] / (dict_a[value] + dict_d[value])

            if (dict_c[value] + dict_d[value]) == 0 or (
                    dict_c[value] + dict_d[value] + dict_a[value] + dict_a[value]) == 0:
                self.dict_e[value] == 0
            else:
                self.dict_e[value] = (dict_c[value] + dict_d[value]) / (
                        dict_c[value] + dict_d[value] + dict_a[value] + dict_a[value])

        self.dict_f = {}  # F-мера
        for value in list_categories:
            if self.dict_p[value] == 0 or self.dict_r[value] == 0:
                self.dict_f[value] = 0
            else:
                self.dict_f[value] = (2 * self.dict_p[value] * self.dict_r[value]) / (
                            self.dict_p[value] + self.dict_r[value])
        if sum(self.dict_f.values()) == 0 or len(self.dict_f) == 0:
            self.f_general = 0
        else:
            self.f_general = (sum(self.dict_f.values())) / len(self.dict_f)  # F-мера средняя по всем категориям

        path_to_file = 'file_to_load/output.xlsx'
        loader.export_file_data(path_to_file, goods, goods_classes_by_algorithm, self)

        return '\nОценка классификации:',\
               '\nОбщее время выполнения оценки: {0} сек. Из них:'.format(self.general_time),\
               '\t На обучение:{0} сек.'.format(self.education_time), \
               '\t На классификацию:{0} сек.'.format(self.classification_time), \
               '\nВсего было классифицировано: {0} тов. Из них:'.format(self.goods_quantity), \
               '\t Правильно классифицированы:{0} тов.'.format(self.correct_estimates), \
               '\t Ошибочно классифицированы:{0} тов.'.format(self.error_estimates), \
               '\nКачество классификации по категориям:', \
               '\tТочность по категория:\n\t\t{0}'.format(self.dict_p), \
               '\tПолнота по категориям:\n\t\t{0}'.format(self.dict_r), \
               '\tСбалансированная F1 мара:\n\t\t{0}'.format(self.dict_f), \
               '\nДетальная информация сохранена в файл.'

    """
        метод таймер
    """
    def timer(start):
        time_result = time.time() - start
        return time_result

    """
        метод тестовой прогонки модели
    """
    def test(path1, path2):
        ModelEducation.load_educ_data(path1)  # загружаем данные для обучения в БД
        start_time_edu = time.time()
        # обучаем модель
        model = ModelEducation()
        print('Обучаем модель')
        model = ModelEducation.teach_classifier(model)

        # готовим товары к оценке
        start_time_clas = time.time()
        print('Извлекаем данные из файла для классификации')
        goods = loader()
        goods = loader.import_file_data(goods, path2)
        print('Переводим описание в векторную форму')
        model_goods_vectors = dt.goods_vectors(goods.goods_description, model.vocabular)

        # получаем результаты оценки
        print('Начали классифицировать товары')
        model.result = mdclas.Classify.get_class(model.model, model_goods_vectors)
        print('\nРезультаты классификации товаров:', model.result, '\n')

        # статистика по тестированию
        estimates = ModelEstimation()
        for value in (ModelEstimation.quality_classification(estimates, goods, model.result, start_time_edu, start_time_clas)):
            print(value)




path2 = 'file_to_load/teach_file_sample.xlsx'
path1 = 'file_to_load/teach_file_sample.xlsx'
#path1 = 'file_to_load/data_set_3.xlsx'
#path2 = 'file_to_load/data_set_4.xlsx'


#ModelEstimation.test(path1, path2)
