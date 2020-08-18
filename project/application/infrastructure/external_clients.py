import requests
import logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from flask import current_app

from application.utils import timer

logger = logging.getLogger(__name__)

session = requests.sessions.Session()
retries = Retry(total=2, backoff_factor=0.1, status_forcelist=[500, 502, 503])
session.mount("https://", HTTPAdapter(max_retries=retries))

timeout = 35


class BaseExternalClient:
    def __init__(self):
        pass

    def make_post_request(self, url, data=None, headers=None):
        logger.info("Getting response from %s" % url)
        response = session.post(url, json=data, headers=headers, timeout=timeout)
        logger.info("Response code: %s for url: %s" % (response.status_code, url))
        if not 200 <= response.status_code <= 300:
            raise Exception("Error while calling url:%s " % response.url)
        return response.json()

    def make_get_request(self, url, data=None, session=requests.session()):
        logger.info("Getting response from %s" % url)
        response = session.get(url, params=data, timeout=timeout)
        logger.info(
            "Response code: %s for url: %s, data: %s"
            % (response.status_code, response.url, str(data))
        )
        if not 200 <= response.status_code <= 300:
            raise Exception("Error while calling url:%s " % response.url)
        return response.json()
