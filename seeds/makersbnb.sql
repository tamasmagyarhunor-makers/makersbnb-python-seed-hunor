DROP TABLE IF EXISTS user_table;

CREATE TABLE user_table (
    id SERIAL PRIMARY KEY,
    name text,
    email text,
    password text,
    phone_number text
);

INSERT INTO user_table (name, email, password, phone_number) VALUES ('Yahya', 'yahya@makers.com', 'Blahblah1!', '012345678901');
INSERT INTO user_table (name, email, password, phone_number) VALUES ('Pat', 'pat@makers.com', 'Blahblah2!', '012345678902');
