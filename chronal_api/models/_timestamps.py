from datetime import datetime

from sqlalchemy import Column, func, TIMESTAMP


class Timestamps:
    created_at: datetime = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
    )
    updated_at: datetime = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
