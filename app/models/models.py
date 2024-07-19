from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, column_property
from database.database import Base

class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    customer_name = Column(String(55), nullable=False)
    customer_last_name = Column(String(55), nullable=False)
    email = Column(String(55), nullable=False, unique=True)
    customer_password = Column(String(8), nullable=False)
    customer_type = Column(String(55), nullable=False)
    points = Column(Integer, nullable=False)

    # Relación con ventas (uno a muchos)
    sales = relationship("Sale", back_populates="customer")

class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_name = Column(String(55), nullable=False)
    employee_last_name = Column(String(55), nullable=False)
    email = Column(String(55), nullable=False, unique=True)
    employee_password = Column(String(8), nullable=False)
    salary = Column(Float, nullable=False)
    position = Column(String(55), nullable=False)

    # Relación con ventas (uno a muchos)
    sales = relationship("Sale", back_populates="employee")

class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(55), nullable=False)

    # Relación con productos (uno a muchos)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'product'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(55), nullable=False)
    description = Column(String(250), nullable=False)
    category_id = Column(Integer, ForeignKey('category.category_id'), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    brand = Column(String(55), nullable=False)

    # Relación con categoría (muchos a uno)
    category = relationship("Category", back_populates="products")

    # Relación con ventas (uno a muchos)
    sales = relationship("Sale", back_populates="product")

class Sale(Base):
    __tablename__ = 'sales'

    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    sale_date = Column(DateTime, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relación con cliente (muchos a uno)
    customer = relationship("Customer", back_populates="sales")

    # Relación con producto (muchos a uno)
    product = relationship("Product", back_populates="sales")

    # Relación con empleado (muchos a uno)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'), nullable=False)
    employee = relationship("Employee", back_populates="sales")

    # Propiedad de columna para 'total', leer directamente desde la base de datos
    total = column_property(
        Column(Float, nullable=False, server_default='0'),
        deferred=True
    )
