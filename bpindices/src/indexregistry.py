import typing

import indexfunctions as idxfn
from dataclasses import dataclass
from enum import Enum

import registry


@dataclass
class PatientIndex:
    name: str
    display_name: str
    applicable_to: typing.Any
    calc_fn: typing.Callable


patient_indices_registry = registry.create_registry([
    PatientIndex(
        name="residual_variability",
        display_name="Residual variability",
        applicable_to="all",
        calc_fn=idxfn.idx_residual_variability
    ),
    PatientIndex(
        name="mean",
        display_name="Mean value",
        applicable_to="all",
        calc_fn=idxfn.idx_mean
    ),
    PatientIndex(
        name="entropy",
        display_name="Entropy (WIP)",
        applicable_to="all",
        calc_fn=idxfn.idx_entropy
    ),
    PatientIndex(
        name="stddev",
        display_name="Standard deviation",
        applicable_to="all",
        calc_fn=idxfn.idx_standard_deviation
    ),
    PatientIndex(
        name="coeff_var",
        display_name="Coefficient of variation",
        applicable_to="all",
        calc_fn=idxfn.idx_coeff_of_variation
    ),
    PatientIndex(
        name="arv",
        display_name="Average real variability",
        applicable_to="all",
        calc_fn=idxfn.idx_arv
    ),
    PatientIndex(
        name="range",
        display_name="Range",
        applicable_to="all",
        calc_fn=idxfn.idx_range
    ),
    PatientIndex(
        name="peak",
        display_name="Peak",
        applicable_to="all",
        calc_fn=idxfn.idx_peak
    ),
    PatientIndex(
        name="through",
        display_name="Through",
        applicable_to="all",
        calc_fn=idxfn.idx_through
    ),
    PatientIndex(
        name="max",
        display_name="Highest value",
        applicable_to="all",
        calc_fn=idxfn.idx_max
    ),
    PatientIndex(
        name="min",
        display_name="Lowest value",
        applicable_to="all",
        calc_fn=idxfn.idx_min
    ),

])


def calculate_index(bp_series: idxfn.BPSeriesArray, idxname: str) -> float:
    return float(patient_indices_registry[idxname].calc_fn(bp_series))


def all_indices(bp_series: idxfn.BPSeriesArray):
    return {idx: calculate_index(bp_series, idx.name) for idx in patient_indices_registry.values()}
