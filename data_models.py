# Standard
from datetime import date
# Third Party
from typing import List, Optional
from fastapi import Query
from pydantic.main import BaseModel


class SubmitRates(BaseModel):
    date_from: date = Query(..., title="")
    date_to: date = Query(..., title="")
    origin: str = Query(..., title="")
    destination: str = Query(..., title="")
    price: float = Query(..., title="")
    currency_code: Optional[str] = ''


class SearchResponse(BaseModel):
    result: List[dict] = Query(..., example=[
        {
            "day": "2016-01-01",
            "average_price": 129
        },
        {
            "day": "2016-01-02",
            "average_price": 139
        },
    ])


class UploadResponse(BaseModel):
    result: List[dict] = Query(..., example=[
        {   "origin": "",
            "destination": "",
            "day": "2016-01-01",
            "price": 129.00
        }

    ])