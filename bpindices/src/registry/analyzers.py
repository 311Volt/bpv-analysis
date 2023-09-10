import typing
from dataclasses import dataclass
import src.registry.basicregistry as registry

import src.analyzers as analyzers


@dataclass
class AnalyzerDescription:
    name: str
    display_name: str
    clazz: typing.Type


arr_analyzer_registry = [
    AnalyzerDescription(
        name="correlation",
        display_name="Correlation",
        clazz=analyzers.CorrelationAnalyzer
    ),
    AnalyzerDescription(
        name="histogram",
        display_name="Histogram",
        clazz=analyzers.HistogramAnalyzer
    ),
    AnalyzerDescription(
        name="shapiro",
        display_name="Shapiro test",
        clazz=analyzers.ShapiroAnalyzer
    )
]


analyzer_registry: typing.Dict[str, AnalyzerDescription] \
    = registry.create_registry(arr_analyzer_registry)