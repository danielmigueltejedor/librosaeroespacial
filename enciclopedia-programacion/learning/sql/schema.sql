CREATE TABLE customer(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL,
                    cents INTEGER NOT NULL, paid INTEGER);
INSERT INTO customer VALUES (1, 'Ada'), (2, 'Grace'), (3, 'Linus');
INSERT INTO orders VALUES (1, 1, 100, 1), (2, 1, 200, 0), (3, 2, 300, NULL);
