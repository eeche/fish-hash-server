#!/bin/bash
python -c "from main import init_db; init_db()"  # init_db() 호출
uvicorn api:app --host 0.0.0.0 --port 8080  # uvicorn 실행
