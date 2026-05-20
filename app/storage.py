from __future__ import annotations

import os

import aiosqlite


class Storage:
    """Per-user settings persisted in SQLite (the default target language)."""

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._db: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        parent = os.path.dirname(self._db_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        self._db = await aiosqlite.connect(self._db_path)
        await self._db.execute(
            "CREATE TABLE IF NOT EXISTS user_settings ("
            "user_id INTEGER PRIMARY KEY, "
            "target_lang TEXT NOT NULL)"
        )
        await self._db.commit()

    async def close(self) -> None:
        if self._db is not None:
            await self._db.close()
            self._db = None

    async def get_target_lang(self, user_id: int) -> str | None:
        db = self._require_db()
        async with db.execute(
            "SELECT target_lang FROM user_settings WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()
        return row[0] if row else None

    async def set_target_lang(self, user_id: int, target_lang: str) -> None:
        db = self._require_db()
        await db.execute(
            "INSERT INTO user_settings (user_id, target_lang) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET target_lang = excluded.target_lang",
            (user_id, target_lang),
        )
        await db.commit()

    def _require_db(self) -> aiosqlite.Connection:
        if self._db is None:
            raise RuntimeError("Storage.connect() must be called first")
        return self._db
