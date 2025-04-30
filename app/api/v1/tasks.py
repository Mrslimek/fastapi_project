from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.tasks import Task, Base
from db.database import get_db
from utils.auth import verify_token
from utils.etc import handle_db_result
from schemas.tasks import (
    TaskCreateUpdate,
    TaskPartialUpdate,
    TaskResponse,
    TaskResponseList,
)
from depends.tasks import (
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
    result = await list_model_data(model=Task, user=user, db=db)
    if not result:
        raise HTTPException(
            status_code=404, detail="По вашему запросу ничего не найдено"
        )
    return result


# TODO: Посмотреть, может быть здесь будет эффективнее использовать синхронные запросы и как это сделать
@router.get("/{task_id}", summary="Метод GET/retrieve", response_model=TaskResponse)
async def retrieve_tasks(
    task_id: int, db: AsyncSession = Depends(get_db), user: Base = Depends(verify_token)
):
    """
    Получение записи модели Task по id
    """
    result = await retrieve_model_data(model_id=task_id, model=Task, db=db)
    if result is None:
        raise HTTPException(
            status_code=404, detail="По вашему запросу ничего не найдено"
        )
    return result


# TODO: Сюда надо вставить response_model=TaskResponse, но для этого надо
# возвращать модель с id
@router.post("", summary="Метод POST", status_code=201, response_model=TaskResponse)
async def create_task(
    task_data: TaskCreateUpdate,
    db: AsyncSession = Depends(get_db),
    user: Base = Depends(verify_token),
):
    """
    Создание новой записи модели Task
    """
    result = await create_model_and_commit(model=Task, model_data=task_data, user=user, db=db)
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
        model=Task, model_id=task_id, new_data=new_data, user=user, db=db
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
        model=Task, model_id=task_id, new_data=new_data, db=db
    )
    handle_db_result(result)
    return result


@router.delete("/{task_id}", summary="Метод DELETE")
async def destroy_task(
    task_id: int, db: AsyncSession = Depends(get_db), user: Base = Depends(verify_token)
):
    """
    Удаление записи модели Task
    """
    result = await destroy_and_commit(model=Task, model_id=task_id, db=db)
    handle_db_result(result)
    return {"status": "success"}
