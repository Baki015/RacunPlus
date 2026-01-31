from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from RacunPlus.database import SessionLocal
from RacunPlus.settings import settings
from .models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import uuid

router = APIRouter(prefix='/auth', tags=['auth'])

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
bcrypt = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2 = OAuth2PasswordBearer(tokenUrl='auth/login')


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str):
    return bcrypt.hash(password)


def verify_password(plain: str, hashed: str):
    return bcrypt.verify(plain, hashed)


def create_token(username: str, user_id: str):
    encode = {'sub': username, 'id': str(user_id)}
    expires = datetime.now(timezone.utc) + timedelta(minutes=60)
    encode['exp'] = expires
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        if not username or not user_id:
            raise HTTPException(status_code=401, detail='Greska sa tokenom')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail='Greska sa tokenom')


@router.post('/register', status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail='Korisnik već postoji')

    new_user = User(
        id=uuid.uuid4(),
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(new_user)
    db.commit()
    
    return {'success': True, 'message': 'Korisnik je kreiran'}


@router.post('/login', response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == form.username).first()
    if not user:
        raise HTTPException(status_code=401, detail='Pogresno korisnicko ime ili lozinka')
    if not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Pogresno korisnicko ime ili lozinka')
    
    token = create_token(user.username, user.id)
    return {'access_token': token, 'token_type': 'bearer'}


@router.get('/current-user')
def get_user_info(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user['id']).first()
    if not user:
        raise HTTPException(status_code=404, detail='Korisnik nije pronađen')
    
    return {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
