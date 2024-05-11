from sqlalchemy.ext.asyncio import create_async_engine
from settings import DB_URI

engine = create_async_engine(DB_URI)
