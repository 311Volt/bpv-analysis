import typing
from dataclasses import dataclass

import src.analyzers as analyzers
import src.registry.basicregistry as registry


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
    ),
    AnalyzerDescription(
        name="grpcompare",
        display_name="Compare Groups",
        clazz=analyzers.GroupCompareAnalyzer
    ),
    AnalyzerDescription(
        name="agglomerativec",
        display_name="Hierarchical Grouping",
        clazz=analyzers.AgglomerativeClusteringAnalyzer
    ),
    AnalyzerDescription(
        name="kmeans",
        display_name="K-Means",
        clazz=analyzers.KMeansAnalyzer
    ),
    AnalyzerDescription(
        name="pca",
        display_name="PCA",
        clazz=analyzers.PCAAnalyzer
    )
]


analyzer_registry: typing.Dict[str, AnalyzerDescription] \
    = registry.create_registry(arr_analyzer_registry)
