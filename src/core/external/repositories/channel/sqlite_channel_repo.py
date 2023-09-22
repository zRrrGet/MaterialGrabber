from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy import update, select, delete

from src.core.external.orm.models import Channel
from src.core.domain.entities.channel import Channel as EntityChannel
from src.core.domain.repositories.channel_repo import IChannelRepository


class SqliteChannelRepo(IChannelRepository):

    def __init__(self, session: scoped_session):
        self.session = session

    def add_channel(self, channel: EntityChannel):
        session = self.session()
        session.add(Channel(id=channel.id, chat_id=channel.chat_id, join_link=channel.join_link))
        session.commit()
        session.close()

    def remove_channel(self, channel_id: int):
        session = self.session()
        session.execute(delete(Channel).where(Channel.id == channel_id))
        session.commit()
        session.close()

    def get_channels(self) -> list[EntityChannel]:
        session = self.session()
        channels = session.query(Channel).all()

        entity_channels = []
        for channel in channels:
            chat_id = channel.chat_id
            try:
                chat_id = int(chat_id)
            except (TypeError, ValueError):
                pass
            entity_channels.append(EntityChannel(id=channel.id, chat_id=chat_id, join_link=channel.join_link))
        session.close()

        return entity_channels
