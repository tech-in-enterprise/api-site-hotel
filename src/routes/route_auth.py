from fastapi import APIRouter, status, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from db.config.database import get_db
from db.schemas import schema
from dependencies.users import UserDependencies
from utils.providers import hash_provider, token_provider
from dependencies.auth_utils import get_user_logged_in, validate_user_role


router = APIRouter()

@router.post('/sign-up', status_code=status.HTTP_201_CREATED, response_model=schema.UserOutSchema)
def create_users( user: schema.UserSchema, role_id: int = Body(..., embed=True), hotel_id: int = Body(None, embed=True), session: Session = Depends(get_db),  current_user=Depends(get_user_logged_in)):

    validate_user_role(current_user, allowed_roles=['Administrador'])

    # Verifica a existência do usuário pelo e-mail
    find_user = UserDependencies(session).read_email(user.email)

    if find_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='E-mail já cadastrado')

    # Criptografa a senha do usuário
    user.password = hash_provider.create_hash(user.password)

    # Cria o usuário
    user_created = UserDependencies(session).create_user(user, role_id, hotel_id)

    return {
        "id": user_created.id,
        "name": user_created.user_name,
        "email": user_created.user_email,
        "role": {"access_level": user_created.role.access_level},
        "hotel_id": user_created.hotel_id
    }


@router.post('/sign-in')
def login(login_data: schema.LoginSchema, session: Session = Depends(get_db)):
    email = login_data.email
    password = login_data.password

    user = UserDependencies(session).read_email(email)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='E-mail incorreto ou não cadastrado')
    
    #se chegou aqui existe um usuário, agora vai ser verificado a senha 
    verify_password = hash_provider.verify_hash(password, user.user_password)

    if not verify_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Senha incorreta')
    

    #Gerar Token JWT
    token = token_provider.create_access_token({
        'sub': user.user_email,
        'role': user.role.access_level,
        'hotel_id': user.hotel_id
        })

    
    return {'user': user.user_name, 'access_token': token, 'role': user.role.access_level, 'hotel': user.hotel_id}
    
