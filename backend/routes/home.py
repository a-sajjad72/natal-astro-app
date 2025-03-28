# backend/routes/home.py

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "page_heading": "Discover Your Cosmic Blueprint",
            "show_cta": True,
        },
    )
