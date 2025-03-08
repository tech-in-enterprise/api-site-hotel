from sqlalchemy.orm import Session
from db.schemas import schema
from db.models import models




class Hotel():
    def __init__(self, db: Session) -> None:
        self.db = db
    

    #Post Hotels
    def create_hotel_in_db(self, hotel: schema.HotelSchema):
        db_hotel = models.Hotel(
            hotel_name = hotel.hotel_name.title(),
            registered_name = hotel.registered_name.title(),
            phone_number = hotel.phone_number,
            hotel_email = hotel.hotel_email,
            cnpj = hotel.cnpj,
            street_address = hotel.street_address,
            number_address =  hotel.number_address,
            city = hotel.city.title(),
            state = hotel.state.title(),
            cep = hotel.cep,
        )
        self.db.add(db_hotel)
        self.db.commit()
        self.db.refresh(db_hotel)
        return db_hotel
    


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