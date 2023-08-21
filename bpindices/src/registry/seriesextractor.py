import typing
from dataclasses import dataclass
import numpy as np

import src.registry.basicregistry as registry
from src.registry.extracteddatatype import ExtractedDataType, extracted_data_type_registry


@dataclass
class SeriesExtractor:
    name: str
    display_name: str
    type: ExtractedDataType
    extractor: typing.Callable


arr_series_extractor_registry = [
    SeriesExtractor(
        name="bp_sys",
        display_name="Systolic blood pressure",
        type=extracted_data_type_registry["blood_pressure"],
        extractor=lambda ses: (ses.series_systolic,)
    ),
    SeriesExtractor(
        name="bp_dia",
        display_name="Diastolic blood pressure",
        type=extracted_data_type_registry["blood_pressure"],
        extractor=lambda ses: (ses.series_diastolic,)
    ),
    SeriesExtractor(
        name="bp_avg",
        display_name="Average blood pressure",
        type=extracted_data_type_registry["blood_pressure"],
        extractor=lambda ses: (((2 / 3) * np.array(ses.series_diastolic) + (1 / 3) * np.array(ses.series_systolic)),)
    ),
    SeriesExtractor(
        name="bp_diff",
        display_name="Systolic minus diastolic",
        type=extracted_data_type_registry["blood_pressure"],
        extractor=lambda ses: ((np.array(ses.series_systolic) - np.array(ses.series_diastolic)),)
    ),
    SeriesExtractor(
        name="bpm",
        display_name="Beats per minute",
        type=extracted_data_type_registry["beats_per_minute"],
        extractor=lambda ses: (ses.series_bpm,)
    ),
    SeriesExtractor(
        name="metadata",
        display_name="Patient and session data",
        type=extracted_data_type_registry["session_data"],
        extractor=lambda ses: (ses.meta,)
    ),

]

series_extractor_registry: typing.Dict[str, SeriesExtractor] = registry.create_registry(arr_series_extractor_registry)
