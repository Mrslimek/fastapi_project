from pydantic import BaseModel, RootModel, Field, constr
from typing import Optional, Annotated
from app.utils.enums import CompletionStatus

# Аннотации
NonEmptyString = constr(strip_whitespace=True, min_length=1)
TitleType = Annotated[
    NonEmptyString,
    Field(
        max_length=25,
        description="Название должно быть не более 25 символов и не быть пустым",
    ),
]
DescriptionType = Annotated[
    NonEmptyString,
    Field(
        max_length=255,
        description="Описание должно быть не более 255 символов и не быть пустым",
    ),
]


# pydantic схемы
class TaskResponse(BaseModel):
    """
    Схема для ответа модели Task
    """

    id: int
    title: str
    description: Optional[str]
    completion_status: str
    user_id: int


class TaskResponseList(RootModel):
    """
    Рут схема для списка схем TaskResponse
    """

    root: list[TaskResponse]


class TaskCreateUpdate(BaseModel):
    """
    Схема для создания и обновления модели Task
    """

    title: TitleType
    description: Optional[DescriptionType] = None
    completion_status: Optional[CompletionStatus] = CompletionStatus.NOT_COMPLETED
    
    class Config:
        extra = "forbid"


class TaskPartialUpdate(BaseModel):
    """
    Схема для частичного обновления модели Task
    """

    title: Optional[TitleType] = None
    description: Optional[DescriptionType] = None
    completion_status: Optional[CompletionStatus] = CompletionStatus.NOT_COMPLETED
    
    class Config:
        extra = "forbid"
