import os
import uvicorn
import logging
import models
import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from database import db, Base

load_dotenv()

logging.basicConfig(level=logging.INFO)

MASTER_EMAIL = os.getenv('MASTER_EMAIL')
MASTER_APIKEY = os.getenv('MASTER_APIKEY')

def init_db(max_retries=5, retry_interval=5):
    logging.info("FishHash API Server is starting...")
    retries = 0
    while retries < max_retries:
        try:
            models.UserTable.__table__.create(db.engine, checkfirst=True)
            models.Log.__table__.create(db.engine, checkfirst=True)
            Base.metadata.create_all(bind=db.engine)
            logging.info("Database tables created successfully or already exist.")

            session = db.Session()
            try:
                add_master_account(session)
            finally:
                session.close()
            
            logging.info("Database initialization successful.")
            return  # 성공적으로 초기화되면 함수 종료
        except OperationalError as e:
            retries += 1
            logging.warning(f"Database connection failed. Retrying in {retry_interval} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(retry_interval)
        except Exception as e:
            logging.error("Failed to initialize database.")
            logging.error(str(e))
            raise

    logging.error(f"Failed to connect to the database after {max_retries} attempts. Exiting...")
    raise Exception("Database connection failed")

def add_master_account(session: Session):
    user = session.query(models.UserTable).filter_by(email=MASTER_EMAIL).first()
    if not user:
        new_user = models.UserTable(email=MASTER_EMAIL, apikey=MASTER_APIKEY)
        session.add(new_user)
        session.commit()
        logging.info("Master account created successfully.")
    else:
        logging.info("Master account already exists.")

if __name__ == '__main__':
    try:
        init_db()  # 재시도 로직이 포함된 init_db 호출

        LOG = 'debug'
        if LOG == 'debug':
            uvicorn.run(
                "api:app",
                host='0.0.0.0',
                port=8080,
                workers=1,
                log_level='info',
                reload=True,
            )
        else:
            uvicorn.run(
                "api:app",
                host='0.0.0.0',
                port=8080,
                workers=5,
                log_level='warning',
                reload=False,
            )
    except KeyboardInterrupt:
        print('\nExiting\n')
    except Exception as errormain:
        print('Failed to Start API')
        print('='*100)
        print(str(errormain))
        print('='*100)
        print('Exiting\n')