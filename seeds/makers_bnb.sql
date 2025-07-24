DROP TABLE IF EXISTS availabilities; -- these tables have fks so must be dropped first
DROP TABLE IF EXISTS bookings; -- these tables have fks so must be dropped first
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

CREATE TABLE availabilities (
    id SERIAL PRIMARY KEY,
    space_id INTEGER NOT NULL,
    available_from DATE NOT NULL,
    available_to DATE NOT NULL,
    CONSTRAINT fk_spaces FOREIGN KEY (space_id) REFERENCES spaces(id) ON DELETE CASCADE
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    space_id INTEGER,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT DEFAULT 'pending',
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

INSERT INTO spaces (name, description, price_per_night, user_id) VALUES
('Cozy london flat', 'A beautiful 1-bedroom flat in central london', 85.00, 1),
('Garden studio', 'Peaceful studio with private garden access', 65.00, 1),
('Modern Apartment', 'Stylish 2-bedroom apartment near the tube', 120.00, 2);

INSERT INTO availabilities (space_id, available_from, available_to) VALUES
(1, '2025-07-24', '2025-08-24'),
(1, '2025-09-30', '2025-12-20'),
(2, '2025-07-24', '2025-09-30'),
(3, '2025-07-24', '2025-12-31');

INSERT INTO bookings (user_id, space_id, start_date, end_date, status) VALUES
(1, 3, '2025-01-01', '2025-01-05', 'confirmed'),
(2, 1, '2025-09-10', '2025-09-15', 'confirmed');