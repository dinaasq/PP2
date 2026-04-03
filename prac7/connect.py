# connect.py
import psycopg2
from config import params

def connect():
    """ Устанавливает соединение с сервером PostgreSQL """
    conn = None
    try:
        # Читаем параметры подключения
        print('Подключение к базе данных PostgreSQL...')
        conn = psycopg2.connect(**params)
        
        # Создаем курсор
        cur = conn.cursor()
        
        # Выполняем запрос для проверки версии базы
        print('Версия PostgreSQL:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
       
        # Закрываем курсор
        cur.close()
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка: {error}")
        return None

if __name__ == '__main__':
    # Если запустить этот файл напрямую, он просто проверит связь
    connection = connect()
    if connection:
        connection.close()
        print('Соединение закрыто.')