from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, backref, column_property
from database.database import Base

class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(55), nullable=False)
    customer_last_name = Column(String(55), nullable=False)
    email = Column(String(55), nullable=False, unique=True)
    customer_password = Column(Text, nullable=False)
    customer_type = Column(String(55), nullable=False)
    points = Column(Integer, nullable=False)

    # Relación con ventas (uno a muchos)
    sales = relationship("Sale", back_populates="customer", cascade="all, delete-orphan")

class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_name = Column(String(55), nullable=False)
    employee_last_name = Column(String(55), nullable=False)
    email = Column(String(55), nullable=False, unique=True)
    employee_password = Column(Text, nullable=False)
    salary = Column(Float, nullable=False)
    position = Column(String(55), nullable=False)

    # Relación con ventas (uno a muchos)
    sales = relationship("Sale", back_populates="employee", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(55), nullable=False)

    # Relación con productos (uno a muchos)
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")

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
    sales = relationship("Sale", back_populates="product", cascade="all, delete-orphan")

class Sale(Base):
    __tablename__ = 'sales'

    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    sale_date = Column(DateTime, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'), nullable=False)

    # Relaciones con cliente, producto y empleado
    customer = relationship("Customer", back_populates="sales")
    product = relationship("Product", back_populates="sales")
    employee = relationship("Employee", back_populates="sales")

    # Propiedad de columna para 'total', leer directamente desde la base de datos
    total = column_property(
        Column(Float, nullable=False, server_default='0'),
        deferred=True
    )

