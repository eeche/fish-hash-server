from typing import Optional
from pydantic import BaseModel, ConfigDict

class FishHashBase(BaseModel):
    email: str
    apikey: str
    docker_image_name: str
    docker_image_hash: str

    model_config = ConfigDict(from_attributes=True)

class FishHashCreate(FishHashBase):
    pass

class FishHash(FishHashBase):
    id: int
    created_at: Optional[str] = None

class UserEmail(BaseModel):
    email: str

    model_config = ConfigDict(from_attributes=True)

class DockerHashRequest(BaseModel):
    apikey: str
    docker_image_name: str
    docker_image_hash: str

class LogRequest(BaseModel):
    apikey :str

    model_config = ConfigDict(from_attributes=True)