from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database.database import SessionLocal
from models.models import Customer as DBCustomer

router = APIRouter()

# Esquema universal de pydantic para operaciones
class CustomerBase(BaseModel):
    customer_name: str
    customer_last_name: str
    email: EmailStr
    customer_password: str
    customer_type: str
    points: int

    class Config:
        orm_mode = True

# Esquema de pydantic con el id incluido para operar con el
class Customer(CustomerBase):
    customer_id: int

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Método para obtener todos los clientes
@router.get("/customers/", response_model=list[Customer])
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(DBCustomer).all()
    return customers

# Método para obtener un cliente por su id
@router.get("/customers/{customer_id}", response_model=Customer)
def read_customer(customer_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_customer = db.query(DBCustomer).filter(DBCustomer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# Método para crear un cliente
@router.post("/customers/", response_model=Customer)
def create_customer(customer: CustomerBase, db: Session = Depends(get_db)):
    db_customer = DBCustomer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# Método para actualizar un cliente
@router.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerBase, db: Session = Depends(get_db)):
    db_customer = db.query(DBCustomer).filter(DBCustomer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    for attr, value in customer.dict(exclude_unset=True).items():
        setattr(db_customer, attr, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer

# Método para eliminar un cliente
@router.delete("/customers/{customer_id}", response_model=Customer)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(DBCustomer).filter(DBCustomer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(db_customer)
    db.commit()
    return db_customer
