from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.config.database import get_db
from db.models import models
from db.schemas import schema
from dependencies.hotel import Hotel, ManagementHotel
from dependencies.auth_utils import get_user_logged_in, validate_user_role


router = APIRouter()


#Get all data from Hotel
@router.get("/hotel_data", status_code=status.HTTP_200_OK)
def get_hotel_data( db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):

     # Valida o papel do usuário
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])

    # Administrador vê todos os hotéis
    if current_user.role.access_level == "Administrador":
        hotels = db.query(models.Hotel).all()

    # Gerente vê apenas o hotel associado
    elif current_user.role.access_level == "Gerente":
        hotels = db.query(models.Hotel).filter(models.Hotel.id == current_user.hotel_id).all()

    # Retorna os hotéis filtrados
    return hotels

#Post Hotel
@router.post('/create-hotel',  status_code=status.HTTP_201_CREATED)
def new_hotel(hotel: schema.HotelSchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in) ):

    validate_user_role(current_user, allowed_roles=['Administrador'])

    hotel_created = Hotel(db).create_hotel_in_db(hotel)
    return hotel_created


#Post ManagementHotel
@router.post('/management-hotel',  status_code=status.HTTP_201_CREATED)
def new_management_hotel(managmentHotel: schema.ManagementHotelSchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in) ):

    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])

    # Adicionar `hotel_id` ao managementhotel com base no papel do usuário
    if current_user.role.access_level == "Administrador":
        if not managmentHotel.hotel_id:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Administradores precisam informar o hotel_id.")
        hotel_id = managmentHotel.hotel_id

    # Gerente só pode criar para o hotel ao qual pertence
    elif current_user.role.access_level == "Gerente":
        hotel_id = current_user.hotel_id

   # Atualiza o hotel_id no objeto managmentHotel
    managmentHotel.hotel_id = hotel_id

    management_hotel_created = ManagementHotel(db).create_management_hotel_in_db(managmentHotel)
    return management_hotel_created

