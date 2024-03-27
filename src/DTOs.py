from dataclasses import dataclass


@dataclass(frozen=True)
class RegionDTO:
    location: str
    population_in_2022: int
    population_in_2023: int
    change: str
    region: str
    statistical_subregion: str
