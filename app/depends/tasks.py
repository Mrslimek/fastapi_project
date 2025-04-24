from db.models.tasks import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from schemas.tasks.tasks import TaskCreateUpdate, TaskPartialUpdate


async def list_model_data(model: type[Base], db: AsyncSession) -> list[Base] | None:
    """
    Получение всех записей модели model из бд.
    Если select(model) ничего не вернет, то вернет пустой список.
    Эта ситуация обрабатывается, чтобы вернуть None для простой обработки ошибок.
    """
    tasks = await db.scalars(select(model))
    result = tasks.all()
    if not result:
        return None
    return result


async def retrieve_model_data(
    model_id: int, model: type[Base], db: AsyncSession
) -> Base | None:
    """
    Получение конкретной записи модели model из бд
    по id.
    Метод get у db вернет None, если ничего не будет найдено.
    """
    result = await db.get(model, model_id)
    return result


async def create_model_and_commit(
    model: type[Base], model_data: TaskCreateUpdate, db: AsyncSession
) -> Base | None:
    """
    Создание Объекта модели model и коммит в бд.
    """
    model_data = model_data.model_dump()
    try:
        new_model = model(**model_data)
        async with db.begin():
            db.add(new_model)
        return new_model
    except IntegrityError:
        return None
    except TypeError:
        return None
    except InvalidRequestError:
        return None


async def update_model_and_commit(
    model: type[Base], model_id: int, new_data: TaskCreateUpdate, db: AsyncSession
) -> Base | None:
    """
    Полное обновление объекта модели model и коммит в бд.
    """
    new_data = new_data.model_dump()
    async with db.begin():
        try:
            model_obj = await db.get(model, model_id)
            if model_obj is None:
                return None
            for key, value in new_data.items():
                setattr(model_obj, key, value)
            db.add(model_obj)
        except IntegrityError:
            return "IntegrityError"
        except TypeError:
            return "TypeError"
        except InvalidRequestError:
            return "InvalidRequestError"
    return model_obj


async def partial_update_and_commit(
    model: type[Base], model_id: int, new_data: TaskPartialUpdate, db: AsyncSession
) -> Base | None:
    """
    Частичное обновление объекта модели model и коммит в бд.
    """
    new_data = new_data.model_dump()
    async with db.begin():
        try:
            model_obj = await db.get(model, model_id)
            if model_obj is None:
                return None
            for key, value in new_data.items():
                if value:
                    setattr(model_obj, key, value)
            db.add(model_obj)
        except IntegrityError:
            return "IntegrityError"
        except TypeError:
            return "TypeError"
        except InvalidRequestError:
            return "InvalidRequestError"
    return model_obj
