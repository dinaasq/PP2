-- 1. Поиск по части имени или телефона
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_search TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id, c.name, c.phone FROM contacts c
    WHERE c.name ILIKE '%' || p_search || '%' 
       OR c.phone ILIKE '%' || p_search || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Пагинация (вывод порциями)
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id, c.name, c.phone FROM contacts c
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;