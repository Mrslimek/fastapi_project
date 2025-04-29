from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String
from passlib.context import CryptContext
from db.database import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(25), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    tasks = relationship("Task", back_populates="user")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)
