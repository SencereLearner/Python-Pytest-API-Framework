import allure
from endpoints.endpoint import Endpoint

class CreatePostClass(Endpoint):
# another approach is to use __init__ and pass data so upon class initialization all the data will be passed automatically
# And instead of using decorator: test_post_a_post(create_post_endpoint_fixture): I would have to create object of
# a class: create_post_endpoint_fixture = CreatePostClass()

    @allure.step('Creating a new post')
    def create_new_post(self, payload, headers = None):
        self.send_request('POST', payload=payload, headers=headers)



