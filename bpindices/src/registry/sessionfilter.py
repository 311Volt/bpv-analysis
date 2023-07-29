import typing
from dataclasses import dataclass

import src.registry.basicregistry as registry
from src.txrsession import TxrSession


@dataclass
class SessionFilter:
    name: str
    predicate: typing.Callable[[TxrSession], bool]


session_filter_registry: typing.Dict[str, SessionFilter] = registry.create_registry([
    SessionFilter(
        name="age_valid",
        predicate=lambda ses: ses.meta.age < 100
    ),
    SessionFilter(
        name="gender_male",
        predicate=lambda ses: ses.meta.gender == "male"
    ),
    SessionFilter(
        name="gender_female",
        predicate=lambda ses: ses.meta.gender == "female"
    )
])
