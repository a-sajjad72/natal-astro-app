# backend/gsheets/locations.py

from config import settings

def fetch_locations_from_gsheet(service, range_name=None):
    sheet = service.spreadsheets()

    # If no range is provided use the first sheet's entire data
    if range_name is None:
        # Retrieve metadata for the spreadsheet
        spreadsheet = (
            service.spreadsheets()
            .get(spreadsheetId=settings.location_spreadsheet_id)
            .execute()
        )
        # Get the title of the first sheet
        sheet_title = spreadsheet["sheets"][0]["properties"]["title"]
        range_name = sheet_title

    result = (
        sheet.values()
        .get(spreadsheetId=settings.location_spreadsheet_id, range=range_name)
        .execute()
    )
    values = result.get("values", [])
    if not values:
        return []

    # As the first row contains headers
    headers = [h.lower() for h in values[0]]
    locations = []
    for row in values[1:]:
        entry = {
            headers[i]: row[i] if i < len(row) else "" for i in range(len(headers))
        }
        locations.append(entry)
    return locations
