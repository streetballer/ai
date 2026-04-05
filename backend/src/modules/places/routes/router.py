from fastapi import APIRouter
from src.modules.places.controllers.search_places import router as search_places_router

router = APIRouter()

router.include_router(search_places_router)
