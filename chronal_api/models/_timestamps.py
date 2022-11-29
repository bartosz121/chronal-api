from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, func


class Timestamps:
    created_at = Column[datetime](
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column[datetime](
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
