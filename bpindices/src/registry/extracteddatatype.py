import typing
from dataclasses import dataclass

import numpy as np

import src.registry.basicregistry as registry


@dataclass
class ExtractedDataType:
    name: str
    datatype: typing.Type


extracted_data_type_registry: typing.Dict[str, ExtractedDataType] = registry.create_registry([
    ExtractedDataType(
        name="blood_pressure",
        datatype=typing.Tuple[np.ndarray]
    ),
    ExtractedDataType(
        name="beats_per_minute",
        datatype=typing.Tuple[np.ndarray]
    )
])
