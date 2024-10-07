# controllers.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import SessionLocal
from services import UserService
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import RegisteredUserCreate, RegisteredUserResponse, User
from auth import verify_access_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    service = UserService(db)
    if service.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been logged out")
    
    username = verify_access_token(token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return username

@router.post('/register', response_model=RegisteredUserResponse, status_code=status.HTTP_200_OK)
def register_user(Ruser: RegisteredUserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    new_user = service.register_user(Ruser)
    return new_user
# @router.post('/register', response_model=RegisteredUserResponse, status_code=status.HTTP_200_OK)
# async def register_user(Ruser: RegisteredUserCreate, db: Session = Depends(get_db)):
#     service = UserService(db)
#     new_user = await service.register_user(Ruser)
    
#     # You could capture the notification response and decide how to proceed
#     notification_result = await service.notify_user(new_user.id, "Welcome to the platform!")
#     if "error" in notification_result:
#         # Return a custom warning but don't block user registration
#         return {"user": new_user, "warning": "User registered, but notification failed"}

#     return new_user


@router.get('/registeredusers', response_model=list[RegisteredUserResponse])
def get_all_registered_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_all_registered_users()

@router.post('/login', response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = UserService(db)
    token = service.login(form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

@router.post('/logout', status_code=status.HTTP_200_OK)
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    service = UserService(db)
    service.logout(token)
    return {"message": "Successfully logged out"}

@router.get('/getallusers', response_model=list[User], status_code=status.HTTP_200_OK)
def get_all_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    authenticate_user(token, db)
    service = UserService(db)
    return service.get_all_users()

@router.post('/adduser', response_model=User, status_code=status.HTTP_201_CREATED)
def add_user(user: User, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    authenticate_user(token, db)
    service = UserService(db)
    new_user = service.add_user(user)
    if not new_user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="User with this id already exists")
    return new_user

@router.put('/updateuser/{user_id}', response_model=User, status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id: int, user: User, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    authenticate_user(token, db)
    service = UserService(db)
    updated_user = service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user

@router.delete('/deleteuser/{user_id}', response_model=User, status_code=200)
def delete_user(user_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    authenticate_user(token, db)
    service = UserService(db)
    deleted_user = service.delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return deleted_user

@router.get('/getbyid/{user_id}', response_model=User, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
