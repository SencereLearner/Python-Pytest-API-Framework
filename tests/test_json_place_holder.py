import sys
import pytest
from models.post_response_model import PostResponseModel
import utils.response_validation


TEST_DATA = [
    {"title": "My title", "body": "my body", "userId": 1},
    {"title": "My title2", "body": "my body2", "userId": 2}
]

NEGATIVE_DATA = [
    {"title": ["My title"], "body": "my body", "userId": 1},
    {"title": {"My title2": ''}, "body": "my body2", "userId": 2}
]

# @pytest.mark.skip(reason="Test temporarily disabled")
@pytest.mark.parametrize('data', TEST_DATA)
def test_post_a_post(create_post_endpoint_fixture, data):
    create_post_endpoint_fixture.create_new_post(payload=data)
    create_post_endpoint_fixture.assert_response_code_is(201)
    create_post_endpoint_fixture.assert_response_title_is_correct(data['title'])

@pytest.mark.parametrize('data', NEGATIVE_DATA)
def test_post_with_negative_data(create_post_endpoint_fixture, data):
    create_post_endpoint_fixture.create_new_post(payload=data)
    create_post_endpoint_fixture.assert_bad_request_code_is_not_200()
    create_post_endpoint_fixture.assert_response_title_is_correct(data['title'])

def test_put_a_post(update_post_endpoint_fixture):
    payload = {"title": "UpdatedTitle", "body": "UpdatedBody", "userId": 2}
    update_post_endpoint_fixture.make_changes_in_post(42, payload)
    update_post_endpoint_fixture.assert_response_title_is_correct(payload['title'])
    update_post_endpoint_fixture.assert_response_code_is(200)

@pytest.mark.testing
def test_get_specific_endpoint(get_specific_endpoint_fixture):
    get_specific_endpoint_fixture.get_specific_endpoint(5)
    get_specific_endpoint_fixture.assert_response_code_is(200)
    get_specific_endpoint_fixture.assert_request_returned_within_seconds(1)

@pytest.mark.skipif(sys.platform == "win32", reason="Does not run on Windows")
def test_post_schema_validation(create_post_endpoint_fixture):
    payload = {"title": "Hello", "body": "world", "userId": 1}
    create_post_endpoint_fixture.create_new_post(payload)
    utils.response_validation.validate_response_schema(create_post_endpoint_fixture.json, PostResponseModel)