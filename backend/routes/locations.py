# backend/routes/locations.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from backend.gsheets.locations import fetch_locations_from_gsheet
import json
import pandas as pd

router = APIRouter()


@router.get("/locations")
async def get_locations(request: Request):
    gsheet_service = request.app.state.gsheet_service
    locations_data = pd.DataFrame(fetch_locations_from_gsheet(gsheet_service))
    locations_data.columns = [col.strip().lower() for col in locations_data.columns]
    return JSONResponse(content=json.loads(locations_data.to_json(orient="records")))


def get_coordinates(city: str, state: str, country: str, request: Request) -> dict:
    try:
        gsheet_service = request.app.state.gsheet_service
        locations_df = pd.DataFrame(fetch_locations_from_gsheet(gsheet_service))
        locations_df.columns = [col.strip().lower() for col in locations_df.columns]
        for index, location in locations_df.iterrows():
            if (
                location["country"] == country
                and location["state"] == state
                and location["city"] == city
            ):
                return {
                    "latitude": float(location["latitude"]),
                    "longitude": float(location["longitude"]),
                }.values()
    except KeyError:
        raise ValueError(f"Coordinates not found for {city}, {state}, {country}")


# Direct match using form-selected values
