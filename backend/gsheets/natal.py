from config import settings
from fastapi import Request


def update_input_sheet(service, data):
    """Overwrite entire Input sheet with new data (without headers)"""
    # Clear existing data
    service.spreadsheets().values().clear(
        spreadsheetId=settings.natal_spreadsheet_id, range="Input!A:B"
    ).execute()

    # Write new data starting at A1
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=settings.natal_spreadsheet_id,
            range="Input!A1",
            valueInputOption="RAW",
            body={"values": data},
        )
        .execute()
    )
    return result


def fetch_output_data(service):
    """Fetch data from 'Output' sheet."""
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=settings.natal_spreadsheet_id, range="Output!B1:C10")
        .execute()
    )
    return result.get("values", [])
