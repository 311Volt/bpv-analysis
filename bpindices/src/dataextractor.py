import numpy as np

from txrsession import TxrSession
import typing
import indices
import pandas as pd

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
    "diff": lambda ses: (ses.series_systolic - ses.series_diastolic)
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
    return series_extractors[extractor_name](session)


def create_data_frame(
        sessions: typing.List[TxrSession],
        extractor_name: str,
        filter_names: typing.List[str],
        index_names: typing.List[str]
) -> pd.DataFrame:
    filtered_sessions = filter_sessions(sessions, filter_names)

    matrix = np.zeros((len(filtered_sessions), len(index_names)), dtype=float)

    for sesidx, session in enumerate(filtered_sessions):
        for idxidx, idxname in enumerate(index_names):
            bp_series = extract_series(session, extractor_name)
            matrix[(sesidx, idxidx)] = indices.calculate_index(bp_series, idxname)

    return pd.DataFrame(matrix, columns=index_names, copy=True, dtype=float)
