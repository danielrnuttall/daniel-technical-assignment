import os

import pytest

from src.lambdas.csv_pace_calculator.function.models.garmin_file_row import Row


@pytest.fixture(scope="class", autouse=True)
def mock_envs():
    os.environ["AWS_ACCESS_KEY_ID"] = "foobar"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "foobar"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["S3_BUCKET_NAME"] = "foo_bucket_name"
    os.environ["RUNNING_PACE_SESSION_TABLE_NAME"] = "foo_table_name"


def test_check_if_row_has_necessary_columns_true():
    from src.lambdas.csv_pace_calculator.function.function import (
        _check_if_row_has_necessary_columns,
    )

    row = Row(
        calendarDate="foo",
        garmin_total_timer_time="foo",
        garmin_timestamp="foo",
        garmin_avg_heart_rate="foo",
        garmin_total_distance="foo",
        garmin_restingHeartRateInBeatsPerMinute="foo",
        garmin_vo2Max="foo",
        garmin_sport="foo",
        garmin_start_time="foo",
        garmin_max_heart_rate="foo",
    )
    expected = True
    actual = _check_if_row_has_necessary_columns(row)
    assert expected == actual


def test_check_if_row_has_necessary_columns_false():
    from src.lambdas.csv_pace_calculator.function.function import (
        _check_if_row_has_necessary_columns,
    )

    row = Row(
        calendarDate="foo",
        garmin_total_timer_time="",
        garmin_timestamp="foo",
        garmin_avg_heart_rate="foo",
        garmin_total_distance="foo",
        garmin_restingHeartRateInBeatsPerMinute="foo",
        garmin_vo2Max="foo",
        garmin_sport="foo",
        garmin_start_time="foo",
        garmin_max_heart_rate="foo",
    )
    expected = False
    actual = _check_if_row_has_necessary_columns(row)
    assert expected == actual

    row = Row(
        calendarDate="foo",
        garmin_total_timer_time="foo",
        garmin_timestamp="foo",
        garmin_avg_heart_rate="foo",
        garmin_total_distance="",
        garmin_restingHeartRateInBeatsPerMinute="foo",
        garmin_vo2Max="foo",
        garmin_sport="foo",
        garmin_start_time="foo",
        garmin_max_heart_rate="foo",
    )
    expected = False
    actual = _check_if_row_has_necessary_columns(row)
    assert expected == actual

    row = Row(
        calendarDate="",
        garmin_total_timer_time="foo",
        garmin_timestamp="foo",
        garmin_avg_heart_rate="foo",
        garmin_total_distance="foo",
        garmin_restingHeartRateInBeatsPerMinute="foo",
        garmin_vo2Max="foo",
        garmin_sport="foo",
        garmin_start_time="foo",
        garmin_max_heart_rate="foo",
    )
    expected = False
    actual = _check_if_row_has_necessary_columns(row)
    assert expected == actual

    row = Row(
        calendarDate="foo",
        garmin_total_timer_time="foo",
        garmin_timestamp="",
        garmin_avg_heart_rate="foo",
        garmin_total_distance="foo",
        garmin_restingHeartRateInBeatsPerMinute="foo",
        garmin_vo2Max="foo",
        garmin_sport="foo",
        garmin_start_time="foo",
        garmin_max_heart_rate="foo",
    )
    expected = False
    actual = _check_if_row_has_necessary_columns(row)
    assert expected == actual


def test_calculate_pace():
    from src.lambdas.csv_pace_calculator.function.function import _calculate_pace

    row = Row(
        calendarDate="foo",
        garmin_total_timer_time="1473,25",
        garmin_timestamp="foo",
        garmin_avg_heart_rate="foo",
        garmin_total_distance="4163,82",
        garmin_restingHeartRateInBeatsPerMinute="foo",
        garmin_vo2Max="foo",
        garmin_sport="foo",
        garmin_start_time="foo",
        garmin_max_heart_rate="foo",
    )
    expected = 0.35382
    actual = _calculate_pace(row)
    assert expected == actual
