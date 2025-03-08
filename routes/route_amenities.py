from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.config.database import get_db
from db.models import models
from db.schemas.schema import AmenitySchema
from dependencies.auth_utils import get_user_logged_in, validate_user_role

router = APIRouter()

@router.post('/amenities', status_code=status.HTTP_201_CREATED)
def add_new_amenity(amenity: AmenitySchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_user_logged_in)):

    #verificar papel do usuário
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])


    #verificar se o hotel existe
    hotel = db.query(models.Hotel).filter(models.Hotel.id == current_user.hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with ID {amenity.hotel_id} not found"
        )
    
    #Verificar se o gerente tem permissão para criar social medias
    if current_user.role.access_level == 'Gerente' and amenity.hotel_id != current_user.hotel_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create a amenity for this hotel"
        )
    

    #criar o link da socia media
    new_amenity = models.Amenity(
        name= amenity.name,
        start_time= amenity.start_time,
        end_time= amenity.end_time,
        hotel_id=current_user.hotel_id,
    )

    db.add(new_amenity)
    db.commit()
    db.refresh(new_amenity)


    return{"message": "Amenities created sucessfully", "Amenities": new_amenity} 