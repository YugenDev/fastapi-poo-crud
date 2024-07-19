-- Crear la base de datos TiendaJPBB
CREATE DATABASE TiendaJPBB;

-- Crear la tabla customer (cliente)
CREATE TABLE customer (
    customer_id serial PRIMARY KEY,
    customer_name varchar(55) NOT NULL,
    customer_last_name varchar(55) NOT NULL,
    email varchar(55) NOT NULL,
    customer_password text NOT NULL,
    customer_type varchar(55) NOT NULL,
    points int NOT NULL
);

-- Insertar datos de prueba en customer
INSERT INTO customer (customer_name, customer_last_name, email, customer_password, customer_type, points)
VALUES ('John', 'Doe', 'john.doe@example.com', 'password', 'regular', 100),
       ('Jane', 'Smith', 'jane.smith@example.com', 'password', 'regular', 50),
       ('Michael', 'Johnson', 'michael.johnson@example.com', 'password', 'premium', 200);

-- Crear la tabla employee (empleado)
CREATE TABLE employee (
    employee_id serial PRIMARY KEY,
    employee_name varchar(55) NOT NULL,
    employee_last_name varchar(55) NOT NULL,
    email varchar(55) NOT NULL,
    employee_password text NOT NULL,
    salary float NOT NULL,
    position varchar(55) NOT NULL
);

-- Insertar datos de prueba en employee
INSERT INTO employee (employee_name, employee_last_name, email, employee_password, salary, position)
VALUES ('Sarah', 'Anderson', 'sarah.anderson@example.com', 'password', 50000.0, 'Manager'),
       ('David', 'Wilson', 'david.wilson@example.com', 'password', 40000.0, 'Sales Associate');

-- Crear la tabla category (categoría)
CREATE TABLE category (
    category_id serial PRIMARY KEY,
    category_name varchar(55) NOT NULL
);

-- Insertar datos de prueba en category
INSERT INTO category (category_name)
VALUES ('Electronics'),
       ('Clothing'),
       ('Home Appliances');

-- Crear la tabla product (producto)
CREATE TABLE product (
    product_id serial PRIMARY KEY,
    product_name varchar(55) NOT NULL,
    description varchar(250) NOT NULL,
    category_id int NOT NULL,
    price float NOT NULL,
    quantity int NOT NULL,
    brand varchar(55) NOT NULL,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES category(category_id)
);

-- Insertar datos de prueba en product
INSERT INTO product (product_name, description, category_id, price, quantity, brand)
VALUES ('Smartphone', 'High-performance smartphone with latest features', 1, 799.99, 100, 'XYZ Electronics'),
       ('T-Shirt', 'Comfortable cotton T-shirt for everyday wear', 2, 19.99, 200, 'ABC Clothing'),
       ('Refrigerator', 'Energy-efficient refrigerator with large storage capacity', 3, 1499.99, 50, 'EFG Appliances');

-- Crear la tabla sales (ventas)
CREATE TABLE sales (
    sale_id serial PRIMARY KEY,
    sale_date timestamp NOT NULL,
    customer_id int NOT NULL,
    product_id int NOT NULL,
    price float NOT NULL,
    quantity int NOT NULL,
    total float GENERATED ALWAYS AS (price * quantity) STORED,
    employee_id int NOT NULL,
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES product(product_id),
    CONSTRAINT fk_employee FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- Insertar datos de prueba en sales
INSERT INTO sales (sale_date, customer_id, product_id, price, quantity, employee_id)
VALUES (CURRENT_TIMESTAMP, 1, 1, 799.99, 1, 1),
       (CURRENT_TIMESTAMP, 2, 2, 19.99, 2, 2),
       (CURRENT_TIMESTAMP, 3, 3, 1499.99, 1, 1);
