from fastapi import FastAPI
from .api.endpoints import router as pricing_router
from .config import settings

app = FastAPI(title=settings.app_name)
app.include_router(pricing_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)