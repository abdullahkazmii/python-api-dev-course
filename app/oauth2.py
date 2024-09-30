from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app import schemas, models, database
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status
from fastapi.security import  OAuth2PasswordBearer
from typing import Any
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        # print("LOG==> id:",id, type(id))

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = str(id))
        print("LOG===> token_data",token_data)
    except JWTError:
        print("LOG===> JWTError",JWTError)
        raise credentials_exception

    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> Any | None:
    print("LOG===> get_current_user",token)
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Could not Validate Credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first() #type: ignore
    return user