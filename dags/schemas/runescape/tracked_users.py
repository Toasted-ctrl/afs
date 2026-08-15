from datetime import datetime
from sqlalchemy import UUID, text, String, TIMESTAMP, Boolean
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from schemas.base import Base


class TrackedUsersT(Base):
    __tablename__ = 'tracked_users'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    player_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    inserted_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    inserted_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default=text("current_user")
    )

    is_tracked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true")
    )