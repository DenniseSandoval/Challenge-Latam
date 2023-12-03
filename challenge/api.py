import logging
import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Union

import fastapi
import pandas as pd
from pydantic import BaseModel, ValidationError
from challenge.enums import Airlines, FlightTypes, Months

from challenge.model import DelayModel


app = fastapi.FastAPI()


class Flight(BaseModel):
    OPERA: Airlines
    TIPOVUELO: FlightTypes
    MES: Months


class Flights(BaseModel):
    flights: List[Flight]


@app.on_event("startup")
async def startup_event():
    data_path = Path(os.getcwd(), "data/data.csv")
    data = pd.read_csv(filepath_or_buffer=data_path)
    delay_model = DelayModel()
    features_train, target = delay_model.preprocess(data, "delay")
    delay_model.fit(features_train, target)


@app.get("/health", status_code=200)
async def get_health() -> Dict[str, str]:
    return {"status": "OK"}


@app.post("/predict", status_code=200)
async def post_predict(
    data_payload: Dict[str, List[Dict[str, str]]]
) -> Dict[str, Union[str, List[int]]]:
    try:
        Flights.parse_obj(data_payload)
    except ValidationError:
        return fastapi.responses.JSONResponse(
            {"error": "unknown object received"}, status_code=400
        )

    delay_model = DelayModel()
    request_df = pd.DataFrame(data_payload["flights"])
    features = delay_model.preprocess(request_df)
    return {"predict": delay_model.predict(features)}
