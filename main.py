import uvicorn
import logging
from database import db, Base
import models  # 테이블 정의를 위한 임포트
from sqlalchemy.orm import Session
from config import MASTER_EMAIL, MASTER_APIKEY  # 마스터 계정 정보 불러오기

logging.basicConfig(level=logging.INFO)

def init_db():
    try:
        # 데이터베이스에 테이블이 없는 경우 테이블 생성
        Base.metadata.create_all(bind=db.engine)
        logging.info("Database tables created successfully or already exist.")

        # 마스터 계정 추가 로직
        session = db.Session()
        try:
            add_master_account(session)
        finally:
            session.close()

    except Exception as e:
        logging.error("Failed to initialize database.")
        logging.error(str(e))
        raise  # 예외를 다시 발생시켜 서버 시작을 중단할지 선택할 수 있음

def add_master_account(session: Session):
    # 마스터 계정이 이미 존재하는지 확인
    user = session.query(models.UserTable).filter_by(email=MASTER_EMAIL).first()
    if not user:
        # 마스터 계정이 존재하지 않으면 새로 추가
        new_user = models.UserTable(email=MASTER_EMAIL, apikey=MASTER_APIKEY)
        session.add(new_user)
        session.commit()
        logging.info("Master account created successfully.")
    else:
        logging.info("Master account already exists.")

if __name__ == '__main__':
    try:
        # 서버 시작 전에 데이터베이스 초기화
        init_db()

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
