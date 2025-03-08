from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import route_roles
from routes import route_auth
from routes import route_hotel
from routes import route_departments
from routes import route_services
from routes import route_users
from routes import route_amenities

#create_bd()

app = FastAPI()


# cors
origins = [
    'http://localhost:5173','*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(route_roles.router)
app.include_router(route_users.router)
app.include_router(route_auth.router)
app.include_router(route_hotel.router)
app.include_router(route_amenities.router)
app.include_router(route_departments.router)
app.include_router(route_services.router)