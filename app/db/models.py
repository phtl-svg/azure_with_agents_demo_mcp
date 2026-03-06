# (c) Danit Consultancy and Development, January-2026, danittech@yahoo.com

""" SQLAlchemy ORM models """

from datetime import datetime
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ----------------------------------------------------------------------------------------

class Base(DeclarativeBase):
    """
    Base class for all ORM models.
    Every model that inherits from Base will have its table registered in
    Base.metadata, which is what create_all() iterates over at startup.
    """
    pass

# ----------------------------------------------------------------------------------------

class Document(Base):
    """
    A document stored in the knowledge base.
    The agent can search these via the search_documents tool.

    Columns:
      id         - auto-incrementing primary key
      title      - short label, also searchable
      content    - full text body, the main searchable field
      created_at - set automatically by the database server (not the app)
    """
    __tablename__ = "documents"

    id:         Mapped[int]      = mapped_column(primary_key=True)
    title:      Mapped[str]      = mapped_column(String(255), nullable=False)
    content:    Mapped[str]      = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
