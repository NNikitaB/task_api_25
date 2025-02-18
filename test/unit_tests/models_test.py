import pytest
from sqlalchemy import create_mock_engine,create_engine,delete
from sqlalchemy.orm import Session
from internal.models.Base import Base
from internal.models.Wallets import Wallets
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


def test_add_wallet(db_session):
    wallet = Wallets(
        uuid=uuid.uuid4(),
        amount=0,
        time_registration=datetime.datetime.now()
        )
    s = db_session
    s.add(wallet)
    s.commit()

def test_get_wallet(db_session):
    wallet = Wallets(
        uuid=uuid.uuid4(),
        amount=0,
        time_registration=datetime.datetime.now()
        )
    s = db_session
    s.add(wallet)
    s.commit()
    wallet_from_db = s.query(Wallets).filter(Wallets.uuid == wallet.uuid).first()
    assert wallet_from_db.uuid == wallet.uuid

def test_update_wallet(db_session):
    wallet = Wallets(
        uuid=uuid.uuid4(),
        amount=0,
        time_registration=datetime.datetime.now()
        )
    s = db_session
    s.add(wallet)
    s.execute(delete(Wallets).where(Wallets.uuid == wallet.uuid))
    s.commit()
