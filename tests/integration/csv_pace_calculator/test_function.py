import io
import os
from uuid import uuid4

import pytest
from botocore.response import StreamingBody
from botocore.stub import Stubber


@pytest.fixture(scope="function")
def test_valid_file_data():
    file_path = os.path.join(os.path.dirname(__file__), "garmin_activity_test_file.csv")
    with open(os.path.join(file_path), "r") as f:
        return f.read()


@pytest.fixture(scope="class", autouse=True)
def mock_envs():
    os.environ["AWS_ACCESS_KEY_ID"] = "foobar"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "foobar"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["S3_BUCKET_NAME"] = "foo_bucket_name"
    os.environ["RUNNING_PACE_SESSION_TABLE_NAME"] = "foo_table_name"


@pytest.fixture(scope="function")
def dynamodb_stub():
    from src.lambdas.csv_pace_calculator.function.function import _dynamodb

    with Stubber(_dynamodb) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


@pytest.fixture(scope="function")
def s3_stub():
    from src.lambdas.csv_pace_calculator.function.function import _s3

    with Stubber(_s3.meta.client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


@pytest.fixture(scope="function")
def mock_aws(test_valid_file_data, dynamodb_stub: Stubber, s3_stub: Stubber):
    encoded_message = test_valid_file_data.encode()
    raw_stream = StreamingBody(io.BytesIO(encoded_message), len(encoded_message))
    response = {"Body": raw_stream}
    expected_params = {
        "Bucket": "foo_bucket_name",
        "Key": "garmin_activity_test_file.csv",
    }
    s3_stub.add_response("get_object", response, expected_params)
    put_item_response = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    dynamodb_stub.add_response("put_item", service_response=put_item_response)
    dynamodb_stub.add_response("put_item", service_response=put_item_response)


class MockContext(object):
    def __init__(self, function_name):
        self.function_name = function_name
        self.function_version = "v$LATEST"
        self.memory_limit_in_mb = 512
        self.invoked_function_arn = (
            f"arn:aws:lambda:us-east-1:ACCOUNT:function:{self.function_name}"
        )
        self.aws_request_id = str(uuid4)


@pytest.fixture
def lambda_context():
    return MockContext("dummy_function")


@pytest.fixture(scope="function")
def mock_event():
    return {"file_name": "garmin_activity_test_file.csv"}


def test_happy_path(mock_event, lambda_context, mock_aws):
    from src.lambdas.csv_pace_calculator.function.function import lambda_handler

    actual = lambda_handler(mock_event, lambda_context)
    expected = {"statusCode": 200}
    assert expected == actual


# Pytest:
# Test happy path flow file
# Test empty file
# Test file with incorrect rows/columns

# Rows: calendarDate;garmin_total_timer_time;garmin_timestamp;garmin_avg_heart_rate;garmin_total_elapsed_time;garmin_total_distance;garmin_restingHeartRateInBeatsPerMinute;garmin_vo2Max;garmin_sport;garmin_start_time;garmin_max_heart_rate
