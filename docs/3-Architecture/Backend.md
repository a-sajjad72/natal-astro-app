# ⚙️ Backend Architecture

## Service Layers
| Layer | Module | Responsibility |
|-------|--------|----------------|
| **API** | `routes/*.py` | HTTP endpoint handling |
| **Core Logic** | `services/astrology_service.py` | Chart calculations |
| **Integrations** | `gsheets/*.py` | Google Sheets interaction |

## Key Components
### 1. Astrology Service
- **Input**: Birth data (datetime, location)
- **Output**: Planetary positions, Sahams, Panchang
- **Dependencies**:
  ```python
  import swisseph as swe  # v2.10+
  import ephem
  ```

### 2. Google Sheets Adapter
```python
# Example: Fetching locations
def fetch_locations_from_gsheet(service):
    result = service.spreadsheets().values().get(
        spreadsheetId=settings.location_spreadsheet_id,
        range="Sheet1!A:E"
    ).execute()
    return result.get('values', [])
```

## Concurrency Model
- Synchronous processing (FastAPI default)
- Heavy calculations (e.g., Sahams) are CPU-bound
- Consider async for >100 concurrent users

## Error Handling
- Custom exceptions in `services/exceptions.py`
- HTTP status codes:
  - `422` for validation errors
  - `503` if Sheets API unavailable
