import sys
import pytest
from models.post_response_model import PostResponseModel
import utils.response_validation
from utils.assert_helper import AssertHelper

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
    AssertHelper.assert_status_code_is(create_post_endpoint_fixture.response.status_code, 201)
    AssertHelper.assert_title_is(create_post_endpoint_fixture.json, data['title'])

@pytest.mark.parametrize('data', NEGATIVE_DATA)
def test_post_with_negative_data(create_post_endpoint_fixture, data):
    create_post_endpoint_fixture.create_new_post(payload=data)
    AssertHelper.assert_status_code_is_not_200(create_post_endpoint_fixture.response.status_code)
    AssertHelper.assert_title_is(create_post_endpoint_fixture.json, data['title'])

def test_put_a_post(update_post_endpoint_fixture):
    payload = {"title": "UpdatedTitle", "body": "UpdatedBody", "userId": 2}
    update_post_endpoint_fixture.make_changes_in_post(42, payload)
    AssertHelper.assert_title_is(update_post_endpoint_fixture.json, payload['title'])
    AssertHelper.assert_status_code_is(update_post_endpoint_fixture.response.status_code, 200)

@pytest.mark.testing
def test_get_specific_endpoint(get_specific_endpoint_fixture):
    get_specific_endpoint_fixture.get_specific_endpoint(5)
    AssertHelper.assert_status_code_is(get_specific_endpoint_fixture.response.status_code, 200)
    AssertHelper.assert_response_time_within_limit(get_specific_endpoint_fixture.response.elapsed.total_seconds(), 1)

@pytest.mark.skipif(sys.platform == "win32", reason="Does not run on Windows")
def test_post_schema_validation(create_post_endpoint_fixture):
    payload = {"title": "Hello", "body": "world", "userId": 1}
    create_post_endpoint_fixture.create_new_post(payload)
    utils.response_validation.validate_response_schema(create_post_endpoint_fixture.json, PostResponseModel)