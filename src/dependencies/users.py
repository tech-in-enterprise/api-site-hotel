from fastapi import  HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from db.schemas import schema
from db.models import models


class UserDependencies():
    def __init__(self, session: Session):
        self.session = session

    def read_user(self):
        statement = select(models.User).options(joinedload(models.User.role))
        users = self.session.execute(statement).scalars().all()
        
        return users

    def read_email(self, email):
        query = select(models.User).where(models.User.user_email == email)
        return self.session.execute(query).scalars().first()
    
    def create_user(self, user: schema.UserSchema, role_id: int, hotel_id: int = None):
        if role_id == 1:   # Usuários administradores não estão vinculados a um único hotel
            hotel_id = None
        elif not hotel_id:
            raise HTTPException(status_code=400, detail="Hotel ID é obrigatório para não administradores")

        user_bd = models.User(
            user_name=user.name,
            user_email=user.email,
            user_password=user.password,
            role_id=role_id,
            hotel_id=hotel_id,
        )
        try:
            self.session.add(user_bd)
            self.session.commit()
            self.session.refresh(user_bd)
        except IntegrityError as e:
        # Captura erros de integridade, como violação de chave estrangeira
            raise HTTPException(status_code=400, detail="Hotel ID não existe ou é inválido.")
        return user_bd