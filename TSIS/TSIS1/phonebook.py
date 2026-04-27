import json
import csv
from connect import get_connection # Импортируем функцию подключения

def interactive_nav(page_size=5):
    offset = 0
    conn = get_connection() # Получаем соединение
    if not conn:
        return

    try:
        while True:
            cur = conn.cursor()
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (page_size, offset))
            rows = cur.fetchall()
            
            print(f"\n--- Страница (смещение {offset}) ---")
            if not rows:
                print("Данных больше нет.")
            for r in rows:
                print(f"ID: {r[0]} | Имя: {r[1]} {r[2]} | Email: {r[3]}")
            
            cmd = input("\n[n]ext, [p]rev, [q]uit: ").lower()
            if cmd == 'n': 
                if rows: offset += page_size
            elif cmd == 'p': 
                offset = max(0, offset - page_size)
            elif cmd == 'q': 
                break
            cur.close()
    finally:
        conn.close()

def export_to_json(filename="contacts.json"):
    conn = get_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute("SELECT first_name, last_name, email FROM contacts")
        rows = cur.fetchall()
        data = [{"first_name": r[0], "last_name": r[1], "email": r[2]} for r in rows]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ Данные сохранены в {filename}")
    finally:
        conn.close()

def import_from_csv(filename="contacts.csv"):
    conn = get_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO contacts (first_name, last_name, email) VALUES (%s, %s, %s)",
                    (row['first_name'], row['last_name'], row['email'])
                )
        conn.commit()
        print("✅ Данные из CSV загружены в базу!")
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
    finally:
        conn.close()


# 1. Функция для добавления телефона через процедуру
def add_new_phone():
    name = input("Введите имя или фамилию контакта: ")
    phone = input("Введите номер телефона: ")
    p_type = input("Тип (home, work, mobile): ")
    
    conn = get_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        # В SQL мы писали: CALL add_phone(name, phone, type)
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, p_type))
        conn.commit()
        print(f"✅ Номер {phone} успешно добавлен для {name}!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        conn.close()

# 2. Функция для смены группы через процедуру
def change_contact_group():
    name = input("Введите имя контакта: ")
    group_name = input("Введите название новой группы: ")
    
    conn = get_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        # В SQL мы писали: CALL move_to_group(name, group)
        cur.execute("CALL move_to_group(%s, %s)", (name, group_name))
        conn.commit()
        print(f"✅ Контакт {name} теперь в группе '{group_name}'!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        conn.close()
        
def main_menu():
    while True:
        print("\n=== PHONEBOOK MENU ===")
        print("1. Показать контакты (Пагинация)")
        print("2. Импорт из CSV")
        print("3. Экспорт в JSON")
        print("4. Добавить телефон (Procedure)")  # НОВОЕ
        print("5. Сменить группу (Procedure)")    # НОВОЕ
        print("0. Выход")
        
        choice = input("Выбор: ")
        if choice == '1':
            interactive_nav()
        elif choice == '2':
            import_from_csv()
        elif choice == '3':
            export_to_json()
        elif choice == '4':
            add_new_phone()
        elif choice == '5':
            change_contact_group()
        elif choice == '0':
            break

if __name__ == "__main__":
    main_menu()