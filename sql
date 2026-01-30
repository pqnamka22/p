-- Таблица пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    spent_stars DECIMAL(20, 2) DEFAULT 0,
    rank_id INT REFERENCES ranks(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица рангов
CREATE TABLE ranks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    min_stars DECIMAL(20, 2) NOT NULL,
    icon VARCHAR(10),
    color VARCHAR(7)
);

-- Таблица транзакций
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    amount DECIMAL(20, 2) NOT NULL,
    type VARCHAR(20) CHECK (type IN ('spend', 'receive')),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица целей сообщества
CREATE TABLE community_goals (
    id SERIAL PRIMARY KEY,
    target_stars DECIMAL(20, 2) NOT NULL,
    description TEXT NOT NULL,
    reward_description TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    current_progress DECIMAL(20, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
