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
    goods_target_classes = sa.Column(sa.TEXT)
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


def get_category_kupivip(category_id):
    """
        #Получаем категорию kupivip из базы
    """
    session = connect_db()
    category_from_db = session.query(Classifier_kupivip).filter(Classifier_kupivip.category_id == category_id).first()
    return category_from_db


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
        uid=data['uid'],
        category_path=data['path'],
        category_id=data['category'],
        veryfied='0'
    )
    session.add(new_comfirmed_category)
    session.commit()

# data_cat={'category_id':'23', 'path_category':'Для дома Домашний текстиль Одеяла'};

# add_category_kupivip(data_cat)
# tr=(get_category_kupivip(23))
# print (tr.category_path)
