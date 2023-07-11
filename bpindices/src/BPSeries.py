import BPSeriesMetadata
from dataclasses import dataclass
import datetime
import typing


@dataclass
class BPSeries:
    meta: BPSeriesMetadata
    series_systolic: typing.List[float]
    series_diastolic: typing.List[float]
    series_avg: typing.List[float]
    mins_since_start: typing.List[int]
    timestamps: typing.List[str]
    indices_systolic: typing.Dict[str, float]
    indices_diastolic: typing.Dict[str, float]
    indices_avg: typing.Dict[str, float]


def bp_series_filter_by_sleep(bp_series_obj: BPSeries, bp_series_list: typing.List[float]):
    ret = []
    for t1, t2 in zip(bp_series_list, bp_series_obj.timestamps):
        point: float = t1
        timestamp: datetime.datetime = t2
        if timestamp.hour >= 22 or timestamp.hour < 6:
            ret.append(point)
    return ret


def bp_series_filter_by_wake(bp_series_obj, bp_series_list):
    ret = []
    for t1, t2 in zip(bp_series_list, bp_series_obj.timestamps):
        point: float = t1
        timestamp: datetime.datetime = t2
        if not(timestamp.hour >= 22 or timestamp.hour < 6):
            ret.append(point)
    return ret


