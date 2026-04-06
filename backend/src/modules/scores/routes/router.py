from fastapi import APIRouter
from src.modules.scores.controllers.get_scores import router as get_scores_router
from src.modules.scores.controllers.submit_score import router as submit_score_router
from src.modules.scores.controllers.get_score import router as get_score_router
from src.modules.scores.controllers.confirm_score import router as confirm_score_router
from src.modules.scores.controllers.reject_score import router as reject_score_router

router = APIRouter()

router.include_router(get_scores_router)
router.include_router(submit_score_router)
router.include_router(get_score_router)
router.include_router(confirm_score_router)
router.include_router(reject_score_router)
