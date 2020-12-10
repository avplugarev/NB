import openpyxl  # импортируем модуль по работе с электронными таблицами
"""
"""

class FileLoader:

    def load_file_new(path_to_file, param):
        gender = ['унисекс', 'мужчинам', 'женщинам']
        vat = {0: 'медицина', 10: 'детский', 20: 'обычный'}
        textile_type = ['текстиль', 'трикотаж', 'другое']
        good_rows = ['Class_ID', 'Уровень 1', 'Уровень 2', 'Уровень 3', 'Уровень 4', 'Уровень 5', 'Уровень 6',
                     'Наименование (<=250)', 'Техническое описание', 'Пол', 'Размер производителя  (<=10)', 'НДС',
                     'Возраст+', 'Тип чипа', 'Тип ткани', 'Тип кроя/джинсы']

        file = openpyxl.load_workbook(path_to_file)  # загружам файл в объект для дальнейшей работе с ним
        working_sheet = file.active  # получаю объект лист ддя работы
        goods_description = []  # пустой список под описагния товаров
        goods_class_values = []  # пустой список под категории для товаров

        for row in working_sheet:  # идем по файлу и выгружаем описания и категории товаро в соответствтующие списки
            for cell in row:
                if cell.value not in good_rows:
                    working_sheet.delete_cols(cell.column)
            break
        working_sheet.delete_rows(0)
        for row in working_sheet.values:
            good = str()
            if param == 1:
                goods_class_values.append(row[0])
                start_goods_desc = 1
            else:
                start_goods_desc = 0
            for value in row[start_goods_desc:]:
                if value != None:
                    if value == row[9-param+1]:
                        good = good + ' ' + gender[value]
                    elif value == row[11-param+1]:
                        good = good + ' ' + vat[value]
                    elif value == row[14-param+1]:
                        good = good + ' ' + textile_type[value - 1]
                    else:
                        good = good + ' ' + str(value)
            goods_description.append(good)
        file.close()
        if param == 1:
            return goods_description, goods_class_values
        else:
            return goods_description


path = 'teach_file_sample.xlsx'
path2 = 'teach_test_sample.xlsx'

# print(FileLoader.load_file(path2,2))
#print(FileLoader.load_file_new(path, 1))
