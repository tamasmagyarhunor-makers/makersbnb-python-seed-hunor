DROP TABLE IF EXISTS bookings; -- tests were failing as this line was below users. As it has fk dependencies it has to be dropped first
DROP TABLE IF EXISTS spaces;
DROP TABLE IF EXISTS users;


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL -- NOT NULL, can remove if not needed
);

CREATE TABLE spaces (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    price_per_night FLOAT,
    user_id INTEGER,
    CONSTRAINT fk_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    space_id INTEGER,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    CONSTRAINT fk_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_spaces
        FOREIGN KEY (space_id)
        REFERENCES spaces(id)
        ON DELETE CASCADE   
);


-- Sample seed data
INSERT INTO users (name, email, password) VALUES
('Alice', 'alice@example.com', 'password1'),
('Bob', 'bob@example.com', 'password2');


INSERT INTO spaces (user_id, name, description, price_per_night) VALUES
(1, 'Cozy london flat', 'A beautiful 1-bedroom flat in central london', 85.00),
(1, 'Garden studio', 'Peaceful studio with private garden access', 65.00),
(2, 'Modern Apartment', 'Stylish 2-bedroom apartment near the tube', 120.00);


INSERT INTO bookings (user_id, space_id, start_date, end_date) VALUES
(1, 3, '2025-01-01', '2025-01-05'),
(2, 1, '2025-09-10', '2025-09-15');