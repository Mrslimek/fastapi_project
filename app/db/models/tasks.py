from sqlalchemy import Integer, String, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from utils.enums import CompletionStatus


class Base(DeclarativeBase):
    # Здесь можно будет описать метаданные моделей
    pass


def get_enum_values(enum_class):
    return [member.value for member in enum_class]


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    # TODO: Разобраться с тем, как правильно преобразовать enum в sqlalchemy enum
    completion_status: Mapped[CompletionStatus] = mapped_column(
        SQLEnum(
            CompletionStatus, name="completion_status", values_callable=get_enum_values
        ),
        default=CompletionStatus.NOT_COMPLETED,
        nullable=False,
    )
