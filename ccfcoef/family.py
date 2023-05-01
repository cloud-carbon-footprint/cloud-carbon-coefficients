from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Family:
    name: str
    short: str
