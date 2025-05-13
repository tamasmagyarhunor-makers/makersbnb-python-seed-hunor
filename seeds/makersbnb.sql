-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

------------------------ users ------------------------

-- Delete (drop) all our tables
DROP TABLE IF EXISTS users CASCADE;
DROP SEQUENCE IF EXISTS users_id_seq;

-- Recreate them
CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email_address VARCHAR(255),
    password VARCHAR(255)
);

-- Add any records that are needed for the tests to run
INSERT INTO users (email_address, password) VALUES
('alice@example.com', 'password123'),
('bob@example.com', 'qwerty456'),
('carol@example.com', 'securepass789'),
('dave@example.com', 'letmein321'),
('eve@example.com', 'admin1234');

------------------------ spaces ------------------------

-- Delete (drop) all our tables
DROP TABLE IF EXISTS spaces CASCADE;
DROP SEQUENCE IF EXISTS spaces_id_seq;

-- Recreate them
CREATE SEQUENCE IF NOT EXISTS spaces_id_seq;
CREATE TABLE spaces (
    space_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description VARCHAR(255),
    price_per_night VARCHAR(255),
    user_id INT,
        CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- Add any records that are needed for the tests to run
INSERT INTO spaces (name, description, price_per_night, user_id) VALUES
('Cozy Cabin', 'Rustic cabin in the forest.', '100', 1),
('Urban Loft', 'Sleek apartment in downtown.', '150', 2),
('Beach Bungalow', 'Sunny spot by the sea.', '200', 3),
('Mountain Retreat', 'Quiet escape in the hills.', '180', 4),
('Modern Studio', 'Compact yet luxurious.', '120', 5);

------------------------ availabileRanges ------------------------

-- Delete (drop) all our tables
DROP TABLE IF EXISTS availabileRanges CASCADE;
DROP SEQUENCE IF EXISTS availabileRanges_id_seq;

-- Recreate them
CREATE SEQUENCE IF NOT EXISTS availabileRanges_id_seq;
CREATE TABLE availabileRanges (
    availability_id SERIAL PRIMARY KEY,
    start_range DATE,
    end_range DATE,
    space_id INT,
        CONSTRAINT fk_spaces FOREIGN KEY(space_id) REFERENCES spaces(space_id)
        ON DELETE CASCADE
);

-- Add any records that are needed for the tests to run
INSERT INTO availabileRanges (start_range, end_range, space_id) VALUES
('2025-06-01', '2025-06-10', 1),
('2025-06-05', '2025-06-15', 2),
('2025-07-01', '2025-07-10', 3),
('2025-07-15', '2025-07-25', 4),
('2025-08-01', '2025-08-10', 5);

------------------------ bookings ------------------------

-- Delete (drop) all our tables
DROP TABLE IF EXISTS bookings CASCADE;
DROP SEQUENCE IF EXISTS bookings_id_seq;

-- Recreate them
CREATE SEQUENCE IF NOT EXISTS bookings_id_seq;
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    start_range DATE,
    end_range DATE,
    space_id INT,
        CONSTRAINT fk_spaces FOREIGN KEY(space_id) REFERENCES spaces(space_id)
        ON DELETE CASCADE,
    user_id INT,
        CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,
    is_confirmed BOOLEAN
);

-- Add any records that are needed for the tests to run
INSERT INTO bookings (start_range, end_range, space_id, user_id, is_confirmed) VALUES
('2025-06-02', '2025-06-05', 1, 2, FALSE),
('2025-06-06', '2025-06-09', 2, 3, FALSE),
('2025-07-02', '2025-07-04', 3, 4, FALSE),
('2025-07-16', '2025-07-20', 4, 5, FALSE),
('2025-08-02', '2025-08-06', 5, 1, FALSE);