from pathlib import Path
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Loan Pricing Engine"
    debug: bool = False
    excel_template_path: Path = Path("templates/loan_model.xlsx")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()