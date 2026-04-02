import psycopg2
from config import host, user, password, db_name # Импортируй свои данные

def manage_phonebook():
    try:
        # 1. Подключаемся к базе
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        conn.autocommit = True # Чтобы изменения сразу сохранялись
        cur = conn.cursor()

        # 2. Вызываем ПРОЦЕДУРУ (upsert_contact)
        print("Добавляем контакт...")
        cur.execute("CALL upsert_contact(%s, %s)", ("Miras", "87770001122"))

        # 3. Вызываем ФУНКЦИЮ (get_contacts_by_pattern)
        print("Ищем контакты по части имени 'Mir'...")
        cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", ("Mir",))
        results = cur.fetchall()
        for row in results:
            print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")

        # 4. Вызываем ПРОЦЕДУРУ массовой вставки
        print("Массовая вставка...")
        names = ["Amina", "Arman"]
        phones = ["8701555", "123"] # "123" не пройдет валидацию в нашей процедуре
        cur.execute("CALL bulk_insert_contacts(%s, %s)", (names, phones))

        # 5. Вызываем ФУНКЦИЮ пагинации (Первая страница, 2 записи)
        print("Пагинация (первые 2 записи):")
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (2, 0))
        for row in cur.fetchall():
            print(row)

        cur.close()
        conn.close()

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)

if __name__ == "__main__":
    manage_phonebook()