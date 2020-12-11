import openpyxl  # импортируем модуль по работе с электронными таблицами
import time
import text_transformation


"""
"""


class FileLoader:

    def load_file_new(path_to_file, param):
        start_time = time.time()

        file = openpyxl.load_workbook(path_to_file)  # загружам файл в объект для дальнейшей работе с ним
        working_sheet = file.active  # получаю объект лист ддя работы
        goods_description = []  # пустой список под описагния товаров
        goods_class_values = []  # пустой список под категории для товаров
        supplier_load_classifir_for_good = []  # пустой список ппод классификатор поставщика

        # чистим выгрузку от лишних ячеек
        working_sheet = FileLoader.clear_docs_data(working_sheet)

        for row in working_sheet.values:
            # заполняем таргетинговые значения для обучающей и тестовой выгрузок в зависимости от параметров
            if param == 1:
                goods_class_values.append(row[0])
                start_goods_desc = 1
            else:
                start_goods_desc = 0

            # производим работы с описанием товара и добавляем его в обучающую или тестовую выгрузку
            good = str()
            goods_supplier_class = str()
            n=0
            for value in row[start_goods_desc:]:
                if n < 6:
                    goods_supplier_class = FileLoader.supplier_good_classifier_value(goods_supplier_class, value)
                n=n+1
                good = FileLoader.value_enriching(value, row, param, good)
            goods_description.append(good)

            # получаем классификатор поставкщика для товара
            supplier_load_classifir_for_good.append(goods_supplier_class)

        return FileLoader.result_output(param, goods_description, goods_class_values, start_time, file,
                                        supplier_load_classifir_for_good)

    def value_enriching(value, row, param, good):
        gender = ['унисекс', 'мужчинам', 'женщинам']
        vat = {0: 'медицина', 10: 'детский', 20: 'обычный'}
        textile_type = ['текстиль', 'трикотаж', 'другое']

        if value == None:
            return good
        elif value == row[9 - param + 1]:
            return good + ' ' + gender[value]
        elif value == row[11 - param + 1]:
            return good + ' ' + vat[value]
        elif value == row[14 - param + 1]:
            return good + ' ' + textile_type[value - 1]
        #при включенном морфе надо внести в исключение лот и размер
        else:
            return good+' '+value
            #return FileLoader.filtr_by_word_form(value,good)
            #return text_transformation.filtr_by_word_form(value,good)
    def supplier_good_classifier_value(goods_supplier_class, value):
        if value != None:
            goods_supplier_class = goods_supplier_class + ' ' + str(value)
        else:
            goods_supplier_class = goods_supplier_class + ' ' + str('None')
        return goods_supplier_class

    def timer(start, param):
        time_load_for = "Загрузка {0} выборки заняла {1} сек."
        time_result = time.time() - start
        if param == "teach":
            text = str('обучающей')
        else:
            text = str('тестовой')
        time_exect = time_load_for.format(text, time_result)
        return time_exect

    def clear_docs_data(working_sheet):
        good_rows = ['Class_ID', 'Уровень 1', 'Уровень 2', 'Уровень 3', 'Уровень 4', 'Уровень 5', 'Уровень 6',
                     'Наименование (<=250)', 'Техническое описание', 'Пол', 'Размер производителя  (<=10)', 'НДС',
                     'Возраст+', 'Тип чипа', 'Тип ткани', 'Тип кроя/джинсы']
        for row in working_sheet:
            for cell in row:
                if cell.value not in good_rows:
                    working_sheet.delete_cols(cell.column)
            break
        working_sheet.delete_rows(0)
        return working_sheet

    def result_output(param, goods_description, goods_class_values, start_time, file, supplier_load_classifir_for_good):
        file.close()
        time_exect = FileLoader.timer(start_time, param)
        if param == 1:
            return goods_description, goods_class_values, time_exect, supplier_load_classifir_for_good
        else:
            return goods_description, time_exect, supplier_load_classifir_for_good



path = 'teach_file_sample.xlsx'
path2 = 'teach_test_sample.xlsx'

# print(FileLoader.load_file(path2,2))
print(FileLoader.load_file_new(path, 1))
