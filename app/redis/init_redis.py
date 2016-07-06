from mailchimp import chimp 
from util.util import bad_resp_match
from util.util import transform_mailchimp_response

import logging
import os
import sys

def init_redis_with_mailchimp(redis_server):
    """Inserts ASUIDs into redis for quick access""" 
    try:
        default_list = os.environ['DEFAULT_MAILCHIMP_LIST']
        req = chimp.ChimpRequester()
        resp = req.get_list(default_list)
        # # check if mailchimp response is bad
        # if bad_resp_match(str(resp.status_code)):
        #     logging.error("Bad MailChimp Request")
        #     logging.error(resp.status_code)
        #     logging.error(resp.json())
        #     logging.error("Shutting Down Service")
        #     sys.exit(1)
        # mailchimp_list = transform_mailchimp_response(resp.json())
        # for m in mailchimp_list:
        #     logging.info(m)
        #     redis_server.set(m['ASUID'],True)
        # logging.info("Inserted into redis")
    except Exception as e:
        logging.error("Failure to Setup Redis")
        logging.error(e)
        logging.error("Shutting Down Service")
        sys.exit(1)


