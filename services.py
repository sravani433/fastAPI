# services.py
from typing import Set
from sqlalchemy.orm import Session
import models
import bcrypt
from auth import create_access_token
from schemas import RegisteredUserCreate, RegisteredUserResponse, User
import httpx

class UserService:
    def __init__(self, db: Session):
        self.db = db

    # In-memory set to store blacklisted tokens
    blacklisted_tokens: Set[str] = set()

    async def notify_user(self, user_id: int, message: str):
        """
        Send an HTTP request to the notification service to send a notification.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "http://localhost:8001/send-notification",  # Notification service URL
                    json={"user_id": user_id, "message": message}
                )
                response.raise_for_status()
                print(f"Notification sent successfully for user_id {user_id}")
                return response.json()
            except httpx.RequestError as exc:
                print(f"Failed to send notification: {exc}")
                return {"error": "Failed to send notification"}

    # async def register_user(self, Ruser: RegisteredUserCreate) -> dict:
    #     hashed_password = bcrypt.hashpw(Ruser.password.encode('utf-8'), bcrypt.gensalt())
    #     new_user = models.RegisteredUser(
    #         name=Ruser.name,
    #         hashed_password=hashed_password.decode('utf-8')
    #     )
    #     self.db.add(new_user)
    #     self.db.commit()
    #     self.db.refresh(new_user)

    #     try:
    #         # Notify user
    #         notification_response = await self.notify_user(new_user.id, "Welcome to the platform!")
    #     except Exception as e:
    #         print(f"Notification failed: {str(e)}")
    #         notification_response = {"error": str(e)}

    #     return {"user": new_user, "notification": notification_response}


    

    def register_user(self, Ruser: RegisteredUserCreate) -> RegisteredUserResponse:
        hashed_password = bcrypt.hashpw(Ruser.password.encode('utf-8'), bcrypt.gensalt())
        new_user = models.RegisteredUser(
            name=Ruser.name,
            hashed_password=hashed_password.decode('utf-8')
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_all_registered_users(self) -> list[RegisteredUserResponse]:
        return self.db.query(models.RegisteredUser).all()

    def login(self, username: str, password: str) -> str:
        user = self.db.query(models.RegisteredUser).filter(models.RegisteredUser.name == username).first()
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            return None
        return create_access_token(data={"sub": user.name})

    def logout(self, token: str):
        # Add the token to the blacklist
        self.blacklisted_tokens.add(token)

    def is_token_blacklisted(self, token: str) -> bool:
        return token in self.blacklisted_tokens

    def get_all_users(self) -> list[User]:
        return self.db.query(models.User).all()

    def add_user(self, user: User) -> User:
        new_user = models.User(
            id=user.id,
            name=user.name,
            city=user.city,
            isMale=user.isMale
        )
        existing_user = self.db.query(models.User).filter(models.User.id == user.id).first()
        if existing_user:
            return None
        self.db.add(new_user)
        self.db.commit()
        return new_user

    def update_user(self, user_id: int, user: User) -> User:
        existing_user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if not existing_user:
            return None
        existing_user.name = user.name
        existing_user.city = user.city
        existing_user.isMale = user.isMale
        self.db.commit()
        return existing_user

    def delete_user(self, user_id: int) -> User:
        existing_user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if not existing_user:
            return None
        self.db.delete(existing_user)
        self.db.commit()
        return existing_user

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(models.User).filter(models.User.id == user_id).first()
