from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Ali_wazir1@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()


# getting session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
