from __future__ import annotations

import enum
from typing import List

from sqlalchemy.sql import func
from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, Enum, Float, DateTime
from sqlalchemy.sql import expression
from sqlalchemy.orm import Mapped, backref
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

# from tgbot.models.base import Base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class ExchangeStatus(enum.Enum):
    processing = 0
    approved = 1
    disapproved = 2


class ExchangeType(enum.Enum):
    rub2thb = 0
    thb2rub = 1


class User(Base):
    __tablename__ = 'users'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True, index=True, unique=True)
    tg_user_id = Column(Integer, unique=True)
    first_name = Column(String)
    username = Column(String)
    exchanges: Mapped[List['Exchange']] = relationship(back_populates='user', lazy='selectin')
    inviter_id: Mapped[int] = mapped_column(ForeignKey('users.id'), default=-1)
    invited_users: Mapped[List['User']] = relationship(back_populates='inviter', lazy='selectin')
    inviter: Mapped['User'] = relationship(back_populates='invited_users', remote_side=[id], lazy='selectin')
    is_ref_allowed = Column(Boolean, server_default=expression.false())
    balance = Column(Float, default=0)
    total_income = Column(Float, default=0)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class Exchange(Base):
    __tablename__ = 'exchanges'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='exchanges', lazy='selectin')
    sum = Column(Float, nullable=False)
    exchange_to = Column(Float, nullable=False)
    ref_percent = Column(Float, nullable=False)
    ref_income = Column(Float, nullable=False)
    status = Column(Enum(ExchangeStatus), default=ExchangeStatus.processing)
    ex_type = Column(Enum(ExchangeType))
    bank = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, **kwargs):
        super(Exchange, self).__init__(**kwargs)


class ConfigItem(Base):
    """Represents one config item.

    All values are strings, so non-string values must be converted later.

    :param key: config key
    :param value: configured value
    """

    __tablename__ = 'config_item'

    key = Column(String, primary_key=True)
    value = Column(String)

    def __str__(self):
        return '{}: {}'.format(self.key, self.value)

    def __repr__(self):
        return 'ConfigItem(key={!r}, value={!r})'.format(self.key, self.value)

