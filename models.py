from sqlalchemy import String, Integer, Column, Boolean,DateTime
from database import Base, engine
from datetime import datetime
import bcrypt
def create_tables():
    Base.metadata.create_all(engine)
class User(Base):
    __tablename__='User'
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    city=Column(String,nullable=False)
    isMale=Column(Boolean)

class RegisteredUser(Base):
    __tablename__ = 'registereduser'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    last_accessed=Column(DateTime, default=None)

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))