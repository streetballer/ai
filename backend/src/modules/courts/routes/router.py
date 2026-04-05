from fastapi import APIRouter
from src.modules.courts.controllers.search_courts import router as search_courts_router
from src.modules.courts.controllers.add_court import router as add_court_router
from src.modules.courts.controllers.get_court import router as get_court_router

router = APIRouter()

router.include_router(search_courts_router)
router.include_router(add_court_router)
router.include_router(get_court_router)
