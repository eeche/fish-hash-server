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


def log_action(db: Session, email: str, action: str, status: str, docker_image_name: str, docker_image_hash: str, apikey:str):
    log_entry = models.Log(
        apikey = apikey,
        email=email,
        action=action,
        status=status,
        docker_image_name=docker_image_name,
        docker_image_hash=docker_image_hash,
    )
    db.add(log_entry)
    db.commit()




@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/get-api-key/")
async def get_api_key(email: schema.UserEmail, db: Session = Depends(db.get_session)):
    db_user = crud.get_user_by_email(db, email=email.email)

    if db_user:
        return {"email": db_user.email, "api_key": db_user.apikey}
    else:
        new_api_key = generate_api_key(email.email)
        new_user = models.UserTable(email=email.email, apikey=new_api_key)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"email": new_user.email, "api_key": new_user.apikey}


@app.post("/api/verify-docker-hash/")
async def verify_docker_hash(data: schema.DockerHashRequest, db: Session = Depends(db.get_session)):
    db_user = crud.get_user_by_apikey(db, apikey=data.apikey)
    if not db_user:
        raise HTTPException(status_code=403, detail="Invalid API key")

    db_fishhash = crud.get_fishhash_by_apikey_and_docker_name(db, apikey=data.apikey, docker_image_name=data.docker_image_name)
    
    if not db_fishhash:
        log_action(db, db_user.email, "verify", "failed", data.docker_image_name, data.docker_image_hash,data.apikey)
        return {"status": "Docker image not found", "match": False}

    match_status  = "success" if db_fishhash.docker_image_hash == data.docker_image_hash else "failed"
    log_action(db, db_user.email, "verify", match_status, data.docker_image_name, data.docker_image_hash,data.apikey)
    
    return {"status": "Hash matches" if match_status == "success" else "Hash does not match", "match": match_status == "success"}


@app.post("/api/register-docker-hash/")
async def register_docker_hash(data: schema.DockerHashRequest, db: Session = Depends(db.get_session)):
    
    db_user = crud.get_user_by_apikey(db, apikey=data.apikey)
    if not db_user:
        raise HTTPException(status_code=403, detail="Invalid API key")


    db_fishhash = crud.get_fishhash_by_apikey_and_docker_name(db, apikey=data.apikey, docker_image_name=data.docker_image_name)

    if not db_fishhash:
        new_fishhash = models.FishHash(
            apikey=data.apikey,
            docker_image_name=data.docker_image_name,
            docker_image_hash=data.docker_image_hash
        )
        db.add(new_fishhash)
        db.commit()
        db.refresh(new_fishhash)
        log_action(db, db_user.email, "register", "success", data.docker_image_name, data.docker_image_hash,data.apikey)

        return {"status": "Docker image and hash registered successfully."}
    else:
        db_fishhash.docker_image_hash = data.docker_image_hash
        db.commit()
        db.refresh(db_fishhash)
        log_action(db, db_user.email, "register", "success", data.docker_image_name, data.docker_image_hash,data.apikey)

        return {"status": "Docker image hash updated successfully."}