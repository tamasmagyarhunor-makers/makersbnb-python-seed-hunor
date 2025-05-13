-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

-- First, we must delete (drop) all our tables
DROP TABLE IF EXISTS spaces;
DROP SEQUENCE IF EXISTS spaces_id_seq;
DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS users_id_seq;

-- Then, we recreate them

-- Setting up the users table

CREATE SEQUENCE IF NOT EXISTS users_id_seq;

CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), email_address VARCHAR(255));

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

-- Finally, we add any records that are needed for the tests to run

INSERT INTO users (username, password, email_address) VALUES ('sashaparkes', 'mypassword1234', 'sashaparkes@email.com');

INSERT INTO spaces (name, description, price_per_night, host_id) VALUES ('The Barn', 'Converted barn set in a rural location', 65, 1);
INSERT INTO spaces (name, description, price_per_night, host_id) VALUES ('The Loft', 'City centre loft space with great access to amenities', 95, 1);
INSERT INTO spaces (name, description, price_per_night, host_id) VALUES ('The Hut', 'Rustic shepherds hut with its own hot tub', 55, 1);
INSERT INTO spaces (name, description, price_per_night, host_id) VALUES ('The Cottage', 'Cosy cottage with riverside views', 120, 1);
INSERT INTO spaces (name, description, price_per_night, host_id) VALUES ('The Penthouse', 'Top floor luxury penthouse with breathtaking views', 160, 1);
INSERT INTO spaces (name, description, price_per_night, host_id) VALUES ('The Beach Hut', 'Shoreline stay just footsteps from the seashore', 110, 1);

