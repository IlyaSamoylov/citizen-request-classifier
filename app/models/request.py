from sqlalchemy import ForeignKey, Text, Boolean, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.models.base import Base

class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    raw_text: Mapped[str] = mapped_column(Text)
    toxicity_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    category_code: Mapped[str | None] = mapped_column(ForeignKey("categories.code"),
                                                        nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    processed_at: Mapped[datetime | None] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=True)

    category = relationship("Category")
    clarifications = relationship("Clarification", back_populates="request")