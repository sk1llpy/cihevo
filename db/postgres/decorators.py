from db.postgres.handlers import BaseSessionHandler
import functools


def create_async_session(func, facroty: BaseSessionHandler):
    """
    Create session for database access.
    """

    @functools.wraps(func)
    async def inner(*args, **kwargs):
        if not kwargs.get("session"):
            async with facroty.async_session_scope() as session:
                kwargs["session"] = session
        result = await func(*args, **kwargs)
        return result
    return inner


def create_sync_session(func, facroty: BaseSessionHandler):
    """
    Create session for database access.
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        if not kwargs.get("sync_session"):
            with facroty.sync_session_scope() as session:
                kwargs["sync_session"] = session
        result = func(*args, **kwargs)
        return result
    return inner
