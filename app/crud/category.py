from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.database import SessionLocal
from models.models import Category as DBCategory

router = APIRouter()

# Esquema universal de pydantic para operaciones
class Category(BaseModel):
    category_name: str

    class Config:
        from_attributes = True

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Metodo para obtener todas las categorías
@router.get("/categories/", response_model=list[Category])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(DBCategory).all()
    return categories

# Metodo para obtener una categoría por su id
@router.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(DBCategory).filter(DBCategory.category_id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# Metodo para crear una categoría
@router.post("/categories/", response_model=Category)
def create_category(category: Category, db: Session = Depends(get_db)):
    db_category = DBCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Metodo para actualizar una categoría
@router.put("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category: Category, db: Session = Depends(get_db)):
    db_category = db.query(DBCategory).filter(DBCategory.category_id == category_id).first()
    if db_category:
        db_category.category_name = category.category_name
        db.commit()
        db.refresh(db_category)
    return db_category

# Metodo para eliminar una categoría
@router.delete("/categories/{category_id}", response_model=Category)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(DBCategory).filter(DBCategory.category_id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category
