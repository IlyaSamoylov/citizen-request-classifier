from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class Category(Base):
    __tablename__ = "categories"

    code: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    synonyms: Mapped[str] = mapped_column(Text)
    examples: Mapped[str] = mapped_column(Text)

    request_categories = relationship("RequestCategory", back_populates="category")