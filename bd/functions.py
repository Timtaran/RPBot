import asyncio, string, random

from sqlalchemy import Column
from sqlalchemy import DateTime
from .all import info
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from .main import Base, engine, async_session
from .main import Users as A
help = [i for i in string.ascii_uppercase]
print(help)
import discord
from discord.utils import get
async def create():
	"""Main program function."""
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
		await conn.run_sync(Base.metadata.create_all)

	# expire_on_commit=False will prevent attributes from being expired
	# after commit.
	async_session = sessionmaker(
		engine, expire_on_commit=False, class_=AsyncSession
	)

	async with async_session() as session:
		async with session.begin():
			session.add_all(
				[
				]
			)

		await session.commit()

		# access attribute subsequent to commit; this is what
		# expire_on_commit=False allow
async def get_info(id):
	async with async_session() as session:
		async with session.begin():
			#async_result = await conn.stream(select(A).where(A.id == 549204433))
			#return async_result.scalars().first()
			result = await session.execute(select(A).where(A.id == id))
			a1 = result.scalars().first()
			return a1
async def get_info2(id, session):
	result = await session.execute(select(A).where(A.id == id))
	a1 = result.scalars().first()
	return a1
async def get_tag(tag, session):
	print(tag)
	result = await session.execute(select(A).where(A.tag == tag))
	a1 = result.scalars().first()
	print(a1)
	return a1
async def add_user(id, session):
	if await get_info2(id, session):
		return 'Вы уже являетесь жителем Альт-Сити.'
	gen=True
	while gen:
		tag=f'{random.choice(help)}-{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}'
		if await get_tag(tag, session) == None:
			gen=False
			session.add_all(
				[
					A(id=id,
					  tag=tag,
					  role='CH',
					  level='Low',
					  balance=0)

				]
			)
			await session.commit()
			return 'Успешная регистрация жителя Альт-Сити.'