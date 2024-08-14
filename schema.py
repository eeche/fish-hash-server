from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Access_Data(BaseModel):
    user_id: Optional[str] = None
    channel_id: Optional[str] = None
    access_time: Optional[datetime] = None
    access_id: Optional[str] = None

    class Config:
        orm_mode = True

class Ioc_Data(BaseModel):
    ioc_item : Optional[str] = None
    ioc_type : Optional[str] = None

    class Config:
        orm_mode = True

class FishHashBase(BaseModel):
    email: str
    apikey: str
    docker_image_name: str
    docker_image_hash: str

    class Config:
        orm_mode = True

class FishHashCreate(FishHashBase):
    pass

class FishHash(FishHashBase):
    id: int
    created_at: Optional[str]

class UserEmail(BaseModel):
    email: str

    class Config:
        orm_mode = True

class DockerHashRequest(BaseModel):
    apikey: str
    docker_image_name: str
    docker_image_hash: str
