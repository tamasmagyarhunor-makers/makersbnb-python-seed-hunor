DROP TABLE IF EXISTS bookings;
DROP SEQUENCE IF EXISTS bookings_id_seq;

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

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    listing_id INT REFERENCES listings(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    UNIQUE (listing_id, start_date, end_date)
);



INSERT INTO listings (name, description, price, image, user_id) VALUES ('Country Cottage', 'Quaint little cottage with a view', 75, 'countrycottage.jpg', 1);
INSERT INTO listings (name, description, price, image, user_id) VALUES ('Beach House', 'Well situated beachfront property', 100, 'beachhouse.jpeg', 1);
INSERT INTO listings (name, description, price, image, user_id) VALUES ('Potato House', 'House that looks like a potato', 250, 'potato.jpg', 2);