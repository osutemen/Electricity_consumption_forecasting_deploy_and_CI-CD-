from typing import Optioselectnal, List
from datetime import datetime

from fastapi import Form
from sqlmodel import SQLModel, Field


class DailyEnergyConsumption(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    Date: str
    prediction: str


class HourlyEnergyConsumption(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    Date: str
    prediction: str



class CreateUpdateEnergy(SQLModel):
    Date: str

    class Config:
        schema_extra = {
            "example": {
                "Date": '23.07.2024 10:00'
            }
        }

class sle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    Datetime: str
    Tuketim: float


class ElectricDriftInput(SQLModel):
    last_n_values: int

    class Config:
        schema_extra = {
            "example": {
                "last_n_values": 5,
            }
        }
