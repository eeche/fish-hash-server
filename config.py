import os.path
import json
import os

config_path = './conf/conf.json'

# conf.json 파일이 없거나 내용이 비어 있을 경우 기본 값 설정
if not os.path.isfile(config_path) or os.path.getsize(config_path) == 0:
    conf = {}
    conf['dbpassword']  = os.environ.get('DB_PASSWORD', 'password')
    conf['log']  = os.environ.get('LOG_LVL', 'info')
    conf['master_email'] = os.environ.get('MASTER_EMAIL', 'default_email@example.com')
    conf['master_apikey'] = os.environ.get('MASTER_APIKEY', 'default_apikey')
    conf['dbhost'] = os.environ.get('DB_HOST', 'db')
    conf['dbuser'] = os.environ.get('DB_USER', 'root')
    conf['dbname'] = os.environ.get('DB_NAME', 'bob')
    os.makedirs(os.path.dirname(config_path), exist_ok=True)  # 디렉토리가 없으면 생성
    with open(config_path, 'w') as newconf:
        json.dump(conf, newconf, indent=4)

# conf.json 파일이 존재하고 내용이 있을 때 읽기
with open(config_path, 'r') as mainconf:
    try:
        conf = json.load(mainconf)
    except json.JSONDecodeError:
        # JSONDecodeError가 발생하면 기본 값으로 파일을 덮어씀
        conf = {}
        conf['dbpassword']  = os.environ.get('DB_PASSWORD', 'password')
        conf['log']  = os.environ.get('LOG_LVL', 'info')
        conf['master_email'] = os.environ.get('MASTER_EMAIL', 'default_email@example.com')
        conf['master_apikey'] = os.environ.get('MASTER_APIKEY', 'default_apikey')
        conf['dbhost'] = os.environ.get('DB_HOST', 'db')
        conf['dbuser'] = os.environ.get('DB_USER', 'root')
        conf['dbname'] = os.environ.get('DB_NAME', 'bob')
        
        with open(config_path, 'w') as newconf:
            json.dump(conf, newconf, indent=4)

MASTER_EMAIL = conf.get('master_email')
MASTER_APIKEY = conf.get('master_apikey')
