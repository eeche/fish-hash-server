from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class UserTable(Base):
    __tablename__ = 'UserTable'

    email = Column(String(255), primary_key=True, index=True)
    apikey = Column(String(255), nullable=False, unique=True)

class FishHash(Base):
    __tablename__ = 'FishHash'

    apikey = Column(String(255), ForeignKey('UserTable.apikey'), primary_key=True)
    docker_image_name = Column(String(255), nullable=False)
    docker_image_hash = Column(String(255), nullable=False)

class Log(Base):
    __tablename__ = 'Log'

    apikey = Column(String(255), ForeignKey('UserTable.apikey'), primary_key=True)
    emaill = Column(String(255), ForeignKey('UserTable.email'), nullable=False)  
    action = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)  # 작업의 상태("success", "failed" 등)
    docker_image_name = Column(String(255), nullable=True)
    docker_image_hash = Column(String(255), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())