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

    def __init__(self):
        self.redis_server = self.connect_to_redis()
    
    def pull_mailchimp(self):
        self._init_redis_with_mailchimp()

    def connect_to_redis(self):
        redis_server = redis.StrictRedis(host='localhost', port=6379, db=0)
        return redis_server

    def _init_redis_with_mailchimp(self):
        """Inserts ASUIDs into redis for quick access""" 
        try:
            default_list = os.environ['DEFAULT_MAILCHIMP_LIST']
            req = chimp.ChimpRequester()
            resp = req.get_list(default_list)
            # check if mailchimp response is bad
            if bad_resp_match(str(resp.status_code)):
                logging.error("Bad MailChimp Request")
                logging.error(resp.status_code)
                logging.error(resp.json())
                logging.error("Shutting Down Service")
                sys.exit(1)
            mailchimp_list = transform_mailchimp_response(resp.json())

            for m in mailchimp_list:
                id = m['ASU_ID']
                m = json.dumps(m)
                m = base64.b64encode(m)
                self.redis_server.set(id,m)

        except Exception as e:
            logging.error("Failure to Setup Redis")
            logging.error(e)
            logging.error("Shutting Down Service")
            sys.exit(1)




