import allure
import requests
from pydantic import ValidationError
from config.config_loader import load_config_data


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

    @allure.step('Logging full response')
    def log_response(self):
        allure.attach(str(self.response.status_code), name = "Status Code", attachment_type = allure.attachment_type.TEXT)
        allure.attach(self.response.text, name = "Response Body", attachment_type = allure.attachment_type.JSON)
        allure.attach(str(self.response.elapsed.total_seconds()), name = "Response Time",
                      attachment_type = allure.attachment_type.TEXT)

    @allure.step('Validating response schema')
    def validate_response_schema(self, model_class):
        try:
            print('Validating Post Response Model')
            model_class(**self.json)
            print("Schema validated successfully")
        except ValidationError as e:
            print("Schema validation failed:")
            print(e)
            raise

