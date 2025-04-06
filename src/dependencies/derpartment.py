from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import delete
from db.schemas import schema
from db.models import models



class Departments():

    def __init__(self, db: Session) -> None:
        self.db = db


    #Post Dependencies
    def create_department_in_db(self, department: schema.DepartmentSchema):
        db_department = models.Department(
            name=department.name.title(),
            image_url=department.image_url,
            start_time=department.start_time,
            end_time=department.end_time,
            hotel_id=department.hotel_id
        )
        self.db.add(db_department)
        self.db.commit()
        self.db.refresh(db_department)
        return db_department
    
    #update departments
    def update_department(self, department_id: int, updated_data: schema.UpdateDepartmentSchema):
        department = self.db.query(models.Department).filter(models.Department.id == department_id).first()

        if not department:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Departamento não encontrado.")

        department.name = updated_data.name
        department.start_time = updated_data.start_time
        department.end_time = updated_data.end_time
        department.image_url = updated_data.image_url
        department.hotel_id = updated_data.hotel_id

        self.db.commit()
        self.db.refresh(department)

        return department



    #Delete dependencies
    def destroy_department(self, department_id: int):
        self.db.query(models.Department).filter(models.Department.id == department_id).delete()

        self.db.commit()


