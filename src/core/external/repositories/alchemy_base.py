from sqlalchemy.orm.scoping import scoped_session


class AlchemyBaseRepo:

    def __init__(self, session: scoped_session):
        self.session = session

    def execute(self, statement):
        session = self.session()
        session.execute(statement)
        session.commit()
        session.close()
