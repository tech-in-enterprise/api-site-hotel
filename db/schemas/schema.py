from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime



class RoleSchema(BaseModel):
    access_level: str
    description_of_access_level: Optional[str] = None
    
    class Config:   
        orm_mode = True


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:   
        orm_mode = True

# Schema de entrada (o que o cliente envia)
class UserSchema(BaseModel):
    name: str
    email: str
    password: str

class HotelSchema(BaseModel):
    hotel_name: str
    registered_name: str
    phone_number: str
    hotel_email: str
    cnpj: str

    # Endereço
    street_address: str
    number_address: str
    city: str
    state: str
    cep: str

    class Config:
        orm_mode = True

# Schema de saída (o que o cliente recebe)
class UserOutSchema(BaseModel):
    id: int
    name: str
    email: str
    role: RoleSchema 
    hotel: Optional[HotelSchema] = None 
    hotel_id: Optional[int]

    class Config:
        orm_mode = True


class ManagementHotelSchema(BaseModel):
    id: Optional[int] = None
    image_hotel_url: str
    instagram_url: str
    facebook_url: str
    wifi_network: Optional[str]
    wifi_password: Optional[str]
    reception_phone: Optional[str] = None
    reservation_phone: Optional[str] = None
    hotel_id: int

    class Config:
        orm_mode = True

class AmenitySchema(BaseModel):
    id: Optional[int] = None
    name: str
    start_time: str
    end_time: str
    hotel_id: int

    class Config:
        orm_mode = True

class DepartmentSchema(BaseModel):
    id: Optional[int] = None
    name: str
    image_url: str
    start_time: str
    end_time: str
    hotel_id: int

    class Config:
        orm_mode = True


class ServiceSchema(BaseModel):
    name: str
    price: Optional[float] = None
    department_id: int
    hotel_id: int

    class Config:
        orm_mode = True