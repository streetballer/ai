from fastapi import APIRouter
from src.modules.settings.controllers.edit_username import router as edit_username_router
from src.modules.settings.controllers.edit_email import router as edit_email_router
from src.modules.settings.controllers.edit_password import router as edit_password_router
from src.modules.settings.controllers.edit_language import router as edit_language_router
from src.modules.settings.controllers.edit_geolocation import router as edit_geolocation_router
from src.modules.settings.controllers.delete_account import router as delete_account_router

router = APIRouter()

router.include_router(edit_username_router)
router.include_router(edit_email_router)
router.include_router(edit_password_router)
router.include_router(edit_language_router)
router.include_router(edit_geolocation_router)
router.include_router(delete_account_router)
