from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class UserTable(Base):
    __tablename__ = 'UserTable'

    email = Column(String(255), primary_key=True, index=True)
    apikey = Column(String(255), nullable=False, unique=True)

    logs = relationship("Log", back_populates="user")


class FishHash(Base):
    __tablename__ = 'FishHash'

    apikey = Column(String(255), ForeignKey('UserTable.apikey'), primary_key=True)
    docker_image_name = Column(String(255), nullable=False)
    docker_image_hash = Column(String(255), nullable=False)

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, ForeignKey('usertable.email'), nullable=False)
    action = Column(String, nullable=False)  # "verify" 또는 "register"와 같은 작업 유형
    status = Column(String, nullable=False)  # 작업의 상태("success", "failed" 등)
    docker_image_name = Column(String, nullable=True)
    docker_image_hash = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserTable", back_populates="logs")
