import csv
import os
import uuid
from typing import Any, Dict, List

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser import ValidationError
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import parse_obj_as

from .models.garmin_dynamo_db_record import (
    CalendarDate,
    Distance,
    Duration,
    GarminDynamodbRecord,
    Id,
    RunningPace,
    Timestamp,
)
from .models.garmin_file_row import Row

logger = Logger()

_s3_bucket_name = os.environ["S3_BUCKET_NAME"]
_running_pace_session_table_name = os.environ["RUNNING_PACE_SESSION_TABLE_NAME"]

_s3 = boto3.resource("s3")
_dynamodb = boto3.client("dynamodb")


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    try:
        file_name = event["file_name"]
        logger.info({"action": "Getting file from S3.", "file_name": file_name})
        response = _get_object_from_s3(file_name)
        logger.info({"action": "Fetched object from S3", "key": file_name})
        object_str = _decode_file_contents(response)

        row_list = _add_rows_to_list(object_str)
        garmin_data = parse_obj_as(List[Row], row_list)
        logger.info({"action": "Extracted rows, now going to process data"})
        for row in garmin_data:
            if _check_if_row_has_necessary_columns(row):
                pace = _calculate_pace(row)
                logger.info({"action": "Uploading calculated pace to DynamoDB"})
                dynamodb_item = _create_dynamodb_item(row, pace)
                _dynamodb.put_item(
                    TableName=_running_pace_session_table_name, Item=dynamodb_item
                )
        logger.info({"action": "Completed processing CSV file."})
        return {"statusCode": 200}
    except ValidationError as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise


def _decode_file_contents(object_data):
    return object_data["Body"].read().decode()


def _get_object_from_s3(key: str):
    file_path = "garmin/" + key
    logger.info({"action": "Fetching object from S3.", "key": file_path})
    s3_object = _s3.Object(bucket_name=_s3_bucket_name, key=file_path)
    return s3_object.get()


def _add_rows_to_list(file_data: str) -> list:
    logger.info({"action": "Now extracting rows from CSV file to process"})
    row_list = []
    reader = csv.DictReader(file_data.splitlines(), delimiter=";")
    for row in reader:
        row_list.append(row)
    return row_list


def _calculate_pace(row: Row) -> float:
    garmin_total_timer_time = float(row.garmin_total_timer_time.replace(",", "."))
    garmin_total_distance = float(row.garmin_total_distance.replace(",", "."))
    if garmin_total_distance == 0:
        return 0
    return round(garmin_total_timer_time / garmin_total_distance, 5)


def _check_if_row_has_necessary_columns(row: Row) -> bool:
    return (
        False
        if row.garmin_total_timer_time == ""
        or row.garmin_total_distance == ""
        or row.calendar_date == ""
        or row.garmin_timestamp == ""
        else True
    )


def _create_dynamodb_item(row: Row, running_pace: float) -> dict:
    garmin_timestamp = row.garmin_timestamp
    calendar_date = row.calendar_date
    duration = row.garmin_total_timer_time
    garmin_total_distance = row.garmin_total_distance
    dynamodb_record = GarminDynamodbRecord(
        id=Id(S=str(uuid.uuid4())),
        timestamp=Timestamp(S=garmin_timestamp),
        calendar_date=CalendarDate(S=calendar_date),
        duration=Duration(S=duration),
        distance=Distance(S=garmin_total_distance),
        running_pace=RunningPace(S=running_pace),
    )
    return dynamodb_record.dict()
