from mailchimp import chimp 
from util.util import bad_resp_match
from util.util import transform_mailchimp_response

import base64
import json
import redis
import logging
import os
import sys

class RedisService(object):
    """Wrapper class to control redis"""

    def __init__(self, list_id,pool_id=0):
        self.list_id = list_id
        self.redis_server = self.connect_to_redis(pool_id)
        
    def pull_mailchimp(self):
       return self._init_redis_with_mailchimp(self.list_id)

    def connect_to_redis(self, id):
        redis_server = redis.StrictRedis(host='localhost', port=6379, db=id)
        return redis_server

    def _init_redis_with_mailchimp(self,list_id):
        """Inserts ASUIDs into redis for quick access""" 
        try:
            req = chimp.ChimpRequester()
            resp = req.get_list(list_id)
            # check if mailchimp response is bad
            if bad_resp_match(str(resp.status_code)):
                logging.error("Bad MailChimp Request for list {}".format(list_id))
                logging.error(resp.status_code)
                logging.error(resp.json())
                logging.error("Skipping List")
                return False
        
            mailchimp_list = transform_mailchimp_response(resp.json())

            for m in mailchimp_list:
                id = m['ASU_ID']
                m = json.dumps(m)
                m = base64.b64encode(m)
                self.redis_server.set(id,m)

        except Exception as e:
            logging.error("Failure to Setup Redis Pool for list")
            logging.error(e)
            logging.error("Skipping list")
            return False
        
        return True 
   
    def __str__(self):
        return "Redis holds {} list".format(self.list_name)

class RedisPopulater(object):
    """Populate and store redis db information"""

    def __init__(self):
        self.redis_host = self._get_redis_host()
        self.redis_port = self._get_redis_port()
        self.redis_list_store = self._connect_list_store()

    def _get_redis_host(self):

        try:
            redis_host =  os.environ['REDIS_HOST']
        except KeyError:
            redis_host = None 
            logging.error("Failed to initialize redis")
        return redis_host
    
    def _get_redis_port(self): 

        try:
            redis_port = os.environ['REDIS_PORT']
        except KeyError:
            redis_port = None
            logging.error("Failed to initialize redis")
        return redis_port

    def _connect_list_store(self):

        if not (self.redis_host and self.redis_port):
            # log and fail
            logging.fatal("Invalid Configs restart server")
            sys.exit(1)

        # setup redis db # 0
        redis_server = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=0)

        return redis_server

    def get_list_count(self):

        list_count = self.redis_list_store.get('list_count')

        if not list_count:
            return 0
        return list_count

    def get_redis_info(self):

        data = self.redis_list_store.get('mailchimp_lists')

        if not data:
            return None
    
        data = base64.b64decode(data)
        return json.loads(data)

    def get_list_db(self,list_id):

        redis_db_num = self.redis_list_store.get(list_id)

        if not redis_db_num:
            logging.info("Redis db not found")
            return None 
        # create connection to redis db 
        redis_db = RedisService(list_id,redis_db_num)
        return redis_db

    def _read_mailchimp_config(self):

        try:
            config_path = os.environ['MAILCHIMP_LIST_CONFIG']

            with open(config_path) as json_file:
                data = json.load(json_file)
                return data['mailchimp_lists']
        except Exception as e:
            logging.error(e)
            logging.error("Failure to read config for mailchimp")
            return None

    def init_redis_dbs(self):

        requester = chimp.ChimpRequester()

        mailchimp_data = self._read_mailchimp_config()

        if not mailchimp_data:
            return None 
        db_num = 1
        valid_list = []
        for mail_list in mailchimp_data:
            
            r = RedisService(mail_list['id'],db_num)
            if r.pull_mailchimp():
                self.redis_list_store.set(mail_list['id'], db_num)
                valid_list.append(mail_list)
            db_num += 1

        self.redis_list_store.set("mailchimp_list_count",db_num)

        json_vaild_list = json.dumps(valid_list)

        encode_mailchimp = base64.b64encode(json_vaild_list)
        self.redis_list_store.set("mailchimp_lists",encode_mailchimp)

        