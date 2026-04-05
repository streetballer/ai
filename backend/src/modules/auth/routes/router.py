from fastapi import APIRouter
from src.modules.auth.controllers.log_in import router as log_in_router
from src.modules.auth.controllers.password import router as password_router
from src.modules.auth.controllers.refresh import router as refresh_router
from src.modules.auth.controllers.sign_up import router as sign_up_router
from src.modules.auth.controllers.social import router as social_router
from src.modules.auth.controllers.verification import router as verification_router

router = APIRouter()

router.include_router(sign_up_router)
router.include_router(log_in_router)
router.include_router(social_router)
router.include_router(password_router)
router.include_router(verification_router)
router.include_router(refresh_router)
