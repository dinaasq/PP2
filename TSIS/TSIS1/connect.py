# connect.py
import psycopg2
from config import get_db_params # Импортируем функцию из первого файла

def get_connection():
    
    try:
        params = get_db_params()
        # Распаковываем словарь через **
        conn = psycopg2.connect(**params)
        return conn
    except Exception as error:
        print(f"Ошибка при подключении: {error}")
        return None