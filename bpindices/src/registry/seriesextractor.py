import typing
from dataclasses import dataclass

import src.registry.basicregistry as registry
from src.registry.extracteddatatype import ExtractedDataType, extracted_data_type_registry


@dataclass
class SeriesExtractor:
    name: str
    type: ExtractedDataType
    extractor: typing.Callable


series_extractor_registry: typing.Dict[str, SeriesExtractor] = registry.create_registry([
    SeriesExtractor(
        name="bp_systolic",
        type=extracted_data_type_registry["blood_pressure"],
        extractor=lambda ses: (ses.series_systolic,)
    ),
    SeriesExtractor(
        name="bp_diastolic",
        type=extracted_data_type_registry["blood_pressure"],
        extractor=lambda ses: (ses.series_diastolic,)
    ),
    SeriesExtractor(
        name="bp_avg",
        type=extracted_data_type_registry["blood_pressure"],
        extractor=lambda ses: (((2 / 3) * ses.series_diastolic + (1 / 3) * ses.series_systolic),)
    ),
    SeriesExtractor(
        name="bp_diff",
        type=extracted_data_type_registry["blood_pressure"],
        extractor=lambda ses: ((ses.series_systolic - ses.series_diastolic),)
    ),
    SeriesExtractor(
        name="bpm",
        type=extracted_data_type_registry["beats_per_minute"],
        extractor=lambda ses: (ses.series_bpm,)
    ),

])
