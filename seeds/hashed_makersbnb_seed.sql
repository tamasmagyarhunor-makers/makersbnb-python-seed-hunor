-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

-- First, we must delete (drop) all our tables
DROP TABLE IF EXISTS availability_ranges;
DROP SEQUENCE IF EXISTS availability_ranges_id_seq;
DROP TABLE IF EXISTS bookings;
DROP SEQUENCE IF EXISTS bookings_id_seq;
DROP TABLE IF EXISTS booking_requests;
DROP SEQUENCE IF EXISTS booking_requests_id_seq;
DROP TABLE IF EXISTS spaces;
DROP SEQUENCE IF EXISTS spaces_id_seq;
DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS users_id_seq;
-- Then, we recreate them

-- Setting up the users table

CREATE SEQUENCE IF NOT EXISTS users_id_seq;

CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(255), password VARCHAR(255), email_address VARCHAR(255));

-- Setting up the spaces table
CREATE SEQUENCE IF NOT EXISTS spaces_id_seq;
CREATE TABLE  spaces (

id SERIAL PRIMARY KEY, 
name VARCHAR(255), 
description VARCHAR(255), 
price_per_night INTEGER, 
host_id INTEGER, 

constraint fk_host foreign key (host_id)

    references users(id)
    on delete cascade
);

-- Setting up the availability_ranges table
CREATE SEQUENCE IF NOT EXISTS availability_ranges_id_seq;
CREATE TABLE  availability_ranges (

id SERIAL PRIMARY KEY, 
start_date VARCHAR(255), 
end_date VARCHAR(255), 
space_id INTEGER, 

constraint fk_space foreign key (space_id)

    references spaces(id)
    on delete cascade
);

-- Setting up the availability_ranges table
CREATE SEQUENCE IF NOT EXISTS bookings_id_seq;
CREATE TABLE  bookings (

id SERIAL PRIMARY KEY, 
start_date VARCHAR(255), 
end_date VARCHAR(255), 
space_id INTEGER,
user_id INTEGER, 

constraint fk_space foreign key (space_id)

    references spaces(id)
    on delete cascade,

constraint fk_user foreign key (user_id)

    references users(id)
    on delete cascade
);

CREATE SEQUENCE IF NOT EXISTS booking_requests_id_seq;
CREATE TABLE  booking_requests (

id SERIAL PRIMARY KEY, 
start_date VARCHAR(255), 
end_date VARCHAR(255), 
space_id INTEGER,
user_id INTEGER, 

constraint fk_space foreign key (space_id)

    references spaces(id)
    on delete cascade,

constraint fk_user foreign key (user_id)

    references users(id)
    on delete cascade
);

-- Finally, we add any records that are needed for the tests to run

INSERT INTO users (name, password, email_address) VALUES ('Sasha Parkes', '$2b$12$n1GzTQLs1ukQAslENaCMbuyuVUUksFHM4heM9TJYVn.KDBjzMzVCi', 'sashaparkes@email.com');
INSERT INTO users (name, password, email_address) VALUES ('James Dismore', 'mypassword54321', 'jamesdismore@email.com');

INSERT INTO spaces (name, description, price_per_night, host_id) VALUES ('The Barn', 'Converted barn set in a rural location', 65, 1);
INSERT INTO spaces (name, description, price_per_night, host_id) VALUES ('The Loft', 'City centre loft space with great access to amenities', 95, 2);
INSERT INTO spaces (name, description, price_per_night, host_id) VALUES ('The Hut', 'Rustic shepherds hut with its own hot tub', 55, 2);
INSERT INTO spaces (name, description, price_per_night, host_id) VALUES ('The Cottage', 'Cosy cottage with riverside views', 120, 1);
INSERT INTO spaces (name, description, price_per_night, host_id) VALUES ('The Penthouse', 'Top floor luxury penthouse with breathtaking views', 160, 1);
INSERT INTO spaces (name, description, price_per_night, host_id) VALUES ('The Beach Hut', 'Shoreline stay just footsteps from the seashore', 110, 2);

INSERT INTO availability_ranges (start_date,end_date,space_id) VALUES ('2025-01-01','2026-01-01',1);
INSERT INTO availability_ranges (start_date,end_date,space_id) VALUES ('2025-01-01','2026-01-01',2);
INSERT INTO availability_ranges (start_date,end_date,space_id) VALUES ('2025-01-01','2025-01-07',3);

INSERT INTO bookings (start_date,end_date,space_id,user_id) VALUES ('2025-10-01','2025-10-02',1,2);
INSERT INTO bookings (start_date,end_date,space_id,user_id) VALUES ('2025-11-01','2025-11-05',2,1);
INSERT INTO bookings (start_date,end_date,space_id,user_id) VALUES ('2025-01-01','2025-01-02',3,1);
INSERT INTO bookings (start_date,end_date,space_id,user_id) VALUES ('2025-01-04','2025-01-06',3,1);

INSERT INTO booking_requests (start_date,end_date,space_id,user_id) VALUES ('2025-11-05','2025-11-06',1,2);
INSERT INTO booking_requests (start_date,end_date,space_id,user_id) VALUES ('2025-01-10','2025-01-12',2,1);