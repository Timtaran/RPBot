import asyncio

from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from .all import info
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload

from .config2 import other
engine = create_async_engine(
        "sqlite+aiosqlite:///database.sqlite3",
        echo=False,
    encoding='utf8', future=True
    )
Base = declarative_base(bind=engine)
metadata = Base.metadata
async_session = scoped_session(sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    ))
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tag = Column(String)
    role=Column(String)
    level=Column(String)
    balance=Column(Integer)
    last_pos=Column(String)
    next=Column(Integer)
    next_pos = Column(String)
    in_path = Column(Boolean)
    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}
