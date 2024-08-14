import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_NAME = os.getenv('DB_NAME')

DB_CONN = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

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
