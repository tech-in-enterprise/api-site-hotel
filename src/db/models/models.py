from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float, Boolean, Time
from db.config.database import Base
from sqlalchemy.orm import relationship




class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    access_level = Column(String, unique=True, nullable=False)  # Ex.: Administrador, Gerente
    description_of_access_level = Column(String, nullable=True)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    user_email = Column(String, unique=True, nullable=False)
    user_password = Column(String)
    is_active = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey('roles.id'))
    hotel_id = Column(Integer, ForeignKey('hotels.id'))  # Relaciona o usuário ao hotel

    role = relationship('Role', back_populates='users')
    hotel = relationship('Hotel', back_populates='users')


class Hotel(Base):
    __tablename__ = 'hotels'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_name = Column(String, nullable=False)
    registered_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    hotel_email = Column(String,  nullable=False)
    cnpj = Column(String,  nullable=False)

    #address
    street_address = Column(String, nullable=False)
    number_address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    cep = Column(String, nullable=False)


    management_hotel = relationship('ManagementHotel', back_populates='hotel')
    amenities = relationship('Amenity', back_populates='hotel')
    rooms = relationship('Room', back_populates='hotel')
    departments = relationship('Department', back_populates='hotel')
    users = relationship('User', back_populates='hotel')  # Relaciona usuários com hotéis


class ManagementHotel(Base):
    __tablename__ = 'management_hotel'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_hotel_url = Column(String)

    #Redes sociais
    instagram_url = Column(String)
    facebook_url = Column(String)

    #Wi-fi
    wifi_network = Column(String)
    wifi_password = Column(String)

    #others numbers from hotel by patch
    reception_phone = Column(String)
    reservation_phone = Column(String)

    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    hotel = relationship('Hotel', back_populates='management_hotel')

class Amenity(Base):
    __tablename__ = 'amenities'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_amenity_url = Column(String)
    name = Column(String, nullable=False)    
    start_time = Column(String, nullable=False) 
    end_time = Column(String, nullable=False)    
    hotel_id = Column(Integer, ForeignKey('hotels.id'))  

    hotel = relationship('Hotel', back_populates='amenities')


class Guest(Base):
    __tablename__ = 'guests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone_number = Column(String)
    email_address = Column(String)
    room_id = Column(Integer, ForeignKey('rooms.id'))

    room = relationship('Room', back_populates='guests')
    requests = relationship("Request", back_populates='guest')

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_number = Column(String, nullable=False)
    status = Column(String)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))

    hotel = relationship('Hotel', back_populates='rooms')
    guests = relationship('Guest', back_populates='room')

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    start_time = Column(String, nullable=True) 
    end_time = Column(String, nullable=True)    
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    image_url = Column(String, nullable=False)

    hotel = relationship('Hotel', back_populates='departments')
    requests = relationship('Request', back_populates='department')
    service = relationship("Service", back_populates="department")

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float)
    department_id = Column(Integer, ForeignKey('departments.id')) 
    start_time = Column(Time, nullable=True)  
    end_time = Column(Time, nullable=True)    
    is_24_hours = Column(Boolean, default=False)  
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    image_url = Column(String, nullable=False)

    department = relationship("Department", back_populates="service") 


class Request(Base):
    __tablename__ = 'requests'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date_created = Column(String)
    date_updated = Column(String)
    status = Column(String)
    guest_id = Column(Integer, ForeignKey('guests.id'))
    department_id = Column(Integer, ForeignKey('departments.id'))

    guest = relationship("Guest", back_populates="requests")
    department = relationship("Department", back_populates="requests")

# Relacionamento bidirecional de roles e usuários
Role.users = relationship('User', back_populates='role')