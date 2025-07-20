import allure

class AssertHelper:


    @staticmethod
    @allure.step('Verifying response title is correct')
    def assert_title_is(json_data, expected_title):
        assert json_data['title'] == expected_title, f"Expected title '{expected_title}', got '{json_data.get('title')}'"

    @staticmethod
    @allure.step('Verifying response code')
    def assert_status_code_is(actual_status, expected_status):
        assert actual_status == expected_status, f"Expected status {expected_status}, got {actual_status}"

    @staticmethod
    @allure.step('Check that response status is not 200')
    def assert_status_code_is_not_200(status_code):
        assert status_code != 200, "Expected a non-200 status code"

    @staticmethod
    @allure.step('Check that request returned within specified seconds')
    def assert_response_time_within_limit(response_time, seconds):
        assert response_time < seconds, f"Response took {response_time:.2f}s, expected under {seconds}s"
