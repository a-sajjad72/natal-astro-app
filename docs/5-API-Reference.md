# 🔌 API Reference

## Base URL
`https://api.natalastro.com/v1` *(or `http://localhost:8000` for local dev)*

## Authentication
No auth required for these endpoints (public API)

---

## 🌐 Endpoints

### 1. `GET /locations`
**Description**: Fetch all available locations  
**Response**:
```json
[
  {
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": "India",
    "latitude": 19.0760,
    "longitude": 72.8777
  }
]
```

**Example**:
```bash
curl -X GET http://localhost:8000/locations
```

---

### 2. `POST /submit`
**Description**: Submit birth data for chart calculation  

**Request Body**:
```json
{
  "fullName": "Rahul Sharma",
  "email": "user@example.com",
  "dateOfBirth": "1990-05-15",
  "timeOfBirth": "08:30",
  "country": "India",
  "state": "Maharashtra",
  "city": "Mumbai",
  "mobileNumber": "+911234567890"
}
```

**Success Response** (`200 OK`):
```html
<html>
  <body>
    <div class="report">
      <h2>Rahul Sharma's Birth Chart</h2>
      <table>
        <tr><th>Lagna</th><td>12.34°</td></tr>
        <!-- ... -->
      </table>
    </div>
  </body>
</html>
```

**Error Responses**:
| Code | Scenario | Response Body |
|------|----------|---------------|
| `422` | Validation Error | `{"detail":[{"loc":["body","dateOfBirth"],"msg":"invalid date format"}]}` |
| `503` | Sheets API Down | `{"detail":"Google Sheets service unavailable"}` |

---

## 🛠️ Developer Notes

### Rate Limits
- `10 requests/minute` per IP address
- Headers returned:
  ```http
  X-RateLimit-Limit: 10
  X-RateLimit-Remaining: 9
  ```

### Testing with Postman
1. Import [Postman Collection](#) *(placeholder link)*
2. Set environment variables:
   ```json
   {
     "baseUrl": "http://localhost:8000",
     "testUserId": "demo123"
   }
   ```

### SDK Examples
**Python Client**:
```python
import requests

def get_locations():
    response = requests.get("http://localhost:8000/locations")
    return response.json()

def submit_chart_request(data):
    headers = {"Content-Type": "application/json"}
    return requests.post(
        "http://localhost:8000/submit", 
        json=data, 
        headers=headers
    )
```

---

## 📡 Webhook Support *(Future)*
Planned for v2:
```json
{
  "event": "chart_processed",
  "webhook_url": "https://your-domain.com/callback"
}
```

---

**See Also**:  
- [Architecture Data Flow](../3-Architecture/Data-Flow.md)  
- [Error Handling Guide](../8-Support/Troubleshooting.md#api-errors)  