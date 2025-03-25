from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_service_account_file: str
    location_spreadsheet_id: str
    natal_spreadsheet_id: str
    google_scopes: list
    class Config:
        env_file = ".env"

settings = Settings()