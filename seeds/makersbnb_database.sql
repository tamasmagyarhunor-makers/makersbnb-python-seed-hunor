DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS user_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255)
);

INSERT INTO users (user_name, email, phone) VALUES ('Bridget', 'bridget@example.com', '07402498078');
INSERT INTO users (user_name, email, phone) VALUES ('Hannah', 'hannah@example.com', '07987654321');