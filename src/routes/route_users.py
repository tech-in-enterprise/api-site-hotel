from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.config.database import get_db
from dependencies.users import UserDependencies
from db.schemas import schema
from dependencies.auth_utils import get_user_logged_in, validate_user_role

router = APIRouter()

# Rota para obter todos os usuários
@router.get("/users")
def get_all_users( session: Session = Depends(get_db),  current_user: schema.UserOutSchema = Depends(get_user_logged_in) ):
    validate_user_role(current_user, allowed_roles=['Administrador', 'Gerente'])
    users = UserDependencies(session).read_user()
    return users
