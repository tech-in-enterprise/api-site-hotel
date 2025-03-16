from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.config.database import get_db
from db.models import models
from db.schemas import schema
from dependencies.profile_hotel import ManagementHotel
from dependencies.auth_utils import get_user_logged_in, validate_user_role


router = APIRouter()


#Get ManagementHotel
@router.get("/management-hotel", status_code=status.HTTP_200_OK)
def get_profile_hotel_data( db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):

     # Valida o papel do usuário
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])

    # Administrador vê todos os hotéis
    if current_user.role.access_level == "Administrador":
        profile_hotel = db.query(models.ManagementHotel).all()

    # Gerente vê apenas o hotel associado
    elif current_user.role.access_level == "Gerente":
        profile_hotel = db.query(models.ManagementHotel).filter(models.ManagementHotel.hotel_id == current_user.hotel_id).all()
    
    # Retorna os hotéis filtrados
    return profile_hotel

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


# Put ManagementHotel
@router.put("/management-hotel", status_code=status.HTTP_200_OK)
def update_management_hotel( updated_management_hotel: schema.ManagementHotelSchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):
    
    # Valida o papel do usuário
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])

    # Busca o ManagementHotel no banco
    db_management_hotel = db.query(models.ManagementHotel).filter(models.ManagementHotel.hotel_id == current_user.hotel_id).first()

    if not db_management_hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ManagementHotel não encontrado."
        )

    # Restrição para Gerente: só pode atualizar o hotel associado ao usuário
    if current_user.role.access_level == "Gerente" and db_management_hotel.hotel_id != current_user.hotel_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Gerentes só podem atualizar o hotel ao qual estão associados."
        )

    # Atualiza os campos permitidos
    db_management_hotel.image_hotel_url = updated_management_hotel.image_hotel_url
    db_management_hotel.instagram_url = updated_management_hotel.instagram_url
    db_management_hotel.facebook_url = updated_management_hotel.facebook_url
    db_management_hotel.wifi_network = updated_management_hotel.wifi_network
    db_management_hotel.wifi_password = updated_management_hotel.wifi_password
    db_management_hotel.reception_phone = updated_management_hotel.reception_phone
    db_management_hotel.reservation_phone = updated_management_hotel.reservation_phone

    # Commit no banco de dados
    db.commit()
    db.refresh(db_management_hotel)

    return db_management_hotel
