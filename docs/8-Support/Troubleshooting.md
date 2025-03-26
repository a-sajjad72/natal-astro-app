# 🚨 Troubleshooting Guide

## Common Errors

### 1. Location Data Not Loading
**Symptoms**:
- Empty dropdowns
- Console errors like `Failed to fetch`

**Solutions**:
```javascript
// Verify service account permissions
1. Check Sheets → Share → service-account@project.iam.gserviceaccount.com has Editor access
2. Validate spreadsheet ID in .env:
   LOCATION_SPREADSHEET_ID="1XyZ..." // Must match exactly
```

### 2. Astro Calculations Failing
**Error Patterns**:
```python
swisseph.Error: SwissEph file 'sepl_18.se1' not found
```
**Fix**:
```bash
# Reinstall Swiss Ephemeris
pip uninstall pyswisseph -y
pip install git+https://github.com/astrorigin/pyswisseph@master
```

## Log Interpretation

### Key Log Patterns
| Log Message | Severity | Action |
|-------------|----------|--------|
| `Sheets API 403` | Critical | Verify service account credentials |
| `Ephemeris JD out of range` | Warning | Check birth date validity |
| `Location cache miss` | Info | Normal first-load behavior |

## Debug Tools

### 1. Diagnostic Endpoints
```bash
# Health check (added in v1.2)
curl http://localhost:8000/health
# Expected: {"status":"ok","sheets_accessible":true}
```

### 2. Manual Data Inspection
```python
# Python shell debugging
from gsheets.locations import fetch_locations
print(fetch_locations()[:2])  # Check first 2 locations
```

---

## Error Code Reference
| HTTP Code | Meaning | Next Steps |
|-----------|---------|------------|
| 422 | Validation Error | Check request body schema |
| 503 | Sheets Unavailable | Retry + verify API quotas |
| 504 | Calculation Timeout | Reduce ephemeris scope |

**See Also**: [API Error Responses](../5-API-Reference.md#error-responses)