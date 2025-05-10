from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from datetime import datetime


class RevokedToken(Base):
    __tablename__ = "revoked_token"
    token: Mapped[str] = mapped_column(
        String(), nullable=False, unique=True, primary_key=True
    )
    revoked_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
