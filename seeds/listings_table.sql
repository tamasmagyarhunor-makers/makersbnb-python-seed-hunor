DROP TABLE IF EXISTS listings;
DROP SEQUENCE IF EXISTS listings_id_seq;

CREATE TABLE listings (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    price int,
    image TEXT,
    user_id int
);

INSERT INTO listings (name, description, price, image, user_id) VALUES ('Country Cottage', 'Quaint little cottage with a view', 75, 'countrycottage.jpg', 1);
INSERT INTO listings (name, description, price, image, user_id) VALUES ('Beach House', 'Well situated beachfront property', 100, 'beachhouse.jpeg', 1);
INSERT INTO listings (name, description, price, image, user_id) VALUES ('Potato House', 'House that looks like a potato', 250, 'potato.jpg', 2);