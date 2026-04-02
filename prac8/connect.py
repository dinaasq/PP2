import psycopg2
from config import host, user, password, db_name

def get_connection():
    try:
        # Пытаемся подключиться к базе данных
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        print("[INFO] Соединение с PostgreSQL установлено")
        return conn
    except Exception as _ex:
        print("[INFO] Ошибка при подключении к PostgreSQL", _ex)
        return None

if __name__ == "__main__":
    # Тестовый запуск: просто проверяем, проходит ли коннект
    connection = get_connection()
    if connection:
        connection.close()
        print("[INFO] Соединение закрыто")