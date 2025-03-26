# 🌍 Location System

## Components
| File | Purpose |
|------|---------|
| `routes/locations.py` | API endpoints |
| `gsheets/locations.py` | Data fetching |
| `static/js/form.js` | Dropdown logic |

## Critical Code Path
1. **Initial Load** (`form.js`):
   ```javascript
   async loadLocations() {
     const response = await fetch('/locations');
     this.cachedLocations = await response.json();
   }
   ```

2. **Coordinate Lookup** (`locations.py`):
   ```python
   def get_coordinates(city, state, country, request):
       for loc in locations_df.itertuples():
           if (loc.city == city and 
               loc.state == state and 
               loc.country == country):
               return (loc.latitude, loc.longitude)
   ```

## Data Structure
**Google Sheets Format**:
```csv
city,state,country,latitude,longitude
Mumbai,Maharashtra,India,19.0760,72.8777
```

## Performance
- **Cache**: Locations stored in memory after first fetch  
- **Validation**:
  ```javascript
  validateSelections() {
    if (!this.citySelect.value) {
      this.citySelect.setAttribute('aria-invalid', 'true');
    }
  }
  ```

**See Also**:  
- [Frontend Architecture](../3-Architecture/Frontend.md)  
- [Sheets API Guide](./Google-Sheets-API.md)  