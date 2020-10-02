import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from impressoras import config
from impressoras.models import Base, User


@pytest.fixture(scope='module')
def Session():
    engine = create_engine(config.TEST_DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    yield Session
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture()
def session(Session):
    session = Session()
    yield session
    session.rollback()
    session.close()


def test_user_crud(session):
    # Create
    alice = User(name='alice', password='0' * 128)
    session.add(alice)
    session.flush()

    # Read
    user = session.query(User).first()
    assert user is alice
    assert user.id == 1
    assert user.name == 'alice'
    assert user.password == '0' * 128

    # Update
    alice.password = '1' * 128
    session.add(alice)
    session.flush()
    
    user = session.query(User).first()
    assert user is alice
    assert user.id == 1
    assert user.name == 'alice'
    assert user.password == '1' * 128

    # Delete
    session.delete(alice)
    session.flush()

    user = session.query(User).first()
    assert user is None
