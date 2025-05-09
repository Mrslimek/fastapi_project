from fastapi import HTTPException
from typing import Type
from app.db.database import Base


def handle_db_result(result):
    """
    Обрабатывает результат операции с базой данных.
    Если результат означает ошибку, поднимает соответствующее HTTPException.
    Если обработки ошибок нет — возвращает результат.
    """
    if result is None:
        raise HTTPException(
            status_code=404, detail="По вашему запросу ничего не найдено"
        )
    error_map = {
        "IntegrityError": ("Ошибка целостности данных", 400),
        "TypeError": ("Неверный формат данных", 400),
        "InvalidRequestError": ("Некорректный запрос", 400),
    }
    if result in error_map:
        detail, status_code = error_map[result]
        raise HTTPException(status_code=status_code, detail=detail)
    return result


def create_model_instance(
    model_class: Type[Base], model_data: dict, user_id: int
):
    model_obj = model_class(**model_data)
    model_obj.user_id = user_id
    return model_obj
