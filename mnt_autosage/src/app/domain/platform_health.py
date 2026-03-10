from dataclasses import dataclass


@dataclass
class PlatformServiceHealth:

    service_name: str
    status: str


@dataclass
class PlatformHealth:

    services: list[PlatformServiceHealth]
