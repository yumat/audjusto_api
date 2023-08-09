from fastapi import APIRouter
import app.schemas.health as health_schema

router = APIRouter()

@router.get("/api/health_check", response_model=health_schema.HealthCheck)
async def get_health():
    return { "message" : "health check OK" }