import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from tenacity import retry, stop_after_attempt, wait_fixed

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_PORT = os.environ.get('DB_PORT')

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

#SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

"""
@retry(stop=stop_after_attempt(10), wait=wait_fixed(5))
def create_engine_with_retry(db_url):
    return create_engine(db_url, echo=True)




@retry(stop=stop_after_attempt(10), wait=wait_fixed(5))
def create_all_with_retry(engine):
    Base.metadata.create_all(bind=engine)

create_all_with_retry(engine)
"""