from pydantic import BaseModel
from models.models import Employee as DBEmployee
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal

router = APIRouter()

# Esquema universal de pydantic para operaciones del CRUD
class Employee(BaseModel):
    employee_id: int
    employee_name: str
    employee_last_name: str
    email: str
    employee_password: str
    salary: float
    position: str

    class Config:
        orm_mode = True

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Metodo para crear un empleado
@router.post("/employees/", response_model=Employee)
def create_employee(employee: Employee, db: Session = Depends(get_db)):
    db_employee = DBEmployee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Metodo para obtener todos los empleados
@router.get("/employees/", response_model=list[Employee])
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(DBEmployee).all()
    return employees

# Metodo para obtener un empleado por su id
@router.get("/employees/{employee_id}", response_model=Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(DBEmployee).filter(DBEmployee.employee_id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

# Metodo para actualizar un empleado
@router.put("/employees/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, employee: Employee, db: Session = Depends(get_db)):
    db_employee = db.query(DBEmployee).filter(DBEmployee.employee_id == employee_id).first()
    if db_employee:
        # Actualizar los atributos del empleado
        db_employee.employee_name = employee.employee_name
        db_employee.employee_last_name = employee.employee_last_name
        db_employee.email = employee.email
        db_employee.employee_password = employee.employee_password
        db_employee.salary = employee.salary
        db_employee.position = employee.position

        db.commit()
        db.refresh(db_employee)
    return db_employee

# Metodo para borrar un empleado
@router.delete("/employees/{employee_id}", response_model=Employee)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(DBEmployee).filter(DBEmployee.employee_id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee
