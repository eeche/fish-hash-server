import hashlib
import os
import crud
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import db
import schema
import models

app = FastAPI()



def generate_api_key(email: str) -> str:
    random_string = os.urandom(32).hex()
    api_key = hashlib.sha256(f"{email}{random_string}".encode()).hexdigest()
    return api_key


def log_action(db: Session, email: str, action: str, status: str, docker_image_name: str, docker_image_hash: str):
    log_entry = models.Log(
        email=email,
        action=action,
        status=status,
        docker_image_name=docker_image_name,
        docker_image_hash=docker_image_hash
    )
    db.add(log_entry)
    db.commit()


def get_user_or_log_error(db: Session, apikey: str, action: str, docker_image_name: str, docker_image_hash: str) -> models.UserTable:
    db_user = crud.get_user_by_apikey(db, apikey=apikey)
    if not db_user:
        log_action(db, "unknown", action, "failed", docker_image_name, docker_image_hash)
        raise HTTPException(status_code=403, detail="Invalid API key")
    return db_user


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/get-api-key/")
async def get_api_key(email: schema.UserEmail, db: Session = Depends(db.get_session)):
    # UserTable에서 email에 해당하는 레코드 검색
    db_user = crud.get_user_by_email(db, email=email.email)

    if db_user:
        # 이메일이 이미 존재하면 해당 API 키를 반환
        return {"email": db_user.email, "api_key": db_user.apikey}
    else:
        # 이메일이 존재하지 않으면 새로운 API 키 생성 후 반환
        new_api_key = generate_api_key(email.email)
        new_user = models.UserTable(email=email.email, apikey=new_api_key)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"email": new_user.email, "api_key": new_user.apikey}


@app.post("/api/verify-docker-hash/")
async def verify_docker_hash(data: schema.DockerHashRequest, db: Session = Depends(db.get_session)):
    # 기존에 UserTable에서 매칭 여부 확인하던걸, 로그추가해서 함수화
    db_user = get_user_or_log_error(db, data.apikey, "verify", data.docker_image_name, data.docker_image_hash)

    
    # 1. UserTable에서 apikey가 매칭되는지 확인
    # db_user = crud.get_user_by_apikey(db, apikey=data.apikey)
    # if not db_user:
    #     raise HTTPException(status_code=403, detail="Invalid API key")

    db_fishhash = crud.get_fishhash_by_apikey_and_docker_name(db, apikey=data.apikey, docker_image_name=data.docker_image_name)
    
    if not db_fishhash:
        log_action(db, db_user.email, "verify", "failed", data.docker_image_name, data.docker_image_hash)
        return {"status": "Docker image not found", "match": False}

    match_status  = "success" if db_fishhash.docker_image_hash == data.docker_image_hash else "failed"
    log_action(db, db_user.email, "verify", match_status, data.docker_image_name, data.docker_image_hash)
    
    return {"status": "Hash matches" if match_status == "success" else "Hash does not match", "match": match_status == "success"}


@app.post("/api/register-docker-hash/")
async def register_docker_hash(data: schema.DockerHashRequest, db: Session = Depends(db.get_session)):

    db_user = get_user_or_log_error(db, data.apikey, "register", data.docker_image_name, data.docker_image_hash)
    db_fishhash = crud.get_fishhash_by_apikey_and_docker_name(db, apikey=data.apikey, docker_image_name=data.docker_image_name)

    if not db_fishhash:
        # 3. 해당 docker_image_name이 존재하지 않으면 새로운 레코드를 추가
        new_fishhash = models.FishHash(
            apikey=data.apikey,
            docker_image_name=data.docker_image_name,
            docker_image_hash=data.docker_image_hash
        )
        db.add(new_fishhash)
        db.commit()
        db.refresh(new_fishhash)
        log_action(db, db_user.email, "register", "success", data.docker_image_name, data.docker_image_hash)

        return {"status": "Docker image and hash registered successfully."}
    else:
        # 4. 해당 docker_image_name이 이미 존재하면 docker_image_hash를 업데이트
        db_fishhash.docker_image_hash = data.docker_image_hash
        db.commit()
        db.refresh(db_fishhash)
        log_action(db, db_user.email, "register", "success", data.docker_image_name, data.docker_image_hash)

        return {"status": "Docker image hash updated successfully."}