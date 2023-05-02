from typing import List

from aws_lambda_powertools.utilities.parser import BaseModel


class Id(BaseModel):
    S: str


class Distance(BaseModel):
    S: str


class Timestamp(BaseModel):
    S: str


class CalendarDate(BaseModel):
    S: str


class Duration(BaseModel):
    S: str


class RunningPace(BaseModel):
    S: str


class GarminDynamodbRecord(BaseModel):
    id: Id
    timestamp: Timestamp
    calendar_date: CalendarDate
    duration: Duration
    distance: Distance
    running_pace: RunningPace
