from sqlalchemy.orm import Session
import models
import schema

def create_fishhash(db: Session, fishhash: schema.FishHashCreate):
    db_fishhash = models.FishHash(**fishhash.model_dump())
    db.add(db_fishhash)
    db.commit()
    db.refresh(db_fishhash)
    return db_fishhash

def get_fishhash(db: Session, fishhash_id: int):
    return db.query(models.FishHash).filter(models.FishHash.id == fishhash_id).first()

def get_fishhash_by_email(db: Session, email: str):
    return db.query(models.FishHash).filter(models.FishHash.email == email).first()

def get_fishhashes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.FishHash).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.UserTable).filter(models.UserTable.email == email).first()

def update_user_api_key(db: Session, email: str, api_key: str):
    db_user = get_user_by_email(db, email=email)
    if db_user:
        db_user.apikey = api_key
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

#  모든 docker관련 api는 email이 필요없음
#  register docker_image로 등록하는 api => 이미지 명 같든 틀리든 무조건 overwrite
#  verify는 api_key, docker_image_name, docker_image_hash로 검증함

def get_user_by_apikey(db: Session, apikey: str):
    return db.query(models.UserTable).filter(models.UserTable.apikey == apikey).first()

def get_fishhash_by_apikey_and_docker_name(db: Session, apikey: str, docker_image_name: str):
    return db.query(models.FishHash).filter(models.FishHash.apikey == apikey, models.FishHash.docker_image_name == docker_image_name).first()
