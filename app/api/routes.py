from fastapi import APIRouter
from api.v1.tasks import router as task_router


router = APIRouter()
router.include_router(task_router, tags=["CRUD"])