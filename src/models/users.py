import bcrypt

from src.core.hashing import Hasher
from src.models.models import User
from src.schemas.schemas import create_new_user
from sqlalchemy.orm import Session



def create_user(request: create_new_user, db: Session):
    query1 = db.query(User).filter(User.email == request.email).first()
    if not query1:
        query = User.user(
            email=request.email,
            hashed_password = request.hashed_password,
        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return {"Details": "Account Created"}

    else:
        return {"Details:" "Email already exists"}




def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user
