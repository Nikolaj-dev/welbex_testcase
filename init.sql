-- Проверяем существование базы данных
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'testcase') THEN
        CREATE DATABASE testcase;
    END IF;
END $$;

-- Проверяем существование пользователя и предоставляем ему привилегии
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'nick') THEN
        CREATE USER nick WITH PASSWORD 'nick';
        GRANT ALL PRIVILEGES ON DATABASE testcase TO nick;
    END IF;
END $$;
