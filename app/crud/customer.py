from sqlalchemy.orm import Session
from models import models
import models

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.costumer_id == customer_id).first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer
    
def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(models.Customer).filter(models.Customer.costumer_id == customer_id).first()
    db.delete(db_customer)
    db.commit()

