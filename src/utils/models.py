from datetime import datetime
from sqlalchemy.orm import Mapped, registry, mapped_column
from sqlalchemy import func

table_registry = registry()

@table_registry.mapped_as_dataclass
class Customer:
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    date: Mapped[datetime] = mapped_column(nullable=False)
    document: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone1: Mapped[str] = mapped_column(nullable=True)
    phone2: Mapped[str] = mapped_column(nullable=True)
    instagram: Mapped[str] = mapped_column(nullable=True)
    points: Mapped[int] = mapped_column(init=False, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)
    points: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
