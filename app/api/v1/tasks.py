from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from db.models.tasks import Task
from schemas.tasks.tasks import (
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
    destroy_and_commit
)


router = APIRouter(prefix="/tasks")


@router.get("", summary="Метод GET/list", response_model=TaskResponseList)
async def list_tasks(db: AsyncSession = Depends(get_db)):
    """
    Получение всех записей модели Task
    """
    result = await list_model_data(model=Task, db=db)
    if not result:
        raise HTTPException(
            status_code=404, detail="По вашему запросу ничего не найдено"
        )
    return result


# TODO: Посмотреть, может быть здесь будет эффективнее использовать синхронные запросы и как это сделать
@router.get("/{task_id}", summary="Метод GET/retrieve", response_model=TaskResponse)
async def retrieve_tasks(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получение записи модели Task по id
    """
    result = await retrieve_model_data(model_id=task_id, model=Task, db=db)
    if result is None:
        raise HTTPException(
            status_code=404, detail="По вашему запросу ничего не найдено"
        )
    return result


@router.post("", summary="Метод POST", response_model=TaskResponse)
async def create_task(task_data: TaskCreateUpdate, db: AsyncSession = Depends(get_db)):
    """
    Создание новой записи модели Task
    """
    result = await create_model_and_commit(model=Task, model_data=task_data, db=db)
    if result is None:
        raise HTTPException(status_code=400, detail="Некорректные данные")
    return result


@router.put("/{task_id}", summary="Метод PUT", response_model=TaskResponse)
async def update_task(
    task_id: int, new_data: TaskCreateUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Полное обновление записи модели Task
    """
    result = await update_model_and_commit(
        model=Task, model_id=task_id, new_data=new_data, db=db
    )
    match result:
        case None:
            raise HTTPException(
                status_code=404, detail="По вашему запросу ничего не найдено"
            )
        case "IntegrityError":
            raise HTTPException(status_code=400, detail="Ошибка целостности данных")
        case "TypeError":
            raise HTTPException(status_code=400, detail="Неверный формат данных")
        case "InvalidRequestError":
            raise HTTPException(status_code=400, detail="Некорректный запрос")

    return result


@router.patch("/{task_id}", summary="Метод PATCH", response_model=TaskResponse)
async def partial_update_task(
    task_id: int, new_data: TaskPartialUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Частичное обновление записи модели Task
    """
    result = await partial_update_and_commit(
        model=Task, model_id=task_id, new_data=new_data, db=db
    )
    match result:
        case None:
            raise HTTPException(
                status_code=404, detail="По вашему запросу ничего не найдено"
            )
        case "IntegrityError":
            raise HTTPException(status_code=400, detail="Ошибка целостности данных")
        case "TypeError":
            raise HTTPException(status_code=400, detail="Неверный формат данных")
        case "InvalidRequestError":
            raise HTTPException(status_code=400, detail="Некорректный запрос")

    return result


@router.delete("/{task_id}", summary="Метод DELETE")
async def destroy_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удаление записи модели Task
    """
    result = await destroy_and_commit(model=Task, model_id=task_id, db=db)
    match result:
        case None:
            raise HTTPException(status_code=404, detail="По вашесу запросу ничего не найдено")
        case "IntegrityError":
            raise HTTPException(status_code=400, detail="Ошибка целостности данных")
        case "TypeError":
            raise HTTPException(status_code=400, detail="Неверный формат данных")
        case "InvalidRequestError":
            raise HTTPException(status_code=400, detail="Некорректный запрос")
        case "success":
            return {"status": "success"}
