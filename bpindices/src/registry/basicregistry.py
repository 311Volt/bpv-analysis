import typing


def create_registry(items: typing.List) -> dict:
    return {item.name: item for item in items}
