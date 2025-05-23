from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.tasks import Task, Base
from app.db.database import get_db
from app.utils.auth import verify_token
from app.utils.etc import handle_db_result, create_model_instance
from app.schemas.tasks import (
    TaskCreateUpdate,
    TaskPartialUpdate,
    TaskResponse,
    TaskResponseList,
)
from app.depends.tasks import (
    list_model_data,
    retrieve_model_data,
    create_model_and_commit,
    update_model_and_commit,
    partial_update_and_commit,
    destroy_and_commit,
)


router = APIRouter(prefix="/tasks")


@router.get("", summary="Метод GET/list", response_model=TaskResponseList)
async def list_tasks(
    db: AsyncSession = Depends(get_db), user: Base = Depends(verify_token)
):
    """
    Получение всех записей модели Task
    """
    result = await list_model_data(model_class=Task, user=user, db=db)
    if not result:
        raise HTTPException(
            status_code=404, detail="По вашему запросу ничего не найдено"
        )
    return result


@router.get(
    "/{task_id}", summary="Метод GET/retrieve", response_model=TaskResponse
)
async def retrieve_tasks(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user: Base = Depends(verify_token),
):
    """
    Получение записи модели Task по id
    """
    result = await retrieve_model_data(
        model_obj_id=task_id, model_class=Task, db=db
    )
    if result is None:
        raise HTTPException(
            status_code=404, detail="По вашему запросу ничего не найдено"
        )
    return result


@router.post(
    "", summary="Метод POST", status_code=201, response_model=TaskResponse
)
async def create_task(
    task_data: TaskCreateUpdate,
    db: AsyncSession = Depends(get_db),
    user: Base = Depends(verify_token),
):
    """
    Создание новой записи модели Task
    """
    model_obj = create_model_instance(
        model_class=Task, model_data=task_data.model_dump(), user_id=user.id
    )
    result = await create_model_and_commit(model_obj=model_obj, db=db)
    if result is None:
        raise HTTPException(status_code=400, detail="Некорректные данные")
    return result


@router.put("/{task_id}", summary="Метод PUT", response_model=TaskResponse)
async def update_task(
    task_id: int,
    new_data: TaskCreateUpdate,
    db: AsyncSession = Depends(get_db),
    user: Base = Depends(verify_token),
):
    """
    Полное обновление записи модели Task.
    По сути этот метод не нужен в рамках этого приложения,
    Но реализован в учебных целях
    """
    result = await update_model_and_commit(
        model_class=Task,
        model_obj_id=task_id,
        new_data=new_data.model_dump(),
        user=user,
        db=db,
    )
    handle_db_result(result)
    return result


@router.patch("/{task_id}", summary="Метод PATCH", response_model=TaskResponse)
async def partial_update_task(
    task_id: int,
    new_data: TaskPartialUpdate,
    db: AsyncSession = Depends(get_db),
    user: Base = Depends(verify_token),
):
    """
    Частичное обновление записи модели Task
    """
    result = await partial_update_and_commit(
        model_class=Task,
        model_obj_id=task_id,
        new_data=new_data.model_dump(),
        db=db,
    )
    handle_db_result(result)
    return result


@router.delete("/{task_id}", summary="Метод DELETE")
async def destroy_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user: Base = Depends(verify_token),
):
    """
    Удаление записи модели Task
    """
    result = await destroy_and_commit(
        model_class=Task, model_obj_id=task_id, db=db
    )
    handle_db_result(result)
    return {"status": "success"}
