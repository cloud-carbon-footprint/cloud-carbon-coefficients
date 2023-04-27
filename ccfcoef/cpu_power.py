from dataclasses import dataclass


@dataclass
class CPUPower:
    min_watts: float
    max_watts: float
    gb_chip: float
    cpu_info: list
    max_watts_gcp_adjusted: float = None
