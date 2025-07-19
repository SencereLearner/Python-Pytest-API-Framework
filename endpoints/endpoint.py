import allure
import requests
import logging
from config.config_loader import load_config_data
from utils.logger_utility import LoggerUtility

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Endpoint:

    response = None
    json = None
    headers = {'Content-type': 'application/json'}
    config = load_config_data()


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

    @allure.step('Verifying response title is correct')
    def assert_response_title_is_correct(self, title):
        assert self.json['title'] == title

    @allure.step('Verifying response code')
    def assert_response_code_is(self, expected):
        actual = self.response.status_code
        assert actual == expected, f"Expected {expected}, got {actual}"

    @allure.step('Check that response error code is received')
    def assert_bad_request_code_is_not_200(self):
        assert self.response.status_code != 200

    @allure.step('Check that request returned within 2 seconds')
    def assert_request_returned_within_seconds(self, seconds):
        assert self.response.elapsed.total_seconds() < seconds



