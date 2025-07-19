import logging
import allure


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LoggerUtility:
    @staticmethod
    def log_response_with_logger(response):
        if response:
            logger.info(f"Status: {response.status_code}")
            logger.info(f"Body: {response.text}")
        else:
            logger.warning("No response found to log")

    @staticmethod
    def log_response_with_allure(response):
        allure.attach(str(response.status_code), name = "Status Code", attachment_type = allure.attachment_type.TEXT)
        allure.attach(response.text, name = "Response Body", attachment_type = allure.attachment_type.JSON)
        allure.attach(str(response.elapsed.total_seconds()), name = "Response Time",
                      attachment_type = allure.attachment_type.TEXT)