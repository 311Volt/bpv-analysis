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
        extractor_name: str,
        filter_names: typing.List[str],
        index_names: typing.List[str]
) -> pd.DataFrame:
    filtered_sessions = filter_sessions(sessions, filter_names)

    matrix = np.zeros((len(filtered_sessions), len(index_names)), dtype=np.float32)

    for sesidx, session in enumerate(filtered_sessions):
        series = extract_series(session, extractor_name)
        for idxidx, idxname in enumerate(index_names):
            matrix[(sesidx, idxidx)] = reg.patient_indices_registry[idxname].calc_fn(*series)

    return pd.DataFrame(matrix, columns=index_names, copy=True, dtype=np.float32)
