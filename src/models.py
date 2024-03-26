from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database import BaseModel


class LocationsOrm(BaseModel):
    __tablename__ = 'locations'
    id: Mapped[int] = mapped_column(primary_key=True)
    location: Mapped[str]
    population: Mapped[int] = mapped_column(BigInteger)
    percent_of_the_world: Mapped[str]
    last_updated: Mapped[str]
    source_of_data: Mapped[str]
