from sqlalchemy.orm.scoping import scoped_session


class SqliteBaseRepo:

    def __init__(self, session: scoped_session):
        self.session = session

    def execute(self, statement):
        session = self.session()
        session.execute(statement)
        session.commit()
        session.close()
