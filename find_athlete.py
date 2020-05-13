# испортируем модули стандартнй библиотеки datetime
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол пользователя
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения
    birthdate = sa.Column(sa.Text)
    # рост
    height = sa.Column(sa.Float)

class Athelete(Base):
    """
    Описывает структуру таблицы athlete для хранения данных по атлетам
    """
    # задаем название таблицы
    __tablename__ = 'athelete'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)    
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()


def request_data():
    """
    Запрашивает у пользователя id пользователя
    """
    # выводим приветствие
    print("Привет! Ищем атлета похожего на пользователя")
    user_id = input("Введиите id пользователя: ")

    # возвращаем id пользователя
    return user_id

def dateconvert(initial_date):
    """
    Конвертирует дату для дальнейшего сравнения
    """
    splitted_date = initial_date.split("-")
    year = int(splitted_date[0])
    month = int(splitted_date[1])
    day = int(splitted_date[2])

    date = datetime.date(year, month, day)
    return date

def find_bd_athelete(user, session):
    """
    Ищем по ближайшей дате рождения
    """
    athletes_list = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes_list:
        bd = dateconvert(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd
    
    user_bd = dateconvert(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_bd = None

    for id_, bd in athlete_id_bd.items():
        dist = abs(user_bd - bd)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_bd = bd
    
    return athlete_id, athlete_bd

def find_height_athelete(user, session):
    """
    Ищем по ближайшему росту
    """
    athletes_list = session.query(Athelete).filter(Athelete.height != None).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in athletes_list}
    
    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for id_, height in atlhete_id_height.items():
        if height is None:
            continue

        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height
    
    return athlete_id, athlete_height

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """

    session = connect_db()
    user_id = request_data()

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("Пользователь НЕ найден")
    else:
        print("Пользователь найден")

        bd_athlete, bd = find_bd_athelete(user, session)
        height_athlete, height = find_height_athelete(user, session)
        print(f'Ближайший по дате рождения атлет: {bd_athlete}, его дата рождения: {bd}')
        print(f'Ближайший по росту атлет: {height_athlete}, его дата рождения: {height}')

if __name__ == "__main__":
    main()