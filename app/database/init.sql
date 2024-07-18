-- Crear la base de datos TiendaJPBB
CREATE DATABASE TiendaJPBB;

-- Crear la tabla costumer (cliente)
CREATE TABLE customer (
    customer_id serial PRIMARY KEY,
    customer_name varchar(55) NOT NULL,
    customer_last_name varchar(55) NOT NULL,
    email varchar(55) NOT NULL,
    customer_password varchar(8) NOT NULL,
    customer_type varchar(55) NOT NULL,
    points int NOT NULL
);

-- Crear la tabla employee (empleado)
CREATE TABLE employee (
    employee_id serial PRIMARY KEY,
    employee_name varchar(55) NOT NULL,
    employee_last_name varchar(55) NOT NULL,
    email varchar(55) NOT NULL,
    employee_password varchar(8) NOT NULL,
    salary float NOT NULL,
    position varchar(55) NOT NULL
);

-- Crear la tabla category (categoría)
CREATE TABLE category (
    category_id serial PRIMARY KEY,
    category_name varchar(55) NOT NULL
);

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

-- Crear la tabla sales (ventas)
CREATE TABLE sales (
    sale_id serial PRIMARY KEY,
    sale_date timestamp NOT NULL,
    costumer_id int NOT NULL,
    product_id int NOT NULL,
    price float NOT NULL,
    quantity int NOT NULL,
    total float GENERATED ALWAYS AS (price * quantity) STORED,
    employee_id int NOT NULL,
    CONSTRAINT fk_costumer FOREIGN KEY (costumer_id) REFERENCES costumer(costumer_id),
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES product(product_id),
    CONSTRAINT fk_employee FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);
