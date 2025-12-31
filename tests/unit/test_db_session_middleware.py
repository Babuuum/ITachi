import asyncio

import pytest

from bot.middlewares.db_session import DbSessionMiddleware

pytestmark = pytest.mark.anyio


class FakeSession:
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True


def session_factory_bucket():
    bucket = []

    def factory():
        session = FakeSession()
        bucket.append(session)
        return session

    return factory, bucket


async def test_db_session_middleware_commits():
    factory, bucket = session_factory_bucket()
    middleware = DbSessionMiddleware(factory)

    async def handler(event, data):
        assert "session" in data
        assert data["session"] is bucket[0]
        return "ok"

    result = await middleware(handler, event=object(), data={})

    assert result == "ok"
    assert bucket[0].committed is True
    assert bucket[0].rolled_back is False


async def test_db_session_middleware_rolls_back_on_error():
    factory, bucket = session_factory_bucket()
    middleware = DbSessionMiddleware(factory)

    async def handler(event, data):
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        await middleware(handler, event=object(), data={})

    assert bucket[0].committed is False
    assert bucket[0].rolled_back is True
