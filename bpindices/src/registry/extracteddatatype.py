import typing
from dataclasses import dataclass

import numpy as np

import src.registry.basicregistry as registry
from src.txrsessionmetadata import TxrSessionMetadata


@dataclass
class ExtractedDataType:
    name: str
    tags: typing.Set[str]
    datatype: typing.Type


arr_extracted_data_type_registry = [
    ExtractedDataType(
        name="blood_pressure",
        tags={"num_series"},
        datatype=typing.Tuple[np.ndarray]
    ),
    ExtractedDataType(
        name="beats_per_minute",
        tags={"num_series"},
        datatype=typing.Tuple[np.ndarray]
    ),
    ExtractedDataType(
        name="session_data",
        tags=set(),
        datatype=typing.Tuple[TxrSessionMetadata]
    )
]

extracted_data_type_registry: typing.Dict[str, ExtractedDataType] \
    = registry.create_registry(arr_extracted_data_type_registry)
