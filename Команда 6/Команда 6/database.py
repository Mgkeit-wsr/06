from mysql.connector import pooling, Error
from config import *
import datetime as dt


def insert_eventMember(event_id: int, user_id: str) -> None:
    """
    Получает айди юзер-ивента и айди пользователя, который сказал "Пойду" на данный
    юзер-ивент, и вставляет пару в таблицу eventMember

    :param event_id: уникальный id юзер-ивента
    :param user_id: телеграм-username пользователя
    :return: None
    """
    connection_pool = pooling.MySQLConnectionPool(host=HOST,
                                                  database=DB_NAME,
                                                  user=USER,
                                                  password=PASSWORD)
    with connection_pool.get_connection() as cnt:
        query = "INSERT INTO eventMember (user_id, event_id) VALUES (%s, %s)"
        with cnt.cursor() as cur:
            cur.execute(query, (user_id, event_id))
            cnt.commit()
        connection_pool.get_connection().close()


def find_eventMember(event_id: int = None, user_id: str = None) -> tuple:
    """
    ЕСЛИ УКАЗАН ТОЛЬКО user_id: возвращает список всех ивентов данного пользователя

    ЕСЛИ УКАЗАН ТОЛЬКО event_id: возвращает список всех юзеров, кто подписался на данный ивент

    ЕСЛИ УКАЗАНЫ ОБА: находит одну конкретную пару "пользователь - юзер-ивент"
    """
    query = "SELECT * FROM eventMember WHERE "
    values = ()
    connection_pool = pooling.MySQLConnectionPool(host=HOST,
                                                  database=DB_NAME,
                                                  user=USER,
                                                  password=PASSWORD)
    with connection_pool.get_connection() as cnt:
        if event_id is not None and user_id is None:
            query += "event_id=%s"
            values = (event_id,)
        elif user_id is not None and event_id is None:
            query += "user_id=%s"
            values = (user_id,)
        if all([event_id, user_id]) is not None:
            query += "user_id=%s AND event_id=%s"
            values = (user_id, event_id)
        with cnt.cursor() as cur:
            cur.execute(query, values)
            return cur.fetchall()


def remove_eventMember(user_id: str = None, event_id: int = None):
    connection_pool = pooling.MySQLConnectionPool(host=HOST,
                                                  database=DB_NAME,
                                                  user=USER,
                                                  password=PASSWORD)
    with connection_pool.get_connection() as cnt:
        requested_rows = find_eventMember(event_id=event_id, user_id=user_id)
        for item in requested_rows:
            query = "DELETE FROM eventMember WHERE id=%s"
            values = (item[0],)
            with cnt.cursor() as cur:
                cur.execute(query, values)
                cnt.commit()


def insert_event(author_id: str,
                 name: str,
                 description: str,
                 date_time: dt.datetime,
                 latitude: float,
                 longitude: float,
                 category: str) -> None:
    """
    Вставляет в таблицу event юзер-ивент в момент создания пользователем после передачи всех аргументов

    :param author_id: телеграм-username пользователя
    :param name: заголовок
    :param description: описание
    :param date_time: dt.datetime объект. Подсказка: argument_name = dt.datetime(год, месяц, день, час, минута)
    :param latitude: широта
    :param longitude: долгота
    :param category: категория
    :return: None
    """
    connection_pool = pooling.MySQLConnectionPool(host=HOST,
                                                  database=DB_NAME,
                                                  user=USER,
                                                  password=PASSWORD)
    with connection_pool.get_connection() as cnt:
        with cnt.cursor() as cur:
            values = (
                author_id, name, description, date_time, latitude, longitude,
                category)
            insert_query = """INSERT INTO event (author_id, name, description, date, latitude, longitude, category) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(insert_query, values)
            cnt.commit()


def read_filtered_events(author_id: str,
                         minmax_date: tuple = None,
                         minmax_latitude: tuple = None,
                         minmax_longitude: tuple = None,
                         category: str = None,
                         id: int = None) -> list:
    """
    ЕСЛИ УКАЗАН ТОЛЬКО author_id: вернет все записи из event, автор которых - данный пользователь

    ЕСЛИ УКАЗАН ЛЮБОЙ ИЗ ДРУГИХ ЧЕТЫРЕХ: вернет все записи из event, автор которых - НЕ данный пользователь, и которые попадают под все указанные фильтры

    :param author_id:
    :param minmax_date: кортеж из текущей даты и текущей даты ПЛЮС выбраный для фильтра параметер (0 дней, 1 неделя, 1 месяц)
    :param minmax_latitude: кортеж из минимальной широты и максимальной широты (текущая широта пользователя +- выбранное для фильтра число км)
    :param minmax_longitude: кортеж из минимальной долготы и максимальной долготы (текущая долготы пользователя +- выбранное для фильтра число км)
    :param category: категория, выбранная для фильтрации
    :return:
    """
    connection_pool = pooling.MySQLConnectionPool(host=HOST,
                                                  database=DB_NAME,
                                                  user=USER,
                                                  password=PASSWORD)
    with connection_pool.get_connection() as cnt:
        read_query = "SELECT * FROM event WHERE NOT "
        values = ()

        passed_kwargs1 = {"author_id=%s": author_id, "category=%s": category, "id=%s": id}
        read_query += " AND ".join([key for key, value in passed_kwargs1.items() if value is not None])
        values += tuple(item for item in passed_kwargs1.values() if item is not None)

        if minmax_latitude is not None:
            read_query += " AND latitude BETWEEN %s AND %s AND longitude BETWEEN %s AND %s"
            values += (minmax_latitude, minmax_longitude)

        if minmax_date is not None:
            read_query += " AND date BETWEEN %s AND %s"
            values += (minmax_date[0], minmax_date[1])

        if len(values) == 1:
            read_query = read_query.replace("NOT ", "")

        print("ATTEMPTED QUERY: ", read_query)
        print(values)
        with cnt.cursor() as cur:
            cur.execute(read_query, values)
            found_rows = [item for item in cur.fetchall()]
            return found_rows


def delete_event(event_id: int):
    connection_pool = pooling.MySQLConnectionPool(host=HOST,
                                                  database=DB_NAME,
                                                  user=USER,
                                                  password=PASSWORD)
    with connection_pool.get_connection() as cnt:
        delete_query = "DELETE FROM event WHERE id=%s"
        with cnt.cursor() as cur:
            cur.execute(delete_query, (event_id, author_id))
            cnt.commit()


def read_table(table_name: str):
    connection_pool = pooling.MySQLConnectionPool(host=HOST,
                                                  database=DB_NAME,
                                                  user=USER,
                                                  password=PASSWORD)
    cnt = connection_pool.get_connection()
    with cnt.cursor() as cur:
        read_query = f"SELECT * FROM {table_name}"
        cur.execute(read_query)
        rows = [item for item in cur.fetchall()]
        print(rows)
        # cur.execute("DELETE FROM event")



