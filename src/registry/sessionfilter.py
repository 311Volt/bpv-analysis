import typing
from dataclasses import dataclass

import src.registry.basicregistry as registry
from src.txrsession import TxrSession


@dataclass
class SessionFilter:
    name: str
    display_name: str
    predicate: typing.Callable[[TxrSession], bool]


arr_session_filter_registry = [
    SessionFilter(
        name="age_valid",
        display_name="Age Valid",
        predicate=lambda ses: ses.meta.age < 100
    ),
    SessionFilter(
        name="gender_male",
        display_name="Gender Male",
        predicate=lambda ses: ses.meta.gender == "male"
    ),
    SessionFilter(
        name="gender_female",
        display_name="Gender Female",
        predicate=lambda ses: ses.meta.gender == "female"
    ),
    SessionFilter(
        name="age_group_0",
        display_name="Ages 0-29",
        predicate=lambda ses: ses.meta.age <= 29
    ),
    SessionFilter(
        name="age_group_1",
        display_name="Ages 29-54",
        predicate=lambda ses: 29 <= ses.meta.age <= 54
    ),
    SessionFilter(
        name="age_group_2",
        display_name="Ages 55+",
        predicate=lambda ses: ses.meta.age >= 55
    )
]

session_filter_registry: typing.Dict[str, SessionFilter] = registry.create_registry(arr_session_filter_registry)
