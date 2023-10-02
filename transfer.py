import logging


from pony import orm
from datetime import datetime

from config import Config

logger = logging.getLogger(__name__)

remote_db = orm.Database()


class RemoteUser(remote_db.Entity):
    __table__ = "users"
    id = orm.PrimaryKey(int, size=64)
    name = orm.Required(str)
    username = orm.Optional(str)
    started_at = orm.Required(datetime, default=datetime.utcnow)


class RemoteHistory(remote_db.Entity):
    __table__ = "history"
    chat_id = orm.Required(int, size=64)
    author = orm.Required(str)
    name = orm.Required(str)
    message = orm.Required(str)



remote_db.bind(
    provider="postgres",
    host=Config.DB_HOST,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    database=Config.DB_NAME,
    sslmode="require",
)
logger.info("Postgres Database configured.")

remote_db.generate_mapping(create_tables=True)

local_db = orm.Database()

class LocalUser(local_db.Entity):
    __table__ = "users"
    id = orm.PrimaryKey(int, size=64)
    name = orm.Required(str)
    username = orm.Optional(str, nullable=True)
    started_at = orm.Required(datetime, default=datetime.utcnow)


class LocalHistory(local_db.Entity):
    __table__ = "history"
    chat_id = orm.Required(int, size=64)
    author = orm.Required(str)
    name = orm.Required(str)
    message = orm.Required(str)

local_db.bind(provider="sqlite", filename="local.db", create_db=True)
logger.info("Local Database configured.")

with orm.db_session:
    for user in RemoteUser.select():
        if local_user := LocalUser.get(id=user.id):
            local_user.name = user.name
            local_user.username = user.username or None
            local_user.started_at = user.started_at
        else:
            LocalUser(id=user.id, name=user.name, username=user.username, started_at=user.started_at)
    orm.commit()

logger.info("Users transferred.")

with orm.db_session:
    for history in LocalHistory.select():
        local_history = LocalHistory.get(chat_id=history.chat_id, author=history.author, message=history.message)
        if not local_history:
            LocalHistory(chat_id=history.chat_id, author=history.author, name=history.name, message=history.message)
    orm.commit()

logger.info("History transferred.")
logger.info("Transfer complete.")