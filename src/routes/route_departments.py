from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.config.database import get_db
from db.models import models
from db.schemas import schema
from dependencies.derpartment import Departments
from dependencies.auth_utils import get_user_logged_in, validate_user_role


router = APIRouter()




# Get all departments
@router.get("/departments", status_code=status.HTTP_200_OK)
def get_departments(db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):

    # Valida o papel do usuário
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])

    # Administrador vê todos os hotéis
    if current_user.role.access_level == "Administrador":
        departments = db.query(models.Department).all()
    
    # Gerente vê apenas o departamento associado
    elif current_user.role.access_level == "Gerente":
        departments = db.query(models.Department).filter(models.Department.hotel_id == current_user.hotel_id).all()
    
    return departments


# Post Department from hotel
@router.post('/departments', status_code=status.HTTP_201_CREATED)
def add_department(department: schema.DepartmentSchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):

    # Validar papel do usuário
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])

    # Adicionar `hotel_id` ao departamento com base no papel do usuário
    if current_user.role.access_level == "Administrador":
        if not department.hotel_id:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Administradores precisam informar o hotel_id para criar um departamento.")
        hotel_id = department.hotel_id

    # Gerente só pode criar para o hotel ao qual pertence
    elif current_user.role.access_level == "Gerente":
        hotel_id = current_user.hotel_id

   # Atualiza o hotel_id no objeto department
    department.hotel_id = hotel_id

    department_created = Departments(db).create_department_in_db(department)
    return department_created


from fastapi import Body


# Update Department
@router.put('/departments/{department_id}', status_code=status.HTTP_200_OK)
def update_department( department_id: int, department_update: schema.UpdateDepartmentSchema = Body(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):
    
    # Validar o papel do usuário
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])

    # Buscar o departamento
    department_db = db.query(models.Department).filter(models.Department.id == department_id).first()

    if not department_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Departamento não encontrado.")

    # Verificar permissão para gerentes
    if current_user.role.access_level == "Gerente":
        if department_db.hotel_id != current_user.hotel_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para editar este departamento.")
        department_update.hotel_id = current_user.hotel_id  # Garante que o gerente não troque o hotel_id

    # Se for administrador, usa o hotel_id informado (ou mantém o atual)
    elif current_user.role.access_level == "Administrador":
        department_update.hotel_id = department_update.hotel_id or department_db.hotel_id

    # Atualiza
    updated_department = Departments(db).update_department(department_id, department_update)

    return updated_department



# Delete Department from hotel
@router.delete('/departments/{department_id}', status_code=status.HTTP_200_OK)
def remove_department(department_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):
    # Validar o papel do usuário
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])

    # Verificar se o departamento pertence ao escopo do usuário
    department = db.query(models.Department).filter(models.Department.id == department_id).first()

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Departamento não encontrado.")
    

    # Gerente só pode deletar departamentos associados ao seu hotel
    elif current_user.role.access_level == "Gerente":
        if department.hotel_id != current_user.hotel_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para deletar este departamento.")

    # Deletar o departamento
    Departments(db).destroy_department(department_id)
    return {'message': 'Removido com sucesso'}