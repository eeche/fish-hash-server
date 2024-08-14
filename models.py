from sqlalchemy import Column, String, ForeignKey
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
