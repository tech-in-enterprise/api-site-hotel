from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.config.database import get_db
from db.models import models
from db.schemas import schema
from dependencies.hotel_amenities import Amenity
from dependencies.auth_utils import get_user_logged_in, validate_user_role


router = APIRouter()

# Get all departments
@router.get("/amenities-hotel", status_code=status.HTTP_200_OK)
def get_amenities(db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):

    # Valida o papel do usuário
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])

    # Administrador vê todos os hotéis
    if current_user.role.access_level == "Administrador":
        amenities = db.query(models.Amenity).all()
    
    # Gerente vê apenas o departamento associado
    elif current_user.role.access_level == "Gerente":
        amenities = db.query(models.Amenity).filter(models.Amenity.hotel_id == current_user.hotel_id).all()
    
    return amenities

# Post Department from hotel
@router.post('/amenities-hotel', status_code=status.HTTP_201_CREATED)
def add_amenity(amenity: schema.AmenitySchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):

    # Validar papel do usuário
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])

    # Adicionar `hotel_id` ao departamento com base no papel do usuário
    if current_user.role.access_level == "Administrador":
        if not amenity.hotel_id:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Administradores precisam informar o hotel_id para criar uma amenidade do hotel.")
        hotel_id = amenity.hotel_id

    # Gerente só pode criar para o hotel ao qual pertence
    elif current_user.role.access_level == "Gerente":
        hotel_id = current_user.hotel_id

   # Atualiza o hotel_id no objeto comodities
    amenity.hotel_id = hotel_id

    amenities_created = Amenity(db).create_amenity_in_db(amenity)
    return amenities_created


# Put ManagementHotel
@router.put("/amenities-hotel", status_code=status.HTTP_200_OK)
def update_amenity_hotel( updated_amenity_hotel: schema.AmenitySchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):
    
    # Valida o papel do usuário
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])

    # Busca o ManagementHotel no banco
    db_amenity_hotel = db.query(models.Amenity).filter(
        models.Amenity.id == updated_amenity_hotel.id,
        models.Amenity.hotel_id == current_user.hotel_id
    ).first()

    if not db_amenity_hotel:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Amenity não encontrado.")

    # Restrição para Gerente: só pode atualizar o hotel associado ao usuário
    if current_user.role.access_level == "Gerente" and db_amenity_hotel.hotel_id != current_user.hotel_id:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Gerentes só podem atualizar a Amenidade do seu hotel.")

    # Atualiza os campos permitidos
    db_amenity_hotel.name = updated_amenity_hotel.name
    db_amenity_hotel.start_time = updated_amenity_hotel.start_time
    db_amenity_hotel.end_time = updated_amenity_hotel.end_time
    db_amenity_hotel.image_amenity_url = updated_amenity_hotel.image_amenity_url

    # Commit no banco de dados
    db.commit()
    db.refresh(db_amenity_hotel)

    return db_amenity_hotel


# Delete Amenity from hotel
@router.delete('/amenities-hotel/{amenity_id}', status_code=status.HTTP_200_OK)
def remove_amenity(amenity_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):

    # Valida o papel do usuário
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])

    # Busca a amenidade no banco
    amenity = db.query(models.Amenity).filter(models.Amenity.id == amenity_id).first()

    if not amenity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Amenidade não encontrada.")

    # Gerente só pode deletar amenidades do seu hotel
    if current_user.role.access_level == "Gerente" and amenity.hotel_id != current_user.hotel_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para deletar esta amenidade.")

    # Deleta a amenidade
    db.delete(amenity)
    db.commit()

    return {"message": "Amenidade removida com sucesso"}
