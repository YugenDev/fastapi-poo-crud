from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.database import SessionLocal
from models.models import Product as DBProduct

router = APIRouter()

# Esquema pydantic para operaciones CRUD de productos
class ProductBase(BaseModel):
    product_name: str
    description: str
    category_id: int
    price: float
    quantity: int
    brand: str

    class Config:
        orm_mode = True

# Esquema pydantic para la creación de productos
class CreateProduct(ProductBase):
    pass

# Esquema pydantic para la respuesta de productos con ID
class Product(ProductBase):
    product_id: int

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Método para obtener todos los productos
@router.get("/products/", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(DBProduct).all()
    return products

# Método para obtener un producto por su ID
@router.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Método para crear un producto
@router.post("/products/", response_model=Product)
def create_product(product: CreateProduct, db: Session = Depends(get_db)):
    db_product = DBProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Método para actualizar un producto
@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductBase, db: Session = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for field, value in product.dict(exclude_unset=True).items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

# Método para eliminar un producto
@router.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return db_product
