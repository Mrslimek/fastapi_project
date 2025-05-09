from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.tasks import Base


async def list_model_data(
    model_class: type[Base], user: Base, db: AsyncSession
) -> list[Base] | None:
    """
    Получение всех записей модели model из бд.
    Если select(model) ничего не вернет, то вернет пустой список.
    Эта ситуация обрабатывается, чтобы вернуть None для простой обработки ошибок.
    """
    tasks = await db.scalars(
        select(model_class).where(model_class.user_id == user.id)
    )
    result = tasks.all()
    if not result:
        return None
    return result


async def retrieve_model_data(
    model_obj_id: int, model_class: type[Base], db: AsyncSession
) -> Base | None:
    """
    Получение конкретной записи модели model из бд
    по id.
    Метод get у db вернет None, если ничего не будет найдено.
    """
    result = await db.get(model_class, model_obj_id)
    return result


async def create_model_and_commit(model_obj, db: AsyncSession) -> Base | None:
    """
    Создание Объекта модели model и коммит в бд.
    """
    try:
        async with db.begin():
            db.add(model_obj)
    except IntegrityError:
        return "IntegrityError"
    except TypeError:
        return "TypeError"
    except InvalidRequestError:
        return "InvalidRequestError"
    return model_obj


async def update_model_and_commit(
    model_class: type[Base],
    model_obj_id: int,
    new_data: dict,
    user: Base,
    db: AsyncSession,
) -> Base | None:
    """
    Полное обновление объекта модели model и коммит в бд.
    """
    async with db.begin():
        try:
            model_obj = await db.get(model_class, model_obj_id)
            if model_obj is None:
                return None
            # Главное не забывать, что если проходимся циклом,
            # то нужно обязательно заблокировать возможность передавать поля,
            # которые мы не хотим присваивать
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
    model_class: type[Base],
    model_obj_id: int,
    new_data: dict,
    db: AsyncSession,
) -> Base | None:
    """
    Частичное обновление объекта модели model и коммит в бд.
    """
    new_data = new_data.model_dump()
    async with db.begin():
        try:
            model_obj = await db.get(model_class, model_obj_id)
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


async def destroy_and_commit(
    model_class: type[Base], model_obj_id: int, db: AsyncSession
):
    """
    Удаление записи переданной модели
    """
    async with db.begin():
        model_obj = await db.get(model_class, model_obj_id)
        if model_obj is None:
            return None
        try:
            # Здесь используется await потому, что delete у AsyncSession
            # реализован через async def, но
            # он вызывает синхронную функцию delete у greenlet
            # Асинхронность тут нужна для того, чтобы, в случае существования каких-то связей,
            # и, соответственно, необходимости добавить каскадные удаления этих связей,
            # то есть, сделать запрос в бд, то есть i/o операцию, не блокировать поток
            await db.delete(model_obj)
        except IntegrityError:
            return "IntegrityError"
        except TypeError:
            return "TypeError"
        except InvalidRequestError:
            return "InvalidRequestError"
    return "success"
