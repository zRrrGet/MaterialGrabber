from __future__ import annotations
import datetime

from sqlalchemy import DateTime, BIGINT
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy.ext.declarative import declarative_base

from src.core.domain.entities.download_request import RequestStatus, ContentType, FailStatus

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __mapper_args__ = {'eager_defaults': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    tg_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    subscribed_on_channels: Mapped[bool] = mapped_column()
    accepted_rules: Mapped[bool] = mapped_column()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class DownloadRequest(Base):
    __tablename__ = 'download_requests'
    __mapper_args__ = {'eager_defaults': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    user_id: Mapped[int] = mapped_column()
    download_link: Mapped[str] = mapped_column()
    content_link: Mapped[str] = mapped_column(nullable=True)
    content_type: Mapped[ContentType] = mapped_column()
    status: Mapped[RequestStatus] = mapped_column(default=RequestStatus.waiting_queue)
    fail_status: Mapped[FailStatus] = mapped_column(default=FailStatus.no_exception)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __init__(self, **kwargs):
        super(DownloadRequest, self).__init__(**kwargs)


class Channel(Base):
    __tablename__ = 'channels'
    __mapper_args__ = {'eager_defaults': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    chat_id: Mapped[str] = mapped_column(unique=True)
    join_link: Mapped[str] = mapped_column()

    def __init__(self, **kwargs):
        super(Channel, self).__init__(**kwargs)
