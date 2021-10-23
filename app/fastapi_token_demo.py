from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from passlib.context import CryptContext

from pydantic import BaseModel

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# to get a string like this run in linux:
# openssl rand -hex 32
SECRET_KEY = "c4af8692b37bcf2d575c5958254eee21a049cf01925207beb8e4f02a5c0c9593"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# secret01
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$X8w2pubd67dP8JsAijamkejzK1LIiY.JMTh7qAgscb9TVkSHkT0sy",
        "disabled": False,
    }
}

class Test01_data_model(BaseModel):
    infor: Optional[str] = None

class Test02_data_model(BaseModel):
    username: str
    MFAtoken: str
    addtion: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# state this url-"\token" is used for get token only
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()



def verify_password(plain_password, hashed_password):

    return pwd_context.verify(plain_password, hashed_password)



# used for generating hash_password by plain_password
def get_password_hash(password):

    return pwd_context.hash(password)



def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)



def authenticate_user(fake_db, username: str, password: str):

    user = get_user(fake_db, username)

    if not user:

        return False

    if not verify_password(password, user.hashed_password): # the former password is a plain,yes!!

        return False

    return user



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    '''
    this function is used for verifying the token's expire time and get the user's infor
    '''
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        '''
        # A token can be decode to be as the data was encoded before
        if the token has expired then it can not be decode and raise a 
        'ExpiredSignatureError('Signature has expired.')' error.
        payload = {'sub': 'johndoe', 'exp': 1634789405}
        '''
        print(payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception as e:
        print(repr(e))
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user




@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/test01/", response_model=Test01_data_model, dependencies=[Depends(get_current_active_user)])
async def test01_app():
    return {"infor": "tokenttttttttt" }


@app.post("/test02/", dependencies=[Depends(get_current_active_user)])
async def test02_app(user_infor: Test02_data_model = Body(...)):
    print(user_infor.dict())
    return {"infor": user_infor }


if __name__ == '__main__':
    pass
    #import uvicorn
    #uvicorn.run(app='fastapi_token_demo:app', host="127.0.0.1", port=8000, reload=True, debug=True)
    #python -m uvicorn fastapi_token_demo:app --host '127.0.0.1' --port 8000 --reload