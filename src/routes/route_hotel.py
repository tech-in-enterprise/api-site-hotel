from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.config.database import get_db
from db.models import models
from db.schemas import schema
from dependencies.hotel import Hotel, HotelRepository
from dependencies.auth_utils import get_user_logged_in


router = APIRouter()


#Get all data from Hotel
@router.get("/hotel_data", status_code=status.HTTP_200_OK)
def get_hotel_data( db: Session = Depends(get_db)): # current_user: schema.UserSchema = Depends(get_user_logged_in)  ):
    hotel = db.query(models.Hotel).all()
    return hotel

#Post Hotel
@router.post('/create-hotel',  status_code=status.HTTP_201_CREATED)
def new_hotel(hotel: schema.HotelSchema, db: Session = Depends(get_db)):
    hotel_created = Hotel(db).create_hotel_in_db(hotel)
    return hotel_created

#Patch Hotel Amenities
@router.patch('/update-amenities-hotel/{hotel_id}', status_code=status.HTTP_201_CREATED)
def update_hotel_amenities(hotel_id: int, data: schema.HotelAdditionalDataSchema, db: Session = Depends(get_db)):
    # Instancia o repositório do hotel
    hotel_repo = HotelRepository(db)

    # Atualiza o hotel no banco de dados
    updated_hotel = hotel_repo.update_hotel_in_db(hotel_id, data)

    # Caso o hotel não seja encontrado
    if not updated_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    return updated_hotel