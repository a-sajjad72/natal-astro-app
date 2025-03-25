# backend/gsheets/utils.py

from google.oauth2 import service_account
from googleapiclient.discovery import build



def connect_to_gsheet(service_account_file, scopes):
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes
    )
    service = build("sheets", "v4", credentials=credentials)
    return service

