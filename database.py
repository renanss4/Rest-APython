from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)