# backend/gsheets/userdata.py

from config import settings


def update_userdata_sheet(service, data):
    """
    Update the Userdata sheet with new user data.
    If a user with the same email already exists, update their data;
    otherwise, append a new row.
    """
    sheet_name = "Userdata"
    headers = [
        "Name",
        "Email",
        "Date of Birth",
        "Time of Birth",
        "Country",
        "State",
        "City",
        "Mobile Number",
    ]

    # Fetch existing data
    existing_data = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=settings.natal_spreadsheet_id, range=f"{sheet_name}!A:H")
        .execute()
    )
    existing_values = existing_data.get("values", [])

    # Prepare data to be written
    new_row = [data[header] for header in headers]

    # Check if headers exist, if not, add them
    if not existing_values:
        existing_values.append(headers)

    # Check if email exists and update or append
    email_index = headers.index("Email")
    email_exists = False
    for i, row in enumerate(existing_values[1:]):  # Skip headers
        if row[email_index] == data["Email"]:
            existing_values[i + 1] = new_row
            email_exists = True
            break

    if not email_exists:
        existing_values.append(new_row)

    # Clear existing data
    service.spreadsheets().values().clear(
        spreadsheetId=settings.natal_spreadsheet_id, range=f"{sheet_name}!A:H"
    ).execute()

    # Write new data
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=settings.natal_spreadsheet_id,
            range=f"{sheet_name}!A1",
            valueInputOption="RAW",
            body={"values": existing_values},
        )
        .execute()
    )
    return result
