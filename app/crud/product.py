from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.database import SessionLocal
from models.models import Product as DBProduct

router = APIRouter()

# Esquema universal de pydantic para operaciones
class Product(BaseModel):
    product_name: str
    description: str
    category_id: int
    price: float
    quantity: int
    brand: str

    class Config:
        from_attributes = True

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Metodo para obtener todos los productos
@router.get("/products/", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(DBProduct).all()
    return products

# Metodo para obtener un producto por su id
@router.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Metodo para crear un producto
@router.post("/products/", response_model=Product)
def create_product(product: Product, db: Session = Depends(get_db)):
    db_product = DBProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Metodo para actualizar un producto
@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.product_id == product_id).first()
    if db_product:
        db_product.product_name = product.product_name
        db_product.description = product.description
        db_product.category_id = product.category_id
        db_product.price = product.price
        db_product.quantity = product.quantity
        db_product.brand = product.brand

        db.commit()
        db.refresh(db_product)
    return db_product

# Metodo para eliminar un producto
@router.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.product_id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
