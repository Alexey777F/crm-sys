CREATE TABLE managers (
  id SERIAL PRIMARY KEY,
  username VARCHAR(25) NOT NULL,
  password VARCHAR(255) NOT NULL,
  full_name VARCHAR(100) NOT NULL,
  working_position VARCHAR(70) NOT NULL,
  city VARCHAR(30) NOT NULL,
  phone_number VARCHAR(11) NOT NULL,
  email VARCHAR(50)
);

INSERT INTO managers (username, password, full_name, working_position, city, phone_number, email) VALUES ('Alexey', 'pbkdf2:sha256:600000$d2b10DM9WleyyqZN$08e02efa33d5b8c77c0c289d24b7bede053de115df782310b4961ab4dd8128d0', 'Фомин Алексей Геннадьевич', 'Разработчик', 'Москва', '89931234598', 'fff777@mail.ru');
INSERT INTO managers (username, password, full_name, working_position, city, phone_number, email) VALUES ('Daria', 'pbkdf2:sha256:600000$d2b10DM9WleyyqZN$08e02efa33d5b8c77c0c289d24b7bede053de115df782310b4961ab4dd8128d0', 'Каланча Дарья Викторовна', 'Руководитель', 'Москва', '89931232256', 'ddd777@mail.com');


CREATE TABLE clients (
  id SERIAL PRIMARY KEY,
  customer VARCHAR(50) NOT NULL,
  phone_number VARCHAR(11) NOT NULL,
  email VARCHAR(50)
);

CREATE INDEX idx_clients_phone_number ON clients (phone_number);
CREATE INDEX idx_clients_email ON clients (email);


CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer VARCHAR(65) NOT NULL,
  description VARCHAR(255) NOT NULL,
  income INTEGER NOT NULL,
  status VARCHAR(20) NOT NULL,
  dates DATE NOT NULL,
  manager_id INTEGER REFERENCES managers(id),
  client_id INTEGER REFERENCES clients(id)
);

CREATE INDEX idx_orders_customer ON orders (customer);


CREATE TABLE combined (
  manager_id INTEGER REFERENCES managers(id),
  order_id INTEGER REFERENCES orders(id),
  PRIMARY KEY (manager_id, order_id)
);