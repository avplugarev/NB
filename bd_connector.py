import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

DB_PATH = 'sqlite:///app.sqlite3'
Base = declarative_base()


class Users(Base):
    """
         Описываем структуру таблицы user для хранения авторизационных данных пользователя
    """
    __tablename__ = 'users'
    user_id = sa.Column(sa.TEXT, primary_key=True)
    user_login = sa.Column(sa.TEXT)
    user_password = sa.Column(sa.TEXT)
    user_api_key = sa.Column(sa.TEXT)


class Classifier_kupivip(Base):
    """
        #Описываем структуру таблицы classifier_kpvp для хранения классификатора купивип
    """
    __tablename__ = 'classifier_kpvp'
    category_id = sa.Column(sa.INTEGER, primary_key=True)
    category_path = sa.Column(sa.TEXT)


class Classified_category(Base):
    """
        #Описываем структуру таблицы classified_category для хранения классифицированных категорий купивип
    """
    __tablename__ = 'classified_category'
    uid = sa.Column(sa.INTEGER, primary_key=True)
    category_path = sa.Column(sa.TEXT)
    category_id = sa.Column(sa.INTEGER)
    veryfied = sa.Column(sa.INTEGER)


class Prepared_data(Base):
    """
        #Описываем структуру таблицы pre_data для хранения предварительно обработанных для обучения модели товаров
    """
    __tablename__ = 'pre_data'
    uid = sa.Column(sa.INTEGER, primary_key=True)
    goods_description = sa.Column(sa.TEXT)
    goods_target_classes = sa.Column(sa.INTEGER)
    goods_supplier_classes = sa.Column(sa.TEXT)


def connect_db():
    """
        #Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def add_category_kupivip(data):
    """
        #Записываем категории kupivip в базу
    """
    session = connect_db()
    new_category = Classifier_kupivip(
        category_id=data['category_id'],
        category_path=data['path_category']
    )
    session.add(new_category)
    session.commit()


def get_category_kupivip_by_id(category_id):
    """
        #Получаем путь категории kupivip из базы по ее  id
    """
    session = connect_db()
    category_from_db = session.query(Classifier_kupivip).filter(Classifier_kupivip.category_id == int(category_id)).first()
    return category_from_db.category_path


def read_confirmed_category():
    """
            Метод чтения подтвержденных категорий
    """
    session = connect_db()
    categories_from_db = session.query(Classified_category).all()
    data_for_check = list()
    for category in categories_from_db:
        category_db = dict()
        category_db['category_id'] = category.category_id
        category_db['path'] = category.category_path
        category_db['status'] = category.veryfied
        data_for_check.append(category_db)

    return data_for_check, len(categories_from_db)


def add_category_to_dict_categories(data):
    """
        #Записываем подтвержденные категории в справочник категорий - Classified_category
    """
    session = connect_db()
    new_comfirmed_category = Classified_category(
        uid=data['uid_path'],
        category_path=data['path'],
        category_id=data['category'],
        veryfied='0'
    )
    session.add(new_comfirmed_category)
    session.commit()

def get_category_id_from_confirmed_categ(category_path):
    """
           #Получаем id подтвержденной категории из справочника подтвержденных категорий (таб Classified_category  bd
    """
    session = connect_db()
    category_from_db = session.query(Classified_category).filter(
        Classified_category.category_path == category_path).first()
    return category_from_db.category_id

def read_prepared_data():
    """
            Метод чтения подготовленных для обучения классификатора данных
    """
    session = connect_db()
    data_from_db = session.query(Prepared_data).all()
    goods_description = list()
    goods_categories = []
    for good in data_from_db:
        goods_description.append(good.goods_description)
        goods_categories.append(good.goods_target_classes)
    return goods_description, goods_categories, len(goods_categories)


def add_good_to_prepared_data(data):
    """
        Метод добавления проверенных товаров в обучающую выборку
    """
    session = connect_db()
    new_good_to_education = Prepared_data(
        uid=data['uid_educ'],
        goods_description=data['description'],
        goods_target_classes=data['category'],
        goods_supplier_classes=data['path']
    )
    session.add(new_good_to_education)
    session.commit()

def user_login_check(login, password):
    """
        Метод проверки корректности введенного логина и пароля
    """
    session = connect_db()
    user_verification_data = session.query(Users).filter(Users.user_login == login).first()
    if user_verification_data != None:
        if user_verification_data.user_login == login:
            if user_verification_data.user_password == password:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def edu_data_delete():
    """
        Метод удаления обучающих данных из базы
    """
    session = connect_db()
    session.query(Prepared_data).delete()
    session.commit()

    return 'Данные удалены из базы обучения'

def classifier_kupivip_delete():
    """
        Метод удаления классификатора купивип
    """
    session = connect_db()
    session.query(Classifier_kupivip).delete()
    session.commit()

    return 'Данные удалены из базы классификатора kupivip'

def classified_category_delete():
    """
        Метод удаления классификатора купивип
    """
    session = connect_db()
    session.query(Classified_category).delete()
    session.commit()

    return 'Данные удалены из справочника подтвержденных категорий'

# data_cat={'category_id':'23', 'path_category':'Для дома Домашний текстиль Одеяла'};

# add_category_kupivip(data_cat)
# tr=(get_category_kupivip(23))
# print (tr.category_path)

#print(edu_data_delete())
#print(classifier_kupivip_delete())
#print(classified_category_delete())


