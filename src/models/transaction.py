from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey

from .common import table_registry

@table_registry.mapped_as_dataclass
class Transaction:
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    value: Mapped[float] = mapped_column(nullable=False)
    points: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

@table_registry.mapped_as_dataclass
class TransactionProduct:
    __tablename__ = 'transactions_products'

    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    quantity: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
