# 1. Python 3.8 이미지 기반
FROM python:3.8-slim

# 2. 작업 디렉터리 설정
WORKDIR /app

# 3. 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    libmariadb-dev-compat \
    libmariadb-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 4. 프로젝트의 종속성을 추가
COPY requirements.txt .

# 5. Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 6. 애플리케이션 소스 코드를 컨테이너로 복사
COPY . .

# 7. start.sh 파일 복사 및 실행 권한 부여
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# 8. 스크립트를 ENTRYPOINT로 설정
ENTRYPOINT ["/app/start.sh"]
