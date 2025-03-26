# 🖥️ Frontend Architecture

## Key Files
| File | Purpose | Technology |
|------|---------|------------|
| `home.html` | Main form template | Jinja2 + Tailwind CSS |
| `form.js` | Dynamic location handling | Vanilla ES6 |
| `main.css` | Animations & themes | Custom CSS |

## Critical Components
### 1. Location Form Handler
- **Class**: `LocationFormHandler` (in `form.js`)
- **Features**:
  - Cascading dropdowns (Country → State → City)
  - Client-side validation
  - Error retry mechanism (3 attempts)

### 2. UI Patterns
```javascript
// Example: Dynamic dropdown population
populateCountries() {
  const countries = [...new Set(locations.map(l => l.country))];
  this.countrySelect.innerHTML = countries.map(c => 
    `<option value="${c}">${c}</option>`
  ).join('');
}
```

## Data Flow
1. **Initial Load**:
   - Fetch locations via `/locations` API
   - Cache data in `cachedLocations`

2. **Form Submission**:
   - Validate inputs → POST `/submit`
   - Show loading spinner during processing

## Performance Notes
- Locations cached after first fetch
- Debounced API calls during rapid dropdown changes