from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import Employee as DBEmployee

router = APIRouter()

# Esquema de pydantic para operaciones CRUD de empleados
class EmployeeBase(BaseModel):
    employee_name: str
    employee_last_name: str
    email: EmailStr
    employee_password: str
    salary: float
    position: str

    class Config:
        orm_mode = True

# Esquema de pydantic para la creación de empleados
class CreateEmployee(EmployeeBase):
    pass

# Esquema de pydantic para la respuesta de empleados con ID
class Employee(EmployeeBase):
    employee_id: int

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Método para crear un empleado
@router.post("/", response_model=Employee)
def create_employee(employee: CreateEmployee, db: Session = Depends(get_db)):
    db_employee = DBEmployee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Método para obtener todos los empleados
@router.get("/", response_model=list[Employee])
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(DBEmployee).all()
    return employees

# Método para obtener un empleado por su ID
@router.get("/{employee_id}", response_model=Employee)
def read_employee(employee_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_employee = db.query(DBEmployee).filter(DBEmployee.employee_id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

# Método para actualizar un empleado
@router.put("/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, employee: EmployeeBase, db: Session = Depends(get_db)):
    db_employee = db.query(DBEmployee).filter(DBEmployee.employee_id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for field, value in employee.dict(exclude_unset=True).items():
        setattr(db_employee, field, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Método para borrar un empleado
@router.delete("/{employee_id}", response_model=Employee)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(DBEmployee).filter(DBEmployee.employee_id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(db_employee)
    db.commit()
    return db_employee
