from sqlalchemy.orm import sessionmaker

async_session_factory: sessionmaker | None = None
sync_session_factory: sessionmaker | None = None

def get_async_factory() -> sessionmaker:
    return async_session_factory

def get_sync_factory() -> sessionmaker:
    return sync_session_factory
