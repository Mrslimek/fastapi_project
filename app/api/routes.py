from fastapi import APIRouter
from api.v1.tasks import router as tasks_router
from api.v1.users import router as users_router


router = APIRouter()
router.include_router(tasks_router, tags=["TASKS_CRUD"])
router.include_router(users_router, tags=["USERS_CRUD"])