# 📊 Google Sheets Integration

## Key Functions
### `update_input_sheet()`
```python
def update_input_sheet(service, data):
    service.spreadsheets().values().update(
        spreadsheetId=settings.natal_spreadsheet_id,
        range="Input!A1",
        body={'values': data},
        valueInputOption="RAW"
    ).execute()
```

### `fetch_output_data()`
**Response Example**:
```python
{
    "range": "Output!B1:C10",
    "values": [
        ["Lagna", "12.34"],
        ["Sun", "120.5"],
        # ...
    ]
}
```

## Authentication
```python
# utils.py
credentials = service_account.Credentials.from_service_account_file(
    settings.google_service_account_file,
    scopes=settings.google_scopes
)
```

## Error Handling
| Error | Solution |
|-------|----------|
| `403` | Check service account permissions |
| `404` | Verify spreadsheet ID |
| `429` | Implement exponential backoff |

**Rate Limits**:  
- 100 read requests/minute  
- 60 write requests/minute  

**See Also**:  
- [Configuration Guide](../2-Setup-Guide/Configuration.md)  
- [Troubleshooting](../8-Support/Troubleshooting.md#sheets-api)  