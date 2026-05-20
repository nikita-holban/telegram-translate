from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    anthropic_api_key: str
    anthropic_model: str
    default_target_lang: str
    db_path: str


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            "Copy .env.example to .env and fill it in."
        )
    return value


def load_config() -> Config:
    return Config(
        bot_token=_require("BOT_TOKEN"),
        anthropic_api_key=_require("ANTHROPIC_API_KEY"),
        anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5"),
        default_target_lang=os.getenv("DEFAULT_TARGET_LANG", "English"),
        db_path=os.getenv("DB_PATH", "data/bot.db"),
    )
