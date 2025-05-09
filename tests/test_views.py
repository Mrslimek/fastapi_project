import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from asyncio import sleep


# TODO: срабатавыет только первый тест, потом все тесты проваливаются
# Фикстура для тестового клиента FastAPI
@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


# @pytest.mark.asyncio
# async def test_create_task(async_client):
#     response = await async_client.post(
#         "/tasks",
#         json={"title": "Тестовая задача 1", "description": "Тестовое описание 1"},
#     )
#     assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_list_tasks(async_client):
#     response = await async_client.get("/tasks")
#     assert response.status_code == 200  # Проверяем, что запрос на список задач работает
#     assert isinstance(response.json(), list)  # Убеждаемся, что ответ — список


# @pytest.mark.asyncio
# async def test_retrieve_tasks(async_client):
#     response = await async_client.get("/tasks/1")
#     assert response.status_code == 200  # Проверяем, что запрос на список задач работает
#     assert isinstance(response.json(), list)  # Убеждаемся, что ответ — список


# @pytest.mark.asyncio
# async def test_update_task(async_client):
#     response = await async_client.post(
#         "/tasks/1",
#         json={
#             "title": "Тестовая обновленная задача 1",
#             "description": "Тестовое обновленное описание 1",
#         },
#     )
#     assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "json_data, expected_status",
    [
        # ✅ Корректные случаи
        ({"title": "Updated task"}, 200),
        ({"description": "Updated description"}, 200),
        ({"title": "Updated task", "description": "Updated description"}, 200),
        ({"title": "Valid", "description": "Another valid description"}, 200),
        ({"title": "T" * 25, "description": "D" * 255, "done": None}, 200),
        ({"title": None, "description": None, "done": None}, 200),
        (
            {"title": None, "description": "Valid description", "done": True},
            200,
        ),
        ({"title": "Valid Title", "description": None, "done": False}, 200),
        ({}, 200),
        # ❌ Одна часть валидная, другая - некорректная
        ({"title": "Updated task", "description": ""}, 400),
        ({"title": "", "description": "Updated description"}, 400),
        ({"title": "Updated task", "description": " "}, 400),
        ({"title": " ", "description": "Updated description"}, 400),
        ({"title": "Updated task", "description": 1}, 400),
        ({"title": 1, "description": "Updated description"}, 400),
        ({"title": "Updated task", "description": True}, 400),
        ({"title": True, "description": "Updated description"}, 400),
        # ❌ Оба поля некорректные
        ({"title": "", "description": ""}, 400),
        ({"title": " ", "description": " "}, 400),
        ({"title": 1, "description": 1}, 400),
        ({"title": True, "description": False}, 400),
        ({"title": {}, "description": []}, 400),
        # ❌ Неверные типы (не строка)
        ({"title": {}, "description": "Valid description"}, 400),
        ({"title": [], "description": "Valid description"}, 400),
        ({"title": "Valid Title", "description": {}, "done": False}, 400),
        ({"title": "Valid Title", "description": [], "done": False}, 400),
        ({"title": "Valid Title", "description": 123, "done": True}, 400),
        (
            {
                "title": "Valid Title",
                "description": "Valid description",
                "done": "Yes",
            },
            400,
        ),
        (
            {
                "title": "Valid Title",
                "description": "Valid description",
                "done": 5,
            },
            400,
        ),
        (
            {
                "title": "Valid Title",
                "description": "Valid description",
                "done": [],
            },
            400,
        ),
    ],
)
async def test_partial_update_task(async_client, json_data, expected_status):
    """
    Тестирование partial_update_task со всеми возможными случаями
    """
    sleep(0.2)
    response = await async_client.patch(
        "/tasks/26",
        json=json_data,
    )
    print(response.json())
    assert response.status_code == expected_status
