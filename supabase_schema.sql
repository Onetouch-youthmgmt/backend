-- Run this once in the Supabase SQL Editor (Project -> SQL Editor -> New query)
-- Recreates the schema previously managed by Alembic/SQLAlchemy.

CREATE TABLE IF NOT EXISTS sabha_centers (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    responsible_person VARCHAR NOT NULL,
    contact_number VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS youths (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    origin_city_india VARCHAR NOT NULL,
    current_city_germany VARCHAR NOT NULL,
    phone_number VARCHAR NOT NULL,
    birth_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    is_active BOOLEAN DEFAULT true,
    educational_field VARCHAR,
    is_karyakarta BOOLEAN DEFAULT false,
    address VARCHAR,
    pin_code VARCHAR,
    karyakarta_id INTEGER REFERENCES youths(id)
);
CREATE INDEX IF NOT EXISTS ix_youths_email ON youths(email);
CREATE INDEX IF NOT EXISTS ix_youths_created_at ON youths(created_at);
CREATE INDEX IF NOT EXISTS ix_youths_is_active ON youths(is_active);
CREATE INDEX IF NOT EXISTS ix_youths_karyakarta_id ON youths(karyakarta_id);

CREATE TABLE IF NOT EXISTS youth_sabha_center_association (
    youth_id INTEGER REFERENCES youths(id),
    sabha_center_id INTEGER REFERENCES sabha_centers(id)
);
CREATE INDEX IF NOT EXISTS ix_youth_sabha_center_association_youth_id ON youth_sabha_center_association(youth_id);
CREATE INDEX IF NOT EXISTS ix_youth_sabha_center_association_sabha_center_id ON youth_sabha_center_association(sabha_center_id);

CREATE TABLE IF NOT EXISTS sabhas (
    id SERIAL PRIMARY KEY,
    topic VARCHAR NOT NULL,
    speaker_name VARCHAR NOT NULL,
    date DATE NOT NULL,
    food VARCHAR NOT NULL,
    sabha_center_id INTEGER NOT NULL REFERENCES sabha_centers(id)
);
CREATE INDEX IF NOT EXISTS ix_sabhas_sabha_center_id ON sabhas(sabha_center_id);

CREATE TABLE IF NOT EXISTS attendances (
    id SERIAL PRIMARY KEY,
    sabha_id INTEGER NOT NULL REFERENCES sabhas(id),
    youth_id INTEGER REFERENCES youths(id),
    is_present BOOLEAN DEFAULT false,
    UNIQUE (sabha_id, youth_id)
);
CREATE INDEX IF NOT EXISTS ix_attendances_sabha_id ON attendances(sabha_id);
CREATE INDEX IF NOT EXISTS ix_attendances_youth_id ON attendances(youth_id);
