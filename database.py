import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from config import conf

DB_PASSWORD = conf['dbpassword']
DB_HOST = conf['dbhost']
DB_USER = conf['dbuser']
DB_NAME = conf['dbname']


DB_CONN= f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

class SQLAlchemy():
    def __init__(self):
        self.engine = create_engine(DB_CONN, pool_pre_ping=True, pool_size=20, max_overflow=0, pool_recycle=3600, connect_args={'connect_timeout': 10})
        self.Session = scoped_session(sessionmaker(bind=self.engine, autoflush=False, autocommit=False))

    def get_session(self):
        db = self.Session()
        try:
            yield db
        finally:
            db.close()

db = SQLAlchemy()
Base = declarative_base()
