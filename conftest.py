import pytest
from endpoints.create_post import CreatePostClass
from endpoints.update_endpoint import UpdatePostClass
from endpoints.get_endpoint import GetEndpointClass

@pytest.fixture()
def create_post_endpoint_fixture():
    return CreatePostClass()

@pytest.fixture()
def update_post_endpoint_fixture():
    return UpdatePostClass()

@pytest.fixture()
def get_specific_endpoint_fixture():
    return GetEndpointClass()



