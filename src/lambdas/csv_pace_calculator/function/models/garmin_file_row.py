from typing import List

from aws_lambda_powertools.utilities.parser import BaseModel, Field

# Model = typing.TypeVar("Model", bound="GarminData")


class Row(BaseModel):
    calendar_date: str = Field(alias="calendarDate")
    garmin_total_timer_time: str
    garmin_timestamp: str
    garmin_avg_heart_rate: str
    garmin_total_distance: str
    garmin_resting_heart_rate_in_beats_per_minute: str = Field(
        alias="garmin_restingHeartRateInBeatsPerMinute"
    )
    garmin_vo2_max: str = Field(alias="garmin_vo2Max")
    garmin_sport: str
    garmin_start_time: str
    garmin_max_heart_rate: str

    # def parse_dict(cls: typing.Type[Model], obj: dict):
    #     return GarminData.parse_obj()
