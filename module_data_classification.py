import bd_connector as bd

"""
    Класс классификации товаров и подтверждения категории
"""
class Classify:
    """
        метод классификации товара на основе модели
    """
    def get_class(model, good_without_class_vector):
        model = model.predict(good_without_class_vector)
        return model


    """
        метод выбора варианта классификации 
    """
    def need_NB_class(path):

        check = bd.get_category_id_from_confirmed_categ(path)
        if check == None:
            return 'yes'
        else:
            return check

    """
        метод обновления списка подтвержденных категорий и множества документов обучения  
    """
    def confirm_class(self):
        pass
