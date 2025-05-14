DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS user_id_seq;

DROP TABLE IF EXISTS bookings;
DROP SEQUENCE IF EXISTS bookings_id_seq;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255)
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

INSERT INTO bookings (user_id, space_id, booking_date, status) VALUES (1, 1, '20250601', 'Requested');
INSERT INTO bookings (user_id, space_id, booking_date, status) VALUES (2, 2, '20250701', 'Booked');
INSERT INTO bookings (user_id, space_id, booking_date, status) VALUES (2, 2, '20250801', 'Rejected');