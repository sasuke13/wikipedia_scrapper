from dataclasses import dataclass


@dataclass(frozen=True)
class RegionDTO:
    location: str
    population: int
    percent_of_the_world: str
    last_updated: str
    source_of_data: str
