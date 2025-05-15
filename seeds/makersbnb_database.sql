DROP TABLE IF EXISTS bookings;
DROP SEQUENCE IF EXISTS bookings_id_seq;

DROP TABLE IF EXISTS spaces;
DROP SEQUENCE IF EXISTS spaces_id_seq;

DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS user_id_seq;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255)
);

CREATE TABLE spaces (
    id SERIAL PRIMARY KEY,
    space_name VARCHAR(255),
    spaces_description text,
    price_per_night INTEGER, 
    available_from_date date,
    available_to_date date,
    user_id INTEGER,
    CONSTRAINT kf_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    space_id INTEGER,
    booking_date date,
    status VARCHAR(255),
    CONSTRAINT kf_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

INSERT INTO users (user_name, email, phone) VALUES ('Bridget', 'bridget@example.com', '07402498078');
INSERT INTO users (user_name, email, phone) VALUES ('Hannah', 'hannah@example.com', '07987654321');


INSERT INTO bookings (user_id, space_id, booking_date, status) VALUES (1, 1, '20250705', 'Requested');
INSERT INTO bookings (user_id, space_id, booking_date, status) VALUES (2, 2, '20251110', 'Booked');
INSERT INTO bookings (user_id, space_id, booking_date, status) VALUES (2, 2, '20251112', 'Rejected');

INSERT INTO spaces(space_name, spaces_description, price_per_night, available_from_date, available_to_date, user_id) VALUES ('Bee Hive', 'A peaceful hexagonal room', 85, '2025-07-01', '2025-07-12', 2);
INSERT INTO spaces(space_name, spaces_description, price_per_night, available_from_date, available_to_date, user_id) VALUES ('Ant farm', 'Bite-sized luxury pod', 77, '2025-11-06', '2025-11-20', 1);
INSERT INTO spaces(space_name, spaces_description, price_per_night, available_from_date, available_to_date, user_id) VALUES ('Ladybug Residence', 'Luxury spots available nightly', 99, '2025-08-12', '2025-08-31', 1);