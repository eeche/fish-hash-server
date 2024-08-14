import os
from dotenv import load_dotenv

# .env 파일의 내용을 불러옵니다.
load_dotenv()

# 환경 변수들을 가져옵니다.
DB_PASSWORD = os.getenv('DB_PASSWORD')
LOG_LVL = os.getenv('LOG')
MASTER_EMAIL = os.getenv('MASTER_EMAIL')
MASTER_APIKEY = os.getenv('MASTER_APIKEY')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_NAME = os.getenv('DB_NAME')
