import openpyxl  # импортируем модуль по работе с электронными таблицами
import text_normalisation
import bd_connector

#класс загрузки данных из файла для обучения и для тестирования обучения
class FileLoader:
    def __init__(self):
        pass
    #базовая функция загрузки описаний товаров из файла для обучения и тестирования обучения
    def load_file(path_to_file):
        #path_to_file = путь к загружаемому файлу для обучения или тестирования


        file = openpyxl.load_workbook(path_to_file)  # загружам файл в объект для дальнейшей работе с ним
        working_sheet = file.active  # получаю объект лист ддя работы
        goods_description = []  # пустой список под описагния товаров
        goods_target_classes = []  # пустой список sпод категории для товаров
        goods_supplier_classes = []  # пустой список ппод классификатор поставщика

        # чистим выгрузку от лишних ячеек
        working_sheet = FileLoader.clear_file_data(working_sheet)

        for row in working_sheet.values:
            # добавляем категорию товара в коллекцию с таргетинговыми значениями
            goods_target_classes.append(row[0])

            # производим работы с описанием товара и добавляем его в обучающую или тестовую выгрузку
            good = str()
            goods_supplier_class = str()
            n = 0
            for value in row[1:]:
                #получаем путь к категории классификатора поставщика для этого товара
                if n < 6:
                    goods_supplier_class = FileLoader.sup_class_replacement(goods_supplier_class, value)
                n = n + 1
                #получаем полное описание товара
                good = FileLoader.text_transformation(value, row, good)
            #добавляем описание товара в коллекцию описания товаров
            goods_description.append(good)
            #добавляем описание пути к категории в коллекции пставщика
            goods_supplier_classes.append(goods_supplier_class)

            #print('товар - {} добавлен в выходные списки. \r'.format(len(goods_description)), end="")

        file.close()
        return goods_description, goods_target_classes, goods_supplier_classes

    #функция обработки слов в описании товара:
    def text_transformation(value, row, good):
        #описания справочников:
        gender = ['любой_пол', 'мужчинам', 'женщинам']
        vat = {0: 'медицина', 10: 'детский', 20: 'товар_с_обычным_налогом'}
        chip = {'LOT': 'без_чипа', 'DMX': 'обувь', 'datamatrix': 'обувь', 'MEX': 'мех', 'обычный': 'без_чипа'}
        textile_type = ['текстиль', 'трикотаж', 'другое']

        #удаляем пустые ячейки
        if value == None:
            return good
        #заменяем числовые значения в описание товара - значениями из справочника
        elif value == row[9]:
            return good + ' ' + gender[value]
        elif value == row[11]:
            return good + ' ' + vat[value]
        elif value == row[13]:
            return good + ' ' + chip[value]
        elif value == row[14]:
            return good + ' ' + textile_type[value - 1]
        else:
        #если никаких изменений не надо - просто добавляем слово в описание товара
            return good + ' ' + value
            #приводим значения слов к нормальной форме - пока отключенено
            # return text_transformation.filtr_by_word_form(value,good)

    #функция замены пустых значений для пути классификатора поставщика на None
    def sup_class_replacement(goods_supplier_class, value):
        if value != None:
            goods_supplier_class = goods_supplier_class + ' ' + str(value)
        else:
            goods_supplier_class = goods_supplier_class + ' ' + str('None')
        return goods_supplier_class

    #функция удаляения пустых и не нужных нам столбцов имеющих шумовой эффект
    def clear_file_data(working_sheet):
        good_rows = ['Class_ID', 'Уровень 1', 'Уровень 2', 'Уровень 3', 'Уровень 4', 'Уровень 5', 'Уровень 6',
                     'Наименование (<=250)', 'Техническое описание', 'Пол', 'Размер производителя  (<=10)', 'НДС',
                     'Возраст+', 'Тип чипа', 'Тип ткани', 'Тип кроя/джинсы']
        for row in working_sheet:
            for cell in row:
                if cell.value not in good_rows:
                    working_sheet.delete_cols(cell.column)  #удаляем столбцы, если их заголовки нам не нужны
            break
        working_sheet.delete_rows(0)
        return working_sheet

    def load_classifier_kupivip(path):
        file = openpyxl.load_workbook(path_to_classifier)  # загружам файл в объект для дальнейшей работе с ним
        working_sheet = file.active  # получаю объект лист ддя работы

        # dict_category={}

        for row in working_sheet.values:
            category_id = {}
            data = {}
            category_path = str()
            for value in row[:1]:
                category_id = value
            for value in row[2:7]:
                if value == None:
                    category_path = category_path + ' ' + str('None')
                else:
                    category_path = category_path + ' ' + value
            # dict_category[category_id]=category_path
            data['category_id'] = category_id
            data['path_category'] = category_path
            bd_connector.add_category_kupivip(data)
        file.close()
        return 'данные по категориям успешно загружены'




path = 'file_to_load/teach_file_sample.xlsx'
path2 = 'teach_test_sample.xlsx'
#print(FileLoader.load_file(path))
path_to_classifier = 'file_to_load/class_ready.xlsx'

#print(FileLoader.load_classifier_kupivip(path_to_classifier))









