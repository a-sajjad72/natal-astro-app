# My FastAPI Web App

This project is a web application built using FastAPI for the backend and Jinja2 for server-side rendering (SSR) of templates. The frontend utilizes Tailwind UI for styling, with ShadCN extracted classes for enhanced design.

## Project Structure

```
my-fastapi-web-app
├── backend
│   ├── main.py               # Entry point of the FastAPI application
│   ├── routes
│   │   └── home.py           # Contains the HomeRouter class for handling routes
│   ├── templates
│   │   └── base_template.py   # Renders Jinja2 templates
│   └── styles
│       └── tailwind_classes.py # Contains Tailwind UI and ShadCN classes
├── tests
│   └── test_main.py          # Unit tests for the application
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
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