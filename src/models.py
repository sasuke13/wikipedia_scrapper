from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database import BaseModel


class LocationsOrm(BaseModel):
    __tablename__ = 'locations'
    id: Mapped[int] = mapped_column(primary_key=True)
    location: Mapped[str]
    population_in_2022: Mapped[int] = mapped_column(BigInteger, nullable=True)
    population_in_2023: Mapped[int] = mapped_column(BigInteger, nullable=True)
    change: Mapped[str] = mapped_column(nullable=True)
    region: Mapped[str]
    statistical_subregion: Mapped[str]
