
from dataclasses import dataclass
import datetime
import typing
import dateutils
import txrsessionmetadata


@dataclass
class TxrSession:
    meta: txrsessionmetadata.TxrSessionMetadata
    series_systolic: typing.List[float]
    series_diastolic: typing.List[float]
    mins_since_start: typing.List[int]
    timestamps: typing.List[str]


def bp_series_filter_by_sleep(bp_series_obj: TxrSession, bp_series_list: typing.List[float]):
    ret = []
    for t1, t2 in zip(bp_series_list, bp_series_obj.timestamps):
        point: float = t1
        timestamp: datetime.datetime = dateutils.str_to_datetime(t2)
        if timestamp.hour >= 22 or timestamp.hour < 6:
            ret.append(point)
    return ret


def bp_series_filter_by_wake(bp_series_obj, bp_series_list):
    ret = []
    for t1, t2 in zip(bp_series_list, bp_series_obj.timestamps):
        point: float = t1
        timestamp: datetime.datetime = dateutils.str_to_datetime(t2)
        if not (timestamp.hour >= 22 or timestamp.hour < 6):
            ret.append(point)
    return ret
