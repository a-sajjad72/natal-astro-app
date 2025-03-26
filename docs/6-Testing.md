# 🧪 Testing Strategy

## 🔬 Test Types
| Type | Scope | Tools | Frequency |
|------|-------|-------|-----------|
| Unit | Individual functions | `pytest` | Pre-commit |
| Integration | API endpoints | `Postman`, `pytest` | Pre-deploy |
| E2E | User flows | `Selenium` | Nightly |

---

## 🚦 Unit Tests
### AstrologyService
```python
# tests/test_astrology_service.py
def test_lagna_calculation():
    birth_data = {..."latitude": 19.0760, "longitude": 72.8777...}
    service = AstrologyService(birth_data)
    assert 0 <= service._calculate_lagna() < 360
```

**Key Test Cases**:
1. Julian Day conversion (timezone handling)
2. Planetary position rounding (12 decimal places)
3. Saham formula validation

---

## 🧩 Integration Tests
### API Test Suite
```bash
pytest tests/api/ -v
```

**Sample Test**:
```python
# tests/api/test_locations.py
def test_locations_endpoint(client):
    response = client.get("/locations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

**Critical Paths**:
1. `POST /submit` with invalid dates
2. Location dropdown sequencing
3. Google Sheets write/read cycle

---

## 🕹️ E2E Testing
### Selenium Script
```python
# tests/e2e/test_form_submission.py
def test_chart_generation(driver):
    driver.select_dropdown("country", "India")
    driver.fill("dateOfBirth", "1990-05-15")
    driver.submit()
    assert "Birth Chart" in driver.page_source
```

**User Journeys**:
1. Happy path submission
2. Location selection → coordinate mapping
3. Mobile responsive validation

---

## 🚨 Error Cases
| Scenario | Expected Behavior |
|----------|-------------------|
| Invalid time format (25:00) | 422 with "Time must be HH:MM" |
| Nonexistent city/state combo | Empty city dropdown |
| Sheets API timeout | 503 + retry button |

---

## 🧰 Test Data Management
**Location Fixtures** (`tests/fixtures/locations.json`):
```json
[
  {
    "city": "Pune",
    "state": "Maharashtra",
    "country": "India",
    "latitude": 18.5204,
    "longitude": 73.8567
  }
]
```

**Mocking Google Sheets**:
```python
@pytest.fixture
def mock_sheets(monkeypatch):
    def mock_fetch(*args, **kwargs):
        return [["Pune", "MH", "India", "18.5204", "73.8567"]]
    monkeypatch.setattr("gsheets.locations.fetch_locations_from_gsheet", mock_fetch)
```

---

## 📊 Coverage
```bash
pytest --cov=backend --cov-report=html
```
**Target**: 85%+ coverage (excluding templates)

---

## 🚩 Manual Testing Checklist
1. [ ] Location dropdown cascade
   - Country → State → City population
   - Edge case: States with 1 city
2. [ ] Timezone conversion
   - Verify 8:30 AM IST → 03:00 UTC
3. [ ] Sheet persistence
   - Confirm input data appears in Sheets

---

**See Also**:  
- [API Reference](../5-API-Reference.md) for endpoint specs  
- [CI/CD Pipeline](../7-Deployment.md#ci-cd)  