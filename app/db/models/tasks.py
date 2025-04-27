from sqlalchemy import Integer, String, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from utils.enums import CompletionStatus
from db.database import Base


def get_enum_values(enum_class):
    return [member.value for member in enum_class]


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    completion_status: Mapped[CompletionStatus] = mapped_column(
        SQLEnum(
            CompletionStatus, name="completion_status", values_callable=get_enum_values
        ),
        default=CompletionStatus.NOT_COMPLETED,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")
