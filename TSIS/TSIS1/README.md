# 📒 TSIS 1: PhoneBook — Extended Contact Management

## 📌 Description

Advanced PhoneBook application using Python and PostgreSQL.  
Supports relational database design, multiple phone numbers per contact, groups, advanced search, and import/export features.

---

## ⚙️ Technologies

- Python 3
- PostgreSQL
- psycopg2
- JSON / CSV
- PL/pgSQL

---

## 🧱 Database Structure

### Groups
- id
- name

### Contacts
- id
- name
- email
- birthday
- group_id

### Phones
- id
- contact_id
- phone
- type (home / work / mobile)

---

## 🔧 Features

- Add / update / delete contacts
- Multiple phone numbers per contact
- Group system (Family, Work, Friend, Other)
- Search by name, email, or phone
- Filter by group
- Sort by name, birthday
- Pagination (next / prev)
- JSON export / import
- Extended CSV import

---

## 🧠 Stored Procedures

- `add_phone(contact_name, phone, type)`  
  → Adds phone to existing contact

- `move_to_group(contact_name, group_name)`  
  → Moves contact to group (creates group if not exists)

- `search_contacts(query)`  
  → Searches in name, email, and all phones

---

## 📁 Project Structure
TSIS1/
├── phonebook.py
├── connect.py
├── config.py
├── schema.sql
├── procedures.sql
├── contacts.csv
└── contacts.json



---

## 🚀 How to Run

```bash
createdb phonebook
psql -d phonebook -f schema.sql
psql -d phonebook -f procedures.sql
pip install psycopg2
python phonebook.py