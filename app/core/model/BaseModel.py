import uuid
from datetime import datetime
from sqlalchemy import MetaData, func, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Deterministic constraint names so Alembic can generate drop/alter operations.
# With "ck", the name passed to CheckConstraint(name=...) becomes the suffix,
# e.g. name="quantity_non_negative" -> "ck_products_quantity_non_negative".
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class BaseModel(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=NAMING_CONVENTION)
    # Fetch server-generated values (created_at/updated_at) in the same
    # INSERT/UPDATE via RETURNING, avoiding lazy loads (MissingGreenlet in async).
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )