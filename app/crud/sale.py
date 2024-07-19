from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime
from database.database import SessionLocal
from models.models import Sale as DBSale, Customer, Product, Employee
from sqlalchemy import func

router = APIRouter()

# Esquema universal de pydantic para operaciones
class Sale(BaseModel):
    sale_date: datetime = Field(default_factory=datetime.utcnow)
    customer_id: int
    product_id: int
    price: float
    quantity: int
    employee_id: int

    class Config:
        from_attributes = True

# Esquema para obtener una venta
class GetSale(BaseModel):
    sale_date: datetime = Field(default_factory=datetime.utcnow)
    customer_id: int
    product_id: int
    price: float
    quantity: int
    total: float
    employee_id: int

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Metodo para obtener todas las ventas
@router.get("/sales/", response_model=list[GetSale])
def get_sales(db: Session = Depends(get_db)):
    sales = db.query(DBSale).all()
    return sales

# Metodo para obtener una venta por su id
@router.get("/sales/{sale_id}", response_model=Sale)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(DBSale).filter(DBSale.sale_id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale

# Metodo para crear una venta
@router.post("/sales/", response_model=Sale)
def create_sale(sale: Sale, db: Session = Depends(get_db)):
    db_sale = DBSale(
        sale_date=func.now(),  # Utilizamos func.now() de SQLAlchemy para la fecha actual
        customer_id=sale.customer_id,
        product_id=sale.product_id,
        price=sale.price,
        quantity=sale.quantity,
        employee_id=sale.employee_id
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

# Metodo para actualizar una venta
@router.put("/sales/{sale_id}", response_model=Sale)
def update_sale(sale_id: int, sale: Sale, db: Session = Depends(get_db)):
    db_sale = db.query(DBSale).filter(DBSale.sale_id == sale_id).first()
    if db_sale:
        db_sale.sale_date = func.now()  # Actualizamos la fecha de venta con la fecha actual
        db_sale.customer_id = sale.customer_id
        db_sale.product_id = sale.product_id
        db_sale.price = sale.price
        db_sale.quantity = sale.quantity
        db_sale.employee_id = sale.employee_id

        db.commit()
        db.refresh(db_sale)
    return db_sale

# Metodo para eliminar una venta
@router.delete("/sales/{sale_id}", response_model=Sale)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(DBSale).filter(DBSale.sale_id == sale_id).first()
    if db_sale:
        db.delete(db_sale)
        db.commit()
    return db_sale
