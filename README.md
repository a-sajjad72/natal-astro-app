# My FastAPI Web App

This project is a web application built using FastAPI for the backend and Jinja2 for server-side rendering (SSR) of templates. The frontend utilizes Tailwind UI for styling, with ShadCN extracted classes for enhanced design.

## Project Structure

```
my-fastapi-web-app
C:.
│   .env
│   .gitignore
│   config.py
│   main.py
│   README.md
│   requirements.txt
│
├───backend
│   ├───gsheets
│   │       locations.py
│   │       natal.py
│   │       utils.py
│   │
│   ├───routes
│   │       home.py
│   │       locations.py
│   │       submit.py
│   │
│   ├───services
│   │       astrology_constants.py
│   │       astrology_service.py
│   │
│   ├───static
│   │   ├───css
│   │   │       main.css
│   │   │
│   │   ├───images
│   │   │       stars-bg.svg
│   │   │
│   │   └───js
│   │           form.js
│   │
│   └───templates
│       │   base.html
│       │   home.html
│       │   report.html
│       │
│       └───partials
│               footer.html
│               navbar.html
│
└───env
        service-account.json

```

## Setup Instructions

1. **Clone the repository:**

   ```
   git clone https://github.com/yourusername/my-fastapi-web-app.git
   cd my-fastapi-web-app
   ```

2. **Create a virtual environment:**

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the FastAPI application, execute the following command:

```
uvicorn backend.main:app --reload
```

Visit `http://127.0.0.1:8000` in your browser to see the application in action.

## Testing

To run the tests, use the following command:

```
pytest tests/test_main.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
