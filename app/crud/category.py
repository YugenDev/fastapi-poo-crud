from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.database import SessionLocal
from models.models import Category as DBCategory

router = APIRouter()

# Esquema universal de pydantic para operaciones
class Category(BaseModel):
    category_name: str

    class Config:
        orm_mode = True

# Esquema de pydantic con el id incluido para operar con el
class GetCategoryID(Category):
    category_id: int

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Método para obtener todas las categorías
@router.get("/categories/", response_model=list[GetCategoryID])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(DBCategory).all()
    return categories

# Método para obtener una categoría por su id
@router.get("/categories/{category_id}", response_model=GetCategoryID)
def read_category(category_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_category = db.query(DBCategory).filter(DBCategory.category_id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# Método para crear una categoría
@router.post("/categories/", response_model=Category)
def create_category(category: Category, db: Session = Depends(get_db)):
    db_category = DBCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Método para actualizar una categoría
@router.put("/categories/{category_id}", response_model=GetCategoryID)
def update_category(category_id: int, category: Category, db: Session = Depends(get_db)):
    db_category = db.query(DBCategory).filter(DBCategory.category_id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_category.category_name = category.category_name
    db.commit()
    db.refresh(db_category)
    return db_category

# Método para eliminar una categoría
@router.delete("/categories/{category_id}", response_model=GetCategoryID)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(DBCategory).filter(DBCategory.category_id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(db_category)
    db.commit()
    return db_category
