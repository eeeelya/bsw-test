from fastapi.routing import APIRouter

events_router = APIRouter(tags=["События"], prefix="/events")
