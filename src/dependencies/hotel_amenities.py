from sqlalchemy.orm import Session
from db.schemas import schema
from db.models import models



class Amenity():

    def __init__(self, db: Session) -> None:
        self.db = db

    #Post Dependencies
    def create_amenity_in_db(self, amenity: schema.AmenitySchema):
        db_amenity = models.Amenity(
            image_amenity_url=amenity.image_amenity_url,
            name=amenity.name.title(),
            start_time=amenity.start_time,
            end_time=amenity.end_time,
            hotel_id=amenity.hotel_id
        )
        self.db.add(db_amenity)
        self.db.commit()
        self.db.refresh(db_amenity)
        return db_amenity

