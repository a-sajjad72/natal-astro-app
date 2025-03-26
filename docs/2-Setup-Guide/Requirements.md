# 📋 System Requirements

## Hardware
| Component | Minimum Spec | Recommended |
|-----------|--------------|-------------|
| CPU       | 2 cores      | 4+ cores    |
| RAM       | 4GB          | 8GB         |
| Storage   | 500MB        | 1GB+        |

## Software
### Mandatory
- Python 3.9+ (`python --version`)
- Google Cloud Service Account
- Google Sheets with:
  - **Locations Sheet**: 
    ```csv
    city,state,country,latitude,longitude
    ```
  - **Natal Sheet**: `Input` and `Output` tabs

### Recommended Tools
- VS Code (with Python extension)
- Postman (for API testing)
- ngrok (for temporary webhooks)

## Account Prerequisites
1. **Google Cloud**:
   - Enable [Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com)
   - Create service account with **Editor** permissions
2. **Spreadsheets**:
   - Share both sheets with your service account email
   - Format as shown in [Data Structure Guide](../4-Code-Guides/Google-Sheets-API.md#data-structure)

> 🔍 **Verification Checklist**:
> - [ ] `python3 --version` returns 3.9+
> - [ ] Service account JSON file exists
> - [ ] Sheets are shared correctly