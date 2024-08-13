import hashlib
import json
import requests
from sqlalchemy.orm import Session
import models
import schema
from config import conf

def write_access_data_in_db(access_id: str, access_item: schema.Access_Data, db: Session):
    pass



def create_fishhash(db: Session, fishhash: schema.FishHashCreate):
    db_fishhash = models.FishHash(**fishhash.dict())
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

def get_user_by_email_and_apikey(db: Session, email: str, apikey: str):
    return db.query(models.UserTable).filter(models.UserTable.email == email, models.UserTable.apikey == apikey).first()

def get_fishhash_by_email_and_docker_name(db: Session, email: str, docker_image_name: str):
    return db.query(models.FishHash).filter(models.FishHash.email == email, models.FishHash.docker_image_name == docker_image_name).first()
