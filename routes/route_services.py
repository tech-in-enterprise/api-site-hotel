from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.config.database import get_db
from db.models import models
from db.schemas.schema import ServiceSchema
from dependencies.services import Services
from dependencies.auth_utils import get_user_logged_in, validate_user_role



router = APIRouter()


#get a respective service by department
@router.get('/services', status_code = status.HTTP_200_OK)
def get_services(db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):

    #verificar o papel do usuário
    validate_user_role(current_user, allowed_roles= ['Administrador', 'Gerente'])

    #Admin consegue ver todos os serviçõs criados
    if current_user.role.access_level == 'Administrador':
        services = db.query(models.Service).all()

    elif current_user.role.access_level == 'Gerente':
        services = (
            db.query(models.Service)
            .join(models.Department, models.Service.department_id == models.Department.id)
            .filter(models.Department.hotel_id == current_user.hotel_id)
            .all()
        )

    return services


#Create a respective service from department
@router.post('/services', status_code=status.HTTP_201_CREATED)
def add_new_service(service: ServiceSchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):

    # Verificar o papel do usuário
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])

    # Verificar se o departamento existe
    department = db.query(models.Department).filter(models.Department.id == service.department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with ID {service.department_id} not found."
        )

    # Verificar se o gerente tem permissão para criar serviços no departamento
    if current_user.role.access_level == 'Gerente' and department.hotel_id != current_user.hotel_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create a service for this department."
        )

    # Criar o novo serviço
    new_service = models.Service(
        name=service.name.title(),
        price=service.price,
        department_id=service.department_id,
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return {"message": "Service created successfully", "service": new_service}
