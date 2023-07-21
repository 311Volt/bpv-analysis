from dataclasses import dataclass

import numpy as np

import src.indexregistry
from txrsession import TxrSession
import typing
import registry
import indexregistry
import pandas as pd


@dataclass
class ExtractedDataType:
    name: str
    datatype: typing.Type


@dataclass
class SessionFilter:
    name: str
    predicate: typing.Callable[[TxrSession], bool]


@dataclass
class SeriesExtractor:
    name: str
    type: ExtractedDataType
    extractor: typing.Callable


extracted_data_type_registry = registry.create_registry([
    ExtractedDataType(
        name="blood_pressure",
        datatype=np.ndarray
    ),
    ExtractedDataType(
        name="beats_per_minute",
        datatype=np.ndarray
    )
])

session_filter_registry = registry.create_registry([
    SessionFilter(
        name="age_valid",
        predicate=lambda ses: ses.meta.age < 100
    ),
    SessionFilter(
        name="gender_male",
        predicate=lambda ses: ses.meta.gender == "male"
    ),
    SessionFilter(
        name="gender_female",
        predicate=lambda ses: ses.meta.gender == "female"
    )
])

series_extractor_registry = registry.create_registry([
    SeriesExtractor(
        name="bp_systolic",
        type=extracted_data_type_registry["blood_pressure"],
        extractor=lambda ses: ses.series_systolic
    ),
    SeriesExtractor(
        name="bp_diastolic",
        type=extracted_data_type_registry["blood_pressure"],
        extractor=lambda ses: ses.series_diastolic
    ),
    SeriesExtractor(
        name="bp_avg",
        type=extracted_data_type_registry["blood_pressure"],
        extractor=lambda ses: ((2 / 3) * ses.series_diastolic + (1 / 3) * ses.series_systolic)
    ),
    SeriesExtractor(
        name="bp_diff",
        type=extracted_data_type_registry["blood_pressure"],
        extractor=lambda ses: (ses.series_systolic - ses.series_diastolic)
    ),
    SeriesExtractor(
        name="bpm",
        type=extracted_data_type_registry["beats_per_minute"],
        extractor=lambda ses: ses.series_bpm
    ),

])

SessionFilter = typing.Callable[[typing.List[TxrSession]], typing.List[TxrSession]]
SeriesExtractor = typing.Callable[[TxrSession], typing.List[float]]

ses_filters: typing.Dict[str, SessionFilter] = {
    "age_valid": lambda sessions: [s for s in sessions if s.meta.age < 100],
    "gender_male": lambda sessions: [s for s in sessions if s.meta.gender == "male"],
    "gender_female": lambda sessions: [s for s in sessions if s.meta.gender == "female"]
}

series_extractors: typing.Dict[str, SeriesExtractor] = {
    "systolic": lambda ses: ses.series_systolic,
    "diastolic": lambda ses: ses.series_diastolic,
    "avg": lambda ses: ((2 / 3) * ses.series_diastolic + (1 / 3) * ses.series_systolic),
    "diff": lambda ses: (ses.series_systolic - ses.series_diastolic),
    "bpm": lambda ses: ses.series_bpm
}


def filter_sessions(
        sessions: typing.List[TxrSession],
        active_filters: typing.List[str]
) -> typing.List[TxrSession]:
    ret = sessions
    for filter_name in active_filters:
        ret = ses_filters[filter_name](ret)
    return ret


def extract_series(session: TxrSession, extractor_name: str):
    return np.array(series_extractors[extractor_name](session), dtype=np.float32)


def create_data_frame(
        sessions: typing.List[TxrSession],
        extractor_name: str,
        filter_names: typing.List[str],
        index_names: typing.List[str]
) -> pd.DataFrame:
    filtered_sessions = filter_sessions(sessions, filter_names)

    matrix = np.zeros((len(filtered_sessions), len(index_names)), dtype=np.float32)

    for sesidx, session in enumerate(filtered_sessions):
        bp_series = extract_series(session, extractor_name)
        for idxidx, idxname in enumerate(index_names):
            matrix[(sesidx, idxidx)] = src.indexregistry.calculate_index(bp_series, idxname)

    return pd.DataFrame(matrix, columns=index_names, copy=True, dtype=np.float32)
