import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.db.base import Base


class AsyncSessionWrapper:
    """Lightweight async-compatible wrapper around a sync SQLAlchemy session for tests."""

    def __init__(self, sync_session):
        self._sync_session = sync_session

    def add(self, obj):
        self._sync_session.add(obj)

    def add_all(self, objs):
        self._sync_session.add_all(objs)

    async def scalars(self, *args, **kwargs):
        return self._sync_session.scalars(*args, **kwargs)

    async def execute(self, *args, **kwargs):
        return self._sync_session.execute(*args, **kwargs)

    async def get(self, *args, **kwargs):
        return self._sync_session.get(*args, **kwargs)

    async def commit(self):
        self._sync_session.commit()

    async def rollback(self):
        self._sync_session.rollback()

    async def delete(self, obj):
        self._sync_session.delete(obj)

    async def close(self):
        self._sync_session.close()

    def begin(self):
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            self._sync_session.rollback()
        else:
            self._sync_session.commit()
        self._sync_session.close()
        return False


@pytest.fixture()
def test_engine():
    """Synchronous SQLite engine for tests (wrapped for async interfaces)."""
    engine = create_engine(
        "sqlite:///:memory:",
        future=True,
    )
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture()
async def db_session(test_engine):
    """Provide an async-compatible session wrapper backed by a sync engine."""
    sync_session_factory = sessionmaker(test_engine, expire_on_commit=False)
    sync_session = sync_session_factory()
    session_wrapper = AsyncSessionWrapper(sync_session)
    try:
        yield session_wrapper
    finally:
        await session_wrapper.rollback()
