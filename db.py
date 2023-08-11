from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#database url
import os

# # Retrieve the database URL and other sensitive information from environment variables
# DB_HOST = 'localhost'  # Update with your actual database host
# DB_PORT = 3306  # Update with your actual database port
# DB_USER = 'muz_xayrullo'  # Update with your actual database username
# DB_PASSWORD = 'Xayrullo98'  # Update with your actual database password
# DB_NAME = 'muz_baza'  # Update with your actual database name
#
# # Construct the SQLAlchemy database URL
# SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SQLALCHEMY_DATABASE_URL = 'sqlite:///'+os.path.join(BASE_DIR,'bazza.db?check_same_thread=False')
SECRET_KEY = 'SOME-SECRET-KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=300)


'$2b$12$HGh59BB/0Z6XvTOtCFFgmuxKOJ7wobyg3feVVYOjmShRbqnVx75UK'
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()