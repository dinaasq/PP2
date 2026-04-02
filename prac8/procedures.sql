-- 1. Добавление или обновление (Upsert)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- 2. Массовая вставка с проверкой длины номера
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(p_names TEXT[], p_phones TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_upper(p_names, 1) LOOP
        IF length(p_phones[i]) >= 5 THEN
            INSERT INTO contacts (name, phone) VALUES (p_names[i], p_phones[i]);
        ELSE
            RAISE NOTICE 'Номер для % слишком короткий', p_names[i];
        END IF;
    END LOOP;
END;
$$;

-- 3. Удаление по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact(p_search VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts WHERE name = p_search OR phone = p_search;
END;
$$;