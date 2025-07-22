DROP TABLE IF EXISTS spaces;
DROP TABLE IF EXISTS users;


CREATE TABLE spaces (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    price_per_night FLOAT,
    constraint fk_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL, -- NOT NULL, can remove if not needed
);

-- Samplpe seed data
INSERT INTO users (name, email, password) VALUES
('Alice', 'alice@example.com', 'password1')
('Bob', 'bob@example.com', 'password2')


INSERT INTO spaces (user_id, name, description, price_per_night) VALUES
(1, 'Cozy london flat', 'A beautiful 1-bedroom flat in central london', 85.00),
(1, 'Garden studio', 'Peaceful studio with private gardne access', 65.00),
(2, 'Modern Apartment', 'Stylish 2-bedroom apartment near the tube', 120.00);
