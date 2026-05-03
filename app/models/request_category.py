from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class RequestCategory(Base):
    __tablename__ = "request_categories"

    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id"), primary_key=True)
    category_code: Mapped[str] = mapped_column(ForeignKey("categories.code"),  primary_key=True)
    confidence: Mapped[float | None] = mapped_column(Float,  nullable=True)

    request = relationship("Request", back_populates="request_categories")
    category = relationship("Category", back_populates="request_categories")
