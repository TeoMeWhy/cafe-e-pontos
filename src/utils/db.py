import sqlalchemy
from sqlalchemy.orm import Session

from .models import table_registry


def create_engine():
    strcon = 'sqlite:///data/database.db'
    return sqlalchemy.create_engine(strcon)


def new_session():
    engine = create_engine()
    table_registry.metadata.create_all(engine)
    return Session(engine)
