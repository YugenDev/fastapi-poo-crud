from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.database import SessionLocal
from models.models import Customer as DBCustomer

router = APIRouter()

# Esquema para la creación de un nuevo cliente
class CustomerCreate(BaseModel):
    costumer_name: str
    costumer_last_name: str
    email: str
    costumer_password: str
    costumer_type: str
    points: int

# Esquema para la actualización de un cliente existente
class CustomerUpdate(BaseModel):
    costumer_name: str = None
    costumer_last_name: str = None
    email: str = None
    costumer_password: str = None
    costumer_type: str = None
    points: int = None

    class Config:
        orm_mode = True

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/customers/{customer_id}", response_model=Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(DBCustomer).filter(DBCustomer.costumer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.post("/customers/", response_model=Customer)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = DBCustomer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(DBCustomer).filter(DBCustomer.costumer_id == customer_id).first()
    if db_customer:
        for var, value in vars(customer).items():
            setattr(db_customer, var, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

@router.delete("/customers/{customer_id}", response_model=Customer)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(DBCustomer).filter(DBCustomer.costumer_id == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer
