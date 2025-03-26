# 📦 Installation Steps

## 1. Clone Repository
```bash
git clone https://github.com/your-repo/natal-astro.git
cd natal-astro
```

## 2. Create Virtual Environment
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
py -m venv venv
.\venv\Scripts\activate
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Verify Installation
```bash
python -c "import swisseph as swe; print(swe.version())"
```
✅ Expected output: `'2.10.03'` or similar

## Common Issues
| Error | Solution |
|-------|----------|
| `swisseph` fails to install | Install Swiss Ephemeris manually first:
| | ```bash
| pip install https://github.com/astrorigin/pyswisseph/archive/master.zip
| ``` |
| Missing Google APIs | Ensure you ran:
| | ```bash
| pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
| ``` |