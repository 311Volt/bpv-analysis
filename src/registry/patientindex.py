import re
import typing
from dataclasses import dataclass

import src.indexfunctions as idxfn
import src.registry.basicregistry as registry


@dataclass
class PatientIndex:
    name: str
    display_name: str
    applicable_to: typing.Any
    calc_fn: typing.Callable


arr_patient_indices_registry = [
    PatientIndex(
        name="mean",
        display_name="Mean value",
        applicable_to="tag:num_series",
        calc_fn=idxfn.idx_mean
    ),
    PatientIndex(
        name="stddev",
        display_name="Standard deviation",
        applicable_to="tag:num_series",
        calc_fn=idxfn.idx_standard_deviation
    ),
    PatientIndex(
        name="arv",
        display_name="Average real variability",
        applicable_to="tag:num_series",
        calc_fn=idxfn.idx_arv
    ),
    PatientIndex(
        name="residual_variability",
        display_name="Residual variability",
        applicable_to="tag:num_series",
        calc_fn=idxfn.idx_residual_variability
    ),
    PatientIndex(
        name="entropy",
        display_name="Entropy (WIP)",
        applicable_to="tag:num_series",
        calc_fn=idxfn.idx_entropy
    ),
    PatientIndex(
        name="coeff_var",
        display_name="Coefficient of variation",
        applicable_to="tag:num_series",
        calc_fn=idxfn.idx_coeff_of_variation
    ),
    PatientIndex(
        name="range",
        display_name="Range",
        applicable_to="tag:num_series",
        calc_fn=idxfn.idx_range
    ),
    PatientIndex(
        name="peak",
        display_name="Peak",
        applicable_to="tag:num_series",
        calc_fn=idxfn.idx_peak
    ),
    PatientIndex(
        name="through",
        display_name="Through",
        applicable_to="tag:num_series",
        calc_fn=idxfn.idx_through
    ),
    PatientIndex(
        name="max",
        display_name="Highest value",
        applicable_to="tag:num_series",
        calc_fn=idxfn.idx_max
    ),
    PatientIndex(
        name="min",
        display_name="Lowest value",
        applicable_to="tag:num_series",
        calc_fn=idxfn.idx_min
    ),
    PatientIndex(
        name="age",
        display_name="Age",
        applicable_to="session_data",
        calc_fn=lambda meta: meta.age
    ),
    PatientIndex(
        name="patient_id",
        display_name="Patient ID",
        applicable_to="session_data",
        calc_fn=lambda meta: re.search('[0-9]+', meta.id).group()
    )
]


patient_indices_registry: typing.Dict[str, PatientIndex] = registry.create_registry(arr_patient_indices_registry)
