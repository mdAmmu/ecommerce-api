from fastapi import FastAPI

app = FastAPI(
    title="Ecommerce API",
    description="Backend API for the ecommerce platform",
    version="1.0.0"
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
