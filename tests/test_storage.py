import pytest

from app.storage import Storage


@pytest.fixture
async def storage():
    store = Storage(":memory:")
    await store.connect()
    yield store
    await store.close()


async def test_get_returns_none_when_unset(storage):
    assert await storage.get_target_lang(42) is None


async def test_set_then_get(storage):
    await storage.set_target_lang(42, "French")
    assert await storage.get_target_lang(42) == "French"


async def test_set_overwrites_existing(storage):
    await storage.set_target_lang(42, "French")
    await storage.set_target_lang(42, "German")
    assert await storage.get_target_lang(42) == "German"


async def test_settings_are_per_user(storage):
    await storage.set_target_lang(1, "Spanish")
    await storage.set_target_lang(2, "Japanese")
    assert await storage.get_target_lang(1) == "Spanish"
    assert await storage.get_target_lang(2) == "Japanese"
