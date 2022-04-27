from pydantic import BaseModel
from typing import Optional


class Price(BaseModel):
    price_id: int
    last_updated: str
    time_registered: str
    value: str
    service: Optional[str]

    class Config:
        orm_mode = True