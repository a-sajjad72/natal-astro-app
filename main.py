from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.gsheets.utils import connect_to_gsheet
from backend.routes.home import router as home_router
from backend.routes.locations import router as locations_router
from backend.routes.submit import router as submit_router
from config import settings
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.gsheet_service = connect_to_gsheet(
        settings.google_service_account_file, scopes=settings.google_scopes
    )
    print("Google Sheets service created")
    yield
    app.state.gsheet_service.close()


app = FastAPI(lifespan=lifespan)

# Include the routers
app.include_router(home_router)
app.include_router(submit_router)
app.include_router(locations_router)

# Configure templates
templates = Jinja2Templates(directory="backend/templates")


# Mount the static files directory
app.mount("/static", StaticFiles(directory="backend/static"), name="static")


# Run the server (only when running this file directly)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
