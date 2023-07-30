import itertools
import typing

import src.registry as reg


def parse_index_path(path: str) -> typing.Tuple[str, str]:
    split = [s.strip() for s in path.split("/")]
    return split[0], split[1]


def list_or_str_to_strlist(arg):
    if isinstance(arg, str):
        return [arg]
    if isinstance(arg, list):
        return arg
    return None


def type_satisfies_rule(dtype: reg.ExtractedDataType, rule: str) -> bool:
    if rule == "all":
        return True
    if rule.startswith("tag:"):
        tagname = rule.split(":")[1]
        return tagname in dtype.tags
    return rule == dtype.name


def index_applies_to_extractor(index_name: str, extractor_name: str) -> bool:
    idx = reg.patient_indices_registry[index_name]
    extractor = reg.series_extractor_registry[extractor_name]
    data_type = extractor.type
    rules = list_or_str_to_strlist(idx.applicable_to)
    return any(type_satisfies_rule(data_type, rule) for rule in rules)


def create_combination_paths(extractors: typing.List[str], indices: typing.List[str]):
    result = []
    for extractor, index in itertools.product(extractors, indices):
        if index_applies_to_extractor(index, extractor):
            result.append("{}/{}".format(extractor, index))
    return result
