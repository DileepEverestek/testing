import jwt
import uvicorn
from fastapi import Depends, FastAPI,status , HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import src.core.security
from src.core.hashing import Hasher
from src.core.security import settings, create_access_token, decode_token
from src.exceptions import exceptions
from src.models import models
from sqlalchemy.orm import Session
from src.models.users import User
from src.database.database import SessionLocal, engine
from src.schemas.schemas import Refresh_Token, Token, create_new_user, Del_Token
from src.utils import exceptions as e
from src.core.security import decode_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#registration

#registration
@app.post("/")
def create_user(request : create_new_user,db: Session = Depends(get_db)):
    query1 = db.query(User).filter(User.email == request.email).first()
    if not query1:
        query = User(
            username= request.username,
            email=request.email,
            user_role = request.user_role,
            hashed_password=Hasher.get_password_hash(request.hashed_password)
        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return {"Details": "Account Created"}

    else:
        return {"Details:" "Email already exists"}



#login


def get_user(username:str,db: Session):
    user = db.query(User).filter(User.email == username).first()
    return user


def authenticate_user(username: str, password: str,db: Session):
    user = get_user(username=username,db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session= Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(seconds=15)
    #refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    print(access_token)
    refresh_token = src.core.security.encode_refresh_token(user.email)
    print(refresh_token)
    #refresh_token = create_refresh_token(data={"sub":user.email}, expires_delta= refresh_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "refresh_token":refresh_token}

## adding refresh
@app.get("/refresh_token")
def refresh_token(re_token: str ):
    refresh_token1 = src.core.security.refresh_token(re_token)
    access_token = src.core.security.access_token_extend(re_token)
    return {"refresh_token": refresh_token1,"token_type": "bearer", "access_token": access_token}

@app.get("/log-out", response_model= Del_Token)
async def logout(token: str):
    token = src.core.security.delete_token(token)
    return {"token_response" : "token deleted"}

@app.get("/validate_token")
async def validate_token(access_token: str ):
    try:
        payload = decode_token(
            access_token, settings.SECRET_KEY, settings.ALGORITHM, verify=True
        )
        print(payload['sub'])
        return payload['sub']
    except Exception as e:
        print(type(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)