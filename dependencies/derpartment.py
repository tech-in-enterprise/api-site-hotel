from sqlalchemy.orm import Session
from sqlalchemy import delete
from db.schemas import schema
from db.models import models



class Departments():

    def __init__(self, db: Session) -> None:
        self.db = db


    #Post Dependencies
    def create_department_in_db(self, department_data: dict):
        if "name" in department_data:
            department_data["name"] = department_data["name"].title()
            
        new_department = models.Department(**department_data)
        self.db.add(new_department)
        self.db.commit()
        self.db.refresh(new_department)
        return new_department
    
    #Delete dependencies
    def destroy_department(self, department_id: int):
        self.db.query(models.Department).filter(models.Department.id == department_id).delete()

        self.db.commit()