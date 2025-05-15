DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS user_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    password VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255)
);

INSERT INTO users (user_name, password, email, phone) VALUES ('Bridget', 'qwerty', 'bridget@example.com', '07402498078');
INSERT INTO users (user_name, password, email, phone) VALUES ('Hannah', '123456', 'hannah@example.com', '07987654321');