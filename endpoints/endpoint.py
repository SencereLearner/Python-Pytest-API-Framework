import allure
import requests
import logging
from config.config_loader import load_config_data
from utils.logger_utility import LoggerUtility
from tenacity import retry, stop_after_attempt, wait_fixed, before_sleep_log


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Endpoint:

    response = None
    json = None
    headers = {'Content-type': 'application/json'}
    config = load_config_data()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def send_request(self, method, request_id=None, payload=None, headers=None):
        headers = headers if headers else self.headers
        url = f"{self.config['base_url']}/{request_id}" if request_id else self.config['base_url']
        print(f"Loaded base URL: {self.config['base_url']}")

        match method.upper():
            case 'GET':
                self.response = requests.get(url, headers=headers)
            case 'POST':
                self.response = requests.post(url, json=payload, headers=headers)
            case 'PUT':
                self.response = requests.put(url, json=payload, headers=headers)
            case 'DELETE':
                self.response = requests.delete(url, headers=headers)
            case _:
                raise ValueError(f"Unsupported HTTP method: {method}")

        LoggerUtility.log_response_with_logger(self.response)
        LoggerUtility.log_response_with_allure(self.response)
        self.json = self.response.json()
        return self.response





