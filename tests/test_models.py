import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from impressoras import config
from impressoras.models import Base, User


@pytest.fixture(scope="module")
def database():
    engine = create_engine(config.TEST_DATABASE_URL, echo=True)
    Session = sessionmaker(bind=engine)
    yield Session, engine
    engine.dispose()


@pytest.fixture()
def session(database):
    Session, engine = database
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture()
def alice(session):
    alice = User(name="alice", password="0" * 128)
    session.add(alice)
    session.commit()
    return alice


def test_user_create(session):
    alice = User(name="alice", password="0" * 128)
    session.add(alice)
    session.commit()


def test_user_read(alice, session):
    user = session.query(User).first()
    assert user is alice
    assert user.id == 1
    assert user.name == "alice"
    assert user.password == "0" * 128


def test_user_update(alice, session):
    alice.password = "1" * 128
    session.add(alice)
    session.commit()

    user = session.query(User).first()
    assert user is alice
    assert user.id == 1
    assert user.name == "alice"
    assert user.password == "1" * 128


def test_user_delete(alice, session):
    session.delete(alice)
    session.commit()

    user = session.query(User).first()
    assert user is None
