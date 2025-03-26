# backend/routes/submit.py

import csv
import traceback
from io import StringIO

import pandas as pd
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.gsheets.natal import fetch_output_data, update_input_sheet
from backend.gsheets.userdata import update_userdata_sheet
from backend.routes.locations import get_coordinates
from backend.services.astrology_service import AstrologyService

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")


@router.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    fullName: str = Form(...),
    email: str = Form(...),
    dateOfBirth: str = Form(...),
    timeOfBirth: str = Form(...),
    country: str = Form(...),
    state: str = Form(...),
    city: str = Form(...),
    mobileNumber: str = Form(...),
):
    # Get coordinates from locations.json
    latitude, longitude = get_coordinates(city, state, country, request)

    birth_data = {
        "name": fullName,
        "date": dateOfBirth,
        "time": timeOfBirth,
        "latitude": latitude,
        "longitude": longitude,
        "location": {"country": country, "state": state, "city": city},
        "timezone_offset": 5.5,
    }

    # Update Userdata sheet
    update_userdata_sheet(
        request.app.state.gsheet_service,
        {
            "Name": fullName,
            "Email": email,
            "Date of Birth": dateOfBirth,
            "Time of Birth": timeOfBirth,
            "Country": country,
            "State": state,
            "City": city,
            "Mobile Number": mobileNumber,
        },
    )

    service = AstrologyService(birth_data)
    result_csv = service.generate_csv()

    result_csv = service.generate_csv()
    csv_rows = list(csv.reader(StringIO(result_csv.strip())))

    # Insert data Input sheet
    update_input_sheet(request.app.state.gsheet_service, csv_rows[1:])

    # Fetch output data from Output sheet
    output_data = fetch_output_data(request.app.state.gsheet_service)
    output_data = pd.DataFrame(output_data).map(lambda x: "" if x is None else x)
    print(output_data)

    return f"""
        <html>
          <body class="bg-green-100 p-4">
            <!-- ... existing success data ... -->
            <p class="text-green-800">Output Data: {pd.DataFrame(output_data).to_html()}</p>
          </body>
        </html>
        """


"fullName", "email", "dateOfBirth", "timeOfBirth", "country", "state", "city", "mobileNumber"
