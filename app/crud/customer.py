from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.database import SessionLocal
from models.models import Customer as DBCustomer

router = APIRouter()

# Esquema universal de pydantic para operaciones
class Customer(BaseModel):
    customer_name: str
    customer_last_name: str
    email: str
    customer_password: str
    customer_type: str
    points: int

    class Config:
        from_attributes = True

# Esquema de pydantic con el id incluido para operar con el
class GetCustomerID(BaseModel):
    customer_id: int
    customer_name: str
    customer_last_name: str
    email: str
    customer_password: str
    customer_type: str
    points: int

    class Config:
        from_attributes = True

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Metodo para obtener todos los clientes
@router.get("/customers/", response_model=list[Customer])
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(DBCustomer).all()
    return customers

# Metodo para obtener un cliente por su id
@router.get("/customers/{customer_id}", response_model=GetCustomerID)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(DBCustomer).filter(DBCustomer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# Metodo para crear un cliente
@router.post("/customers/", response_model=Customer)
def create_customer(customer: Customer, db: Session = Depends(get_db)):
    db_customer = DBCustomer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# Metodo para actualizar un cliente
@router.put("/customers/{customer_id}", response_model=GetCustomerID)
def update_customer(customer_id: int, customer: Customer, db: Session = Depends(get_db)):
    db_customer = db.query(DBCustomer).filter(DBCustomer.customer_id == customer_id).first()
    if db_customer:
        # Actualizar los atributos del cliente
        db_customer.customer_name = customer.customer_name
        db_customer.customer_last_name = customer.customer_last_name
        db_customer.email = customer.email
        db_customer.customer_password = customer.customer_password
        db_customer.customer_type = customer.customer_type
        db_customer.points = customer.points

        db.commit()
        db.refresh(db_customer)
    return db_customer

# Metodo para eliminar un cliente
@router.delete("/customers/{customer_id}", response_model=GetCustomerID)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(DBCustomer).filter(DBCustomer.customer_id == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer