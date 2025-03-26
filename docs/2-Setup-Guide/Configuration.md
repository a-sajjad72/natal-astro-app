# ⚙️ Configuration

## 1. Environment Variables
Create `.env` in project root:
```ini
# Required
GOOGLE_SERVICE_ACCOUNT_FILE="env/service-account.json"
LOCATION_SPREADSHEET_ID="your-locations-sheet-id"
NATAL_SPREADSHEET_ID="your-natal-sheet-id"
```

## 2. Service Account Setup
1. Place your `service-account.json` in `/env/`
2. Verify file structure:
   ```json
   {
     "type": "service_account",
     "project_id": "...",
     "private_key_id": "...",
     "private_key": "-----BEGIN PRIVATE KEY-----\n...",
     "client_email": "...@...iam.gserviceaccount.com",
     "client_id": "..."
   }
   ```

## 3. Sheet Preparation
### Locations Sheet
- **Required Columns** (case-sensitive):
  ```csv
  city,state,country,latitude,longitude
  ```
- **Example Row**:
  ```csv
  Mumbai,Maharashtra,India,19.0760,72.8777
  ```

### Natal Sheet
- **Input Tab**:
  ```csv
  name,date,time,latitude,longitude
  ```
- **Output Tab**:
  ```csv
  lagna,sun,moon,... (auto-generated)
  ```

## Test Configuration
```bash
python -c "from config import settings; print(settings.location_spreadsheet_id)"
```
✅ Should print your spreadsheet ID without errors