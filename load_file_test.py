import openpyxl  # импортируем модуль по работе с электронными таблицами

class FileLoader:
    def load_file(path_to_file, param):
        file = openpyxl.load_workbook(path_to_file)  # загружам файл в объект для дальнейшей работе с ним
        working_sheet = file.active  # получаю объект лист ддя работы
        goods_description = []  # пустой список под описагния товаров
        goods_class_values = []  # пустой список под категории для товаров
        good_rows=[0,1,2,3,4,5,9,10,11,18,25,28,29,34,35,36,37,41,49,52, 54]
        good_rows2=[0,1,2,3,4,5,9,10,11,18,25,28,29,34,35,36,37,41,49,52, 54]
        for row in working_sheet.values:  # идем по файлу и выгружаем описания и категории товаро в соответствтующие списки
            good = str()
            counter=0
            if row[0] == "Class_ID" or row[0] == "Уровень 1":
                continue;
            if param == 1:
                goods_class_values.append(row[0])
                for value in row[1:]:
                    if value != None:
                        if counter in good_rows:
                            if counter==11:
                                if value ==0:
                                    good = good + ' ' + str('унисекс')
                                elif value ==1:
                                    good = good + ' ' + str('мужчинам')
                                else:
                                    good = good + ' ' + str('женщинам')
                            elif counter ==18:
                                if value ==0:
                                    good = good + ' ' + str('медицина')
                                elif value ==10:
                                    good = good + ' ' + str('детский')
                                else:
                                    good = good + ' ' + str('любой')
                            elif counter ==52:
                                if value ==1:
                                    good = good + ' ' + str('текстиль')
                                elif value ==2:
                                    good = good + ' ' + str('трикотаж')
                                else:
                                    good = good + ' ' + str('другое')
                            else:
                                good = good + ' ' + str(value)
                    counter=counter+1
                goods_description.append(good)
            elif param == 2:
                for value in row:
                    if value != None:
                        if counter in good_rows2:
                            if counter == 11:
                                if value == 0:
                                    good = good + ' ' + str('унисекс')
                                elif value == 1:
                                    good = good + ' ' + str('мужчинам')
                                else:
                                    good = good + ' ' + str('женщинам')
                            elif counter == 18:
                                if value == 0:
                                    good = good + ' ' + str('медицина')
                                elif value == 10:
                                    good = good + ' ' + str('детский')
                                else:
                                    good = good + ' ' + str('любой')
                            elif counter == 52:
                                if value == 1:
                                    good = good + ' ' + str('текстиль')
                                elif value == 2:
                                    good = good + ' ' + str('трикотаж')
                                else:
                                    good = good + ' ' + str('другое')
                            else:
                                good = good + ' ' + str(value)
                    counter = counter + 1
                goods_description.append(good)
        file.close()
        if param == 1:
            return goods_description, goods_class_values
        else:
            return goods_description


path='teach_file_sample.xlsx'
path2='teach_test_sample.xlsx'

#print(FileLoader.load_file(path2,2))