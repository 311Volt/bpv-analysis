import numpy as np

from src.txrsession import TxrSession

import typing
import pandas as pd
import src.registry as reg


def filter_sessions(
        sessions: typing.List[TxrSession],
        active_filter_names: typing.List[str]
) -> typing.List[TxrSession]:
    ret = sessions
    active_filters = [reg.session_filter_registry[name] for name in active_filter_names]
    for flt in active_filters:
        ret = [session for session in sessions if flt.predicate(session)]
    return ret


def extract_series(session: TxrSession, extractor_name: str):
    extractor = reg.series_extractor_registry[extractor_name]
    return np.array(extractor.extractor(session), dtype=np.float32)


def create_data_frame(
        sessions: typing.List[TxrSession],
        filter_names: typing.List[str],
        index_paths: typing.List[str]
) -> pd.DataFrame:
    filtered_sessions = filter_sessions(sessions, filter_names)

    extractor_names = [s.split("/")[0] for s in index_paths]
    extractor_names_set = set(extractor_names)
    index_names = [s.split("/")[1] for s in index_paths]

    matrix = np.zeros((len(filtered_sessions), len(index_paths)), dtype=np.float32)

    for sesidx, session in enumerate(filtered_sessions):
        all_series = {extractor_name: extract_series(session, extractor_name) for extractor_name in extractor_names_set}
        for pathidx, pathname in enumerate(index_names):
            series = all_series[extractor_names[pathidx]]
            matrix[(sesidx, pathidx)] = reg.patient_indices_registry[index_names[pathidx]].calc_fn(*series)

    return pd.DataFrame(matrix, columns=index_paths, copy=True, dtype=np.float32)
