from fastapi import FastAPI
from app.routers import estimations

app = FastAPI(
    title="Estimador CAG",
    description="Estimación de software con arquitectura Cache-Augmented Generation",
    version="0.1.0"
)

app.include_router(estimations.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "estimador-cag"}