import hashlib
import os
import crud
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import db
import schema
import models
from typing import List  # List를 import 합니다.


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


def generate_api_key(email: str) -> str:
    random_string = os.urandom(32).hex()
    api_key = hashlib.sha256(f"{email}{random_string}".encode()).hexdigest()
    return api_key


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


@app.post("/verify-docker-hash/")
async def verify_docker_hash(data: schema.DockerHashRequest, db: Session = Depends(db.get_session)):
    # 1. UserTable에서 apikey가 매칭되는지 확인
    db_user = crud.get_user_by_apikey(db, apikey=data.apikey)
    if not db_user:
        raise HTTPException(status_code=403, detail="Invalid API key")

    # 2. FishHash 테이블에서 해당 apikey와 docker_image_name으로 데이터 검색
    db_fishhash = crud.get_fishhash_by_apikey_and_docker_name(db, apikey=data.apikey, docker_image_name=data.docker_image_name)
    
    if not db_fishhash:
        # 3. docker_image_name이 존재하지 않는 경우
        return {"status": "Docker image not found", "match": False}

    # 4. docker_image_name이 있다면 hash 값을 비교하고 결과를 반환
    if db_fishhash.docker_image_hash == data.docker_image_hash:
        return {"status": "Hash matches", "match": True}
    else:
        return {"status": "Hash does not match", "match": False}


@app.post("/register-docker-hash/")
async def register_docker_hash(data: schema.DockerHashRequest, db: Session = Depends(db.get_session)):
    # 1. UserTable에서 apikey가 존재하는지 확인
    db_user = crud.get_user_by_apikey(db, apikey=data.apikey)
    if not db_user:
        raise HTTPException(status_code=403, detail="Invalid API key")

    # 2. FishHash 테이블에서 apikey와 docker_image_name으로 데이터 검색
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
        return {"status": "Docker image and hash registered successfully."}
    else:
        # 4. 해당 docker_image_name이 이미 존재하면 docker_image_hash를 업데이트
        db_fishhash.docker_image_hash = data.docker_image_hash
        db.commit()
        db.refresh(db_fishhash)
        return {"status": "Docker image hash updated successfully."}