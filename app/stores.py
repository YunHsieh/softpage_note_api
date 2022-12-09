import ormar
import databases
import sqlalchemy
import pydantic

from app import environments as envs
from sqlalchemy.orm import Session

metadata = sqlalchemy.MetaData()
database = databases.Database(envs.DATABASE_URI)


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata
    extra = pydantic.Extra.ignore


def init_database(app):
    app.state.database = database

    @app.on_event('startup')
    async def startup() -> None:
        database_ = app.state.database
        if not database_.is_connected:
            await database_.connect()

    @app.on_event('shutdown')
    async def shutdown() -> None:
        database_ = app.state.database
        if database_.is_connected:
            await database_.disconnect()
