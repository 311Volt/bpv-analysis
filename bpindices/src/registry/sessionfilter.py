import typing
from dataclasses import dataclass

import src.registry.basicregistry as registry
from src.txrsession import TxrSession


@dataclass
class SessionFilter:
    name: str
    display_name: str
    predicate: typing.Callable[[TxrSession], bool]


session_filter_registry: typing.Dict[str, SessionFilter] = registry.create_registry([
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
    )
])

arr_session_filter_registry = list(session_filter_registry.values())
