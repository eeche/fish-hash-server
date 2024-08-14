import os.path
import json
import os

if os.path.isfile('./conf/conf.json') is False:
    with open('./conf/conf.json', 'w') as newconf:
        conf = json.load(newconf)
        conf['dbpassword']  = os.environ['DB_PASSWORD']
        conf['log']  = os.environ['LOG_LVL']
        conf['master_email'] = os.environ['MASTER_EMAIL']
        conf['master_apikey'] = os.environ['MASTER_APIKEY']
        json.dump(conf, newconf, indent=4)

with open('./conf/conf.json', 'r') as mainconf:
    conf = json.load(mainconf)


MASTER_EMAIL = conf.get('master_email')
MASTER_APIKEY = conf.get('master_apikey')