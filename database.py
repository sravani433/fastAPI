from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine
engine = create_engine("postgresql://postgres:kpss%401341@localhost/postgres",echo=True)

Base= declarative_base()
SessionLocal=sessionmaker(bind=engine)

# #database.py
# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker
# import os

# # DATABASE_URL = "postgresql://postgres:kpss%401341@db/User"
# DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_engine(DATABASE_URL, echo=True)
# Base = declarative_base()
# SessionLocal = sessionmaker(bind=engine)
