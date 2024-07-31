from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, validator
from datetime import datetime
from database.database import SessionLocal
from models.models import Sale as DBSale

router = APIRouter()

# Esquema pydantic para operaciones CRUD de ventas
class SaleBase(BaseModel):
    sale_date: datetime = Field(default_factory=datetime.utcnow)
    customer_id: int
    product_id: int
    price: float
    quantity: int
    employee_id: int

    @validator('sale_date', pre=True, always=True)
    def default_sale_date(cls, v):
        return v or datetime.utcnow()

    class Config:
        orm_mode = True

# Esquema pydantic para la creación de ventas
class CreateSale(SaleBase):
    pass

# Esquema pydantic para la respuesta de ventas con ID
class Sale(SaleBase):
    sale_id: int

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Método para obtener todas las ventas
@router.get("/", response_model=list[Sale])
def get_sales(db: Session = Depends(get_db)):
    sales = db.query(DBSale).all()
    return sales

# Método para obtener una venta por su ID
@router.get("/{sale_id}", response_model=Sale)
def read_sale(sale_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_sale = db.query(DBSale).filter(DBSale.sale_id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale

# Método para crear una venta
@router.post("/", response_model=Sale)
def create_sale(sale: CreateSale, db: Session = Depends(get_db)):
    db_sale = DBSale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

# Método para actualizar una venta
@router.put("/{sale_id}", response_model=Sale)
def update_sale(sale_id: int, sale: SaleBase, db: Session = Depends(get_db)):
    db_sale = db.query(DBSale).filter(DBSale.sale_id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    for field, value in sale.dict(exclude_unset=True).items():
        setattr(db_sale, field, value)
    
    db.commit()
    db.refresh(db_sale)
    return db_sale

# Método para eliminar una venta
@router.delete("/{sale_id}", response_model=Sale)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(DBSale).filter(DBSale.sale_id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    db.delete(db_sale)
    db.commit()
    return db_sale
