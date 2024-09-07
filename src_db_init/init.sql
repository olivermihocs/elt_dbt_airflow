CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
);

INSERT INTO users (first_name, last_name, email) VALUES
('Oliver', 'Mihocs', 'oliver.mihocs@gmail');

CREATE TABLE cars (
    car_id SERIAL PRIMARY KEY,
    model VARCHAR(255) NOT NULL,
    release_date DATE,
    price INTEGER,
    car_rating DECIMAL(2,1) CHECK (car_rating >= 1 AND car_rating <= 5)
);

INSERT INTO cars (model, release_date, price, car_rating) VALUES
('Civic', '2025-01-01', 24500, 4.7),
('Accord', '2024-01-01', 27895, 4.8),
('Stinger', '2023-01-01', 52750, 4.3),
('Soul', '2025-01-01', 20290, 4.4),
('Prius', '2025-01-01', 27950, 4.8),
('Rio', '2023-01-01', 19690, 4.3),
('MX-5 Miata', '2024-01-01', 28985, 4.8),
('Corvette', '2024-01-01', 68300, 4.7);

CREATE TABLE manufacturers (
    manufacturer_id SERIAL PRIMARY KEY,
    manufacturer_name VARCHAR(255) NOT NULL
);

CREATE TABLE manufacturers_cars (
    manufacturer_id INTEGER REFERENCES manufacturers(manufacturer_id),
    car_id INTEGER REFERENCES cars(car_id),
    PRIMARY KEY (car_id, manufacturer_id)
);

INSERT INTO manufacturers (manufacturer_name) VALUES
('Honda'),
('Kia'),
('Toyota'),
('MAZDA'),
('Chevrolet');


INSERT INTO manufacturers_cars (manufacturer_id, car_id) VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4),
(3, 5),
(2, 6),
(4, 7),
(5, 8);