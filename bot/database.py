import logging
from enum import Enum
from typing import Optional

from pony import orm
from datetime import datetime

from config import Config

logger = logging.getLogger(__name__)
db = orm.Database()


class User(db.Entity):
    __table__ = "users"
    id = orm.PrimaryKey(int, size=64)
    name = orm.Required(str)
    username = orm.Optional(str, nullable=True)
    started_at = orm.Required(datetime, default=datetime.utcnow)


class History(db.Entity):
    __table__ = "history"
    chat_id = orm.Required(int, size=64)
    author = orm.Required(str)
    name = orm.Required(str)
    message = orm.Required(str)


if not any((Config.DB_HOST, Config.DB_USER, Config.DB_PASSWORD, Config.DB_NAME)):
    logger.warning("External Database not configured. Using SQLite instead.")
    db.bind(provider="sqlite", filename="data.db", create_db=True)

else:
    db.bind(
        provider="postgres",
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        sslmode="require",
    )
    logger.info("Postgres Database configured.")

db.generate_mapping(create_tables=True)

# ==============================================================================
# https://docs.ponyorm.org/integration_with_fastapi.html#async-and-db-session ||
# ==============================================================================

async def add_user(id: int, name: str, username: Optional[str]):
    with orm.db_session:
        if not User.exists(id=id):
            try:
                User(id=id, name=name, username=username)
            except (orm.IntegrityError, orm.TransactionIntegrityError):
                return False
            return True
        return False


async def set_user_history(user_id: int, name: str, message: str):
    with orm.db_session:
        History(chat_id=user_id, name=name, message=message, author="user")
        db.commit()


async def set_response_history(user_id: int, name: str, message: str):
    with orm.db_session:
        History(chat_id=user_id, name=name, message=message, author="model")
        db.commit()


async def get_history(user_id: int) -> list[History]:
    with orm.db_session:
        return list(
            reversed(
                list(
                    History.select(lambda h: h.chat_id == user_id)
                    .order_by(orm.desc(History.id))
                    .limit(20)
                )
            )
        )


async def clear_history(user_id: int):
    with orm.db_session:
        orm.select(h for h in History if h.chat_id == user_id).delete(bulk=True)
