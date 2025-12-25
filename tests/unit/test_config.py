import importlib
import os

import pytest


@pytest.mark.parametrize(
    "user,password,host,port,name",
    [
        ("u", "p", "h", "5432", "db"),
        ("user2", "pass2", "localhost", "6543", "example"),
    ],
)
def test_database_url_builds(monkeypatch, user, password, host, port, name):
    monkeypatch.setenv("PROD_DB_USER", user)
    monkeypatch.setenv("PROD_DB_PASSWORD", password)
    monkeypatch.setenv("PROD_DB_HOST", host)
    monkeypatch.setenv("PROD_DB_PORT", port)
    monkeypatch.setenv("PROD_DB_NAME", name)

    module = importlib.import_module("core.config")
    monkeypatch.setattr(module, "_settings", None)

    settings = module.get_settings()

    expected = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
    assert settings.database_url == expected

    # Cleanup to avoid leaking env to other tests
    for key in [
        "PROD_DB_USER",
        "PROD_DB_PASSWORD",
        "PROD_DB_HOST",
        "PROD_DB_PORT",
        "PROD_DB_NAME",
    ]:
        monkeypatch.delenv(key, raising=False)
