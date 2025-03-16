from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.schemas import schema
from db.models import models



#Management Hotel
class ManagementHotel():

    def __init__(self, db: Session) -> None:
        self.db = db

    #Post Management Hotel
    def create_management_hotel_in_db(self, managementHotel: schema.ManagementHotelSchema):
        db_management_hotel = models.ManagementHotel(
            image_hotel_url = managementHotel.image_hotel_url,
            instagram_url = managementHotel.instagram_url,
            facebook_url = managementHotel.facebook_url,
            wifi_network = managementHotel.wifi_network,
            wifi_password = managementHotel.wifi_password,
            reception_phone = managementHotel.reception_phone,
            reservation_phone = managementHotel.reservation_phone,
            hotel_id = managementHotel.hotel_id
        )
        self.db.add(db_management_hotel)
        self.db.commit()
        self.db.refresh(db_management_hotel)
        return db_management_hotel
    

  