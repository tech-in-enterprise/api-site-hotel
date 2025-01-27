from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.config.database import get_db
from dependencies.users import UserDependencies
from db.schemas import schema
from db.models import models
from dependencies.auth_utils import get_user_logged_in, validate_user_role
from typing import List, Optional


router = APIRouter()


# Função para mapear os dados do hotel
def map_hotel_data(hotel) -> Optional[dict]:
    if not hotel:
        return None
    return {
        "id": hotel.id,
        "hotel_name": hotel.hotel_name,
        "registered_name": hotel.registered_name,
        "phone_number": hotel.phone_number,
        "hotel_email": hotel.hotel_email,
        "cnpj": hotel.cnpj,
        "street_address": hotel.street_address,
        "number_address": hotel.number_address,
        "city": hotel.city,
        "state": hotel.state,
        "cep": hotel.cep,
    }

# Função para mapear os dados do usuário
def map_user_data(user) -> dict:
    return {
        "id": user.id,
        "name": user.user_name,
        "email": user.user_email,
        "role": {
            "access_level": user.role.access_level,
            "description_of_access_level": user.role.description_of_access_level,
        },
        "hotel": map_hotel_data(user.hotel),
        "hotel_id": user.hotel_id,
    }

# Rota para obter todos os usuários
@router.get("/users", response_model=List[schema.UserOutSchema])
def get_all_users( session: Session = Depends(get_db), current_user: schema.UserOutSchema = Depends(get_user_logged_in)):
    # Validar o papel do usuário
    validate_user_role(current_user, allowed_roles=["Administrador", "Gerente"])

    # Obter os usuários do banco de dados
    users = UserDependencies(session).read_user(current_user)

    # Mapear os dados dos usuários
    users_out = [map_user_data(user) for user in users]

    return users_out



@router.patch("/users", response_model=schema.UserOutSchema)
def assign_hotel_to_user( hotel_id: int, session: Session = Depends(get_db), current_user: schema.UserOutSchema = Depends(get_user_logged_in)):

    # Validar o papel do usuário atual
    validate_user_role(current_user, allowed_roles=["Administrador", "Gerente"])

    # Obter o usuário pelo ID
    user = session.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # Validar se o hotel existe
    hotel = session.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel não encontrado.")

    # Verificar se o usuário já possui um hotel associado
    if user.hotel_id is not None:
        raise HTTPException(status_code=400, detail="Usuário já possui um hotel associado.")

    # Atualizar o hotel_id do usuário
    user.hotel_id = hotel.id
    session.commit()
    session.refresh(user)

    # Retornar o usuário atualizado
    return schema.UserOutSchema(
        id=user.id,
        name=user.user_name,
        email=user.user_email,
        role={
            "access_level": user.role.access_level,
            "description_of_access_level": user.role.description_of_access_level,
        },
        hotel={
            "id": hotel.id,
            "hotel_name": hotel.hotel_name,
            "registered_name": hotel.registered_name,
            "phone_number": hotel.phone_number,
            "hotel_email": hotel.hotel_email,
            "cnpj": hotel.cnpj,
            "street_address": hotel.street_address,
            "number_address": hotel.number_address,
            "city": hotel.city,
            "state": hotel.state,
            "cep": hotel.cep,
        },
        hotel_id=user.hotel_id,
    )



@router.patch("/users/remove-hotel", response_model=schema.UserOutSchema)
def remove_hotel_from_user( session: Session = Depends(get_db), current_user: schema.UserOutSchema = Depends(get_user_logged_in)):

    # Obter o usuário logado
    user = session.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # Verificar se o usuário tem um hotel associado
    if user.hotel_id is None:
        raise HTTPException(status_code=400, detail="Usuário não possui um hotel associado.")

    # Remover a associação do hotel
    user.hotel_id = None
    session.commit()
    session.refresh(user)

    # Retornar o usuário atualizado
    return schema.UserOutSchema(
        id=user.id,
        name=user.user_name,
        email=user.user_email,
        role={
            "access_level": user.role.access_level,
            "description_of_access_level": user.role.description_of_access_level,
        },
        hotel=None,  # Hotel removido
        hotel_id=user.hotel_id,
    )
