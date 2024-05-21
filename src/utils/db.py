import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import table_registry, Customer

def create_engine():
    strcon = "sqlite:///../data/database.db"
    return sqlalchemy.create_engine(strcon)


def new_session():
    engine = create_engine()
    table_registry.metadata.create_all(engine)
    return Session(engine)

# def search_user(document_id: str, session: Session):

#     return customer