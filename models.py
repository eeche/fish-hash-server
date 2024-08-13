from sqlalchemy import Column, DateTime, Integer, String ,TIMESTAMP
from database import Base

class Access_Table(Base):
    __tablename__ = 'access_table'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    channel_id = Column(String)
    access_time = Column(DateTime)
    access_id = Column(String)


class FishHash(Base):
    __tablename__ = 'FishHash'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    apikey = Column(String(255), nullable=False)
    docker_image_name = Column(String(255), nullable=False)
    docker_image_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

class UserTable(Base):
    __tablename__ = 'UserTable'

    email = Column(String(255), primary_key=True, index=True)
    apikey = Column(String(255), nullable=False)