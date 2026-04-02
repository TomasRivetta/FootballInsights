from fastapi import FastAPI
from app.routers.stats import router as stats_router
from scripts.update_dataset import update_dataset

app = FastAPI(title="FootballInsights API")

app.include_router(stats_router)

@app.get("/")
def root():
    return {"message": "API running"}

update_dataset()