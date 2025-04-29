from fastapi import HTTPException


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
