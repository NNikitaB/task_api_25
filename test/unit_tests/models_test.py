import pytest
from sqlalchemy import create_mock_engine,create_engine
from sqlalchemy.orm import Session
from internal.database.db import Base
from internal.models.Users import Users
import datetime
import uuid


def test_create_db():
    """
    Creates a new SQLite database and initializes the database schema.
    """
    url = "sqlite://"
    engine = create_engine(url, echo=True)
    Base.metadata.create_all(engine)


@pytest.fixture(scope="module")
def db_session():
    url="sqlite://"
    engine = create_engine(url,echo=True)
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    yield session
    session.rollback()
    session.close()


def test_add_user(db_session):
    user = Users(
        uuid=uuid.uuid4(),
        amount=0,
        time_registration=datetime.datetime.now()
        )
    s = db_session
    s.add(user)
    s.commit()
