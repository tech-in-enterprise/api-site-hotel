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
    


