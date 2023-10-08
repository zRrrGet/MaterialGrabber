from src.core.external.orm.models import User
from src.core.domain.entities.user import User as EntityUser


class UserMapper:

    @staticmethod
    def to_entity(model: User) -> EntityUser:
        return EntityUser(id=model.id, tg_id=model.tg_id, subscribed_on_channels=model.subscribed_on_channels,
                          accepted_rules=model.accepted_rules)

    @staticmethod
    def to_model(entity: EntityUser) -> User:
        return User(id=entity.id, tg_id=entity.tg_id, subscribed_on_channels=entity.subscribed_on_channels,
                    accepted_rules=entity.accepted_rules)
