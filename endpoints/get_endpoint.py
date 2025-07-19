import allure
from endpoints.endpoint import Endpoint

class GetEndpointClass(Endpoint):


    @allure.step('Getting endpoint')
    def get_specific_endpoint(self, get_id):
        self.send_request('GET', get_id)
