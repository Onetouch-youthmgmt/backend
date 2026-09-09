-- Run this in Supabase SQL Editor AFTER supabase_schema.sql.
-- Inserts sample data for local/dev testing. Uses explicit ids so
-- relationships line up predictably; sequences are reset at the end
-- so future inserts (via the app) continue from the right number.

-- 1. Sabha centers
INSERT INTO sabha_centers (id, name, address, city, responsible_person, contact_number) VALUES
    (1, 'Berlin Center', 'Alexanderplatz 1', 'Berlin', 'Raj Patel', '+491234567890'),
    (2, 'Munich Center', 'Marienplatz 5', 'Munich', 'Priya Shah', '+491234567891');

-- 2. Youths (2 karyakartas managing 2 other youths)
INSERT INTO youths (id, first_name, last_name, email, origin_city_india, current_city_germany, phone_number, birth_date, is_active, educational_field, is_karyakarta, karyakarta_id, address, pin_code) VALUES
    (1, 'Raj', 'Mehta', 'raj.mehta@example.com', 'Ahmedabad', 'Berlin', '+491111111111', '1995-04-12', true, 'Computer Science', true, NULL, 'Berlin Street 1', '10115'),
    (2, 'Aarav', 'Shah', 'aarav.shah@example.com', 'Surat', 'Berlin', '+491111111112', '1999-08-23', true, 'Mechanical Engineering', false, 1, 'Berlin Street 2', '10117'),
    (3, 'Diya', 'Patel', 'diya.patel@example.com', 'Vadodara', 'Berlin', '+491111111113', '2000-01-05', true, 'Business Administration', false, 1, 'Berlin Street 3', '10119'),
    (4, 'Kabir', 'Joshi', 'kabir.joshi@example.com', 'Rajkot', 'Munich', '+491111111114', '1997-11-30', true, 'Electrical Engineering', true, NULL, 'Munich Street 1', '80331');

-- 3. Youth <-> Sabha center associations (many-to-many)
INSERT INTO youth_sabha_center_association (youth_id, sabha_center_id) VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 2);

-- 4. Sabhas
INSERT INTO sabhas (id, topic, speaker_name, date, food, sabha_center_id) VALUES
    (1, 'Bhagavad Gita Discussion', 'Swami Ji', '2026-01-15', 'Prasad', 1),
    (2, 'Youth Meetup', 'Priya Shah', '2026-02-10', 'Snacks', 1),
    (3, 'Festival Planning', 'Kabir Joshi', '2026-01-20', 'Dinner', 2);

-- 5. Attendance
INSERT INTO attendances (sabha_id, youth_id, is_present) VALUES
    (1, 2, true),
    (1, 3, false),
    (2, 2, true),
    (2, 3, true),
    (3, 4, true);

-- Reset auto-increment sequences so the app's next inserts don't collide with these explicit ids
SELECT setval(pg_get_serial_sequence('sabha_centers', 'id'), (SELECT MAX(id) FROM sabha_centers));
SELECT setval(pg_get_serial_sequence('youths', 'id'), (SELECT MAX(id) FROM youths));
SELECT setval(pg_get_serial_sequence('sabhas', 'id'), (SELECT MAX(id) FROM sabhas));
SELECT setval(pg_get_serial_sequence('attendances', 'id'), (SELECT MAX(id) FROM attendances));
