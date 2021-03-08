# Third Party
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# Local
from config import SQLALCHEMY_DATABASE_URL

Base = declarative_base()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=300
)
_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# return session
def get_session():
    return _SessionLocal()

