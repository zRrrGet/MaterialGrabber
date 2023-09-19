from __future__ import annotations

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# from tgbot.orm.base import Base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __mapper_args__ = {'eager_defaults': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
    subscribed_on_channels: Mapped[bool] = mapped_column()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
