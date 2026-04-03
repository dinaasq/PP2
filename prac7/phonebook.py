import psycopg2
import csv
import sys
from config import params

def get_connection():
    """Создает подключение к PostgreSQL используя параметры из config.py"""
    try:
        return psycopg2.connect(**params)
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        sys.exit()

def import_from_csv(file_path):
    """3.2: Импорт данных из CSV файла"""
    query = "INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING;"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    # Если в CSV есть заголовок (Name, Phone), раскомментируй следующую строку:
                    # next(reader) 
                    
                    data = [row for row in reader if len(row) == 2]
                    cur.executemany(query, data)
                conn.commit()
        print(">>> Данные из CSV успешно обработаны.")
    except FileNotFoundError:
        print(f">>> Ошибка: Файл {file_path} не найден.")
    except Exception as e:
        print(f">>> Ошибка при импорте: {e}")

def add_contact(name, phone):
    """3.2: Добавление контакта через консоль"""
    query = "INSERT INTO phonebook (name, phone) VALUES (%s, %s);"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name, phone))
                conn.commit()
        print(f">>> Контакт '{name}' добавлен.")
    except psycopg2.IntegrityError:
        print(">>> Ошибка: Этот номер телефона уже существует в базе.")

def update_contact(target_name, new_phone):
    """3.2: Обновление номера телефона по имени"""
    query = "UPDATE phonebook SET phone = %s WHERE name = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (new_phone, target_name))
            if cur.rowcount > 0:
                conn.commit()
                print(f">>> Номер для '{target_name}' обновлен.")
            else:
                print(">>> Контакт с таким именем не найден.")

def search_contacts(search_term):
    """3.2: Поиск контактов с фильтрацией (по имени или части номера)"""
    query = """
        SELECT name, phone FROM phonebook 
        WHERE name ILIKE %s OR phone LIKE %s;
    """
    pattern = f"%{search_term}%"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (pattern, pattern))
            results = cur.fetchall()
            
            if results:
                print("\n--- Результаты поиска ---")
                for name, phone in results:
                    print(f"Имя: {name:15} | Тел: {phone}")
            else:
                print(">>> Ничего не найдено.")

def delete_contact(identifier):
    """3.2: Удаление по имени или номеру телефона"""
    query = "DELETE FROM phonebook WHERE name = %s OR phone = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (identifier, identifier))
            if cur.rowcount > 0:
                conn.commit()
                print(f">>> Контакт '{identifier}' удален.")
            else:
                print(">>> Контакт не найден.")

def show_menu():
    print("\n--- PhoneBook Console ---")
    print("1. Импорт из CSV (contacts.csv)")
    print("2. Добавить новый контакт")
    print("3. Изменить номер (по имени)")
    print("4. Поиск (по имени или номеру)")
    print("5. Удалить контакт")
    print("0. Выход")

def main():
    while True:
        show_menu()
        choice = input("\nВыберите действие: ")

        if choice == '1':
            import_from_csv('contacts.csv')
        
        elif choice == '2':
            name = input("Введите имя: ")
            phone = input("Введите номер: ")
            add_contact(name, phone)
            
        elif choice == '3':
            name = input("Введите имя контакта: ")
            new_phone = input("Введите новый номер: ")
            update_contact(name, new_phone)
            
        elif choice == '4':
            term = input("Введите имя или начало номера для поиска: ")
            search_contacts(term)
            
        elif choice == '5':
            target = input("Введите имя или номер для удаления: ")
            delete_contact(target)
            
        elif choice == '0':
            print("Завершение работы...")
            break
        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()