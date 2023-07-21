
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
    series_bpm: typing.List[float]
    mins_since_start: typing.List[int]
    timestamps: typing.List[str]
