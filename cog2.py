import discord
from discord.ext import commands
from bd.functions import add_user
from time import time
import random
from config import data
import discord
from discord.utils import get
from bd.main import Base, engine, Users, select
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
styles=[discord.ButtonStyle.gray, discord.ButtonStyle.primary, discord.ButtonStyle.danger, discord.ButtonStyle.green, discord.ButtonStyle.red]
class RoleButton(discord.ui.Button):
	def __init__(self):
		"""A button for one role. `custom_id` is needed for persistent views."""
		super().__init__(
			label='Стать жителем Альт-Сити',
			style=random.choice(styles),
			custom_id=f'15',
		)

	async def callback(self, interaction: discord.Interaction):
		async_session = scoped_session(sessionmaker(
			engine, expire_on_commit=False, class_=AsyncSession
		))
		async with async_session() as session:
			async with session.begin():
				res=await add_user(interaction.user.id, session)
				await interaction.response.send_message(f'{res}', ephemeral=True)
				if res == 'Успешная регистрация жителя Альт-Сити.':
					role = get(interaction.user.guild.roles, id=data.roles['CH']['id'])
					await interaction.user.add_roles(role)
				await session.close()
				#view2.add_item(RoleButton())
				#await message.edit(view=)
class Dropdown(discord.ui.Select):
	def __init__(self, bot_: discord.Bot):
		# For example, you can use self.bot to retrieve a user or perform other functions in the callback.
		# Alternatively you can use Interaction.client, so you don't need to pass the bot instance.
		self.bot = bot_
		# Set the options that will be presented inside the dropdown:
		options = []
		for role in data.rolesd:
			if role['admin'] == 0:
				options.append(discord.SelectOption(label=role['name'], description=role['description'], emoji=role['sticker'], value=str(role['id'])))
		# The placeholder is what will be shown when no option is selected.
		# The min and max values indicate we can only pick one of the three options.
		# The options parameter, contents shown above, define the dropdown options.
		super().__init__(
			placeholder="Выбери свою профессию",
			min_values=1,
			max_values=1,
			options=options,
		)

	async def callback(self, interaction: discord.Interaction):
		# Use the interaction object to send a response message containing
		# the user's favourite colour or choice. The self object refers to the
		# Select object, and the values attribute gets a list of the user's
		# selected options. We only want the first one.
		async_session = scoped_session(sessionmaker(
			engine, expire_on_commit=False, class_=AsyncSession
		))
		async with async_session() as session:
			async with session.begin_nested():
				usera = await session.execute(select(Users).where(Users.id == interaction.user.id))
				user = usera.scalars().first()
				if user:
					if user.last_pos == 'emporium':
						rol=get(interaction.user.guild.roles, id=int(interaction.data['values'][0]))
						#rol_b = get(interaction.guild.roles, id=interaction.data['values'])
						await interaction.response.send_message(f"Ты выбрал роль {rol.name}.", ephemeral=True)
						for rol2 in interaction.user.roles:
							if rol2.id in data.rolesid:
								await interaction.user.remove_roles(rol2)
								user.role=data.rolesi[int(interaction.data['values'][0])]
						await interaction.user.add_roles(rol)
					else:
						await interaction.response.send_message(
							f"Профессию можно менять только в эмпориуме.",
							ephemeral=True)

				else:
					await interaction.response.send_message(f"Слушай, {interaction.user.mention}, мне кажется стоит сначала стать жителем.", ephemeral=True)
				await session.commit()
				await session.close()
# Defines a simple View that allows the user to use the Select menu.
class DropdownView(discord.ui.View):
	def __init__(self, bot_: discord.Bot):
		self.bot = bot_
		super().__init__()

		# Adds the dropdown to our View object
		self.add_item(Dropdown(self.bot))

		# Initializing the view and adding the dropdown can actually be done in a one-liner if preferred:
		# super().__init__(Dropdown(self.bot))
class Locations(discord.ui.Select):
	def __init__(self, bot_: discord.Bot):
		# For example, you can use self.bot to retrieve a user or perform other functions in the callback.
		# Alternatively you can use Interaction.client, so you don't need to pass the bot instance.
		self.bot = bot_
		# Set the options that will be presented inside the dropdown:
		options = [
			discord.SelectOption(label='Работа', description='', emoji='🚶',
			                     value='work')
		]
		for location in data.locationsn:
			options.append(discord.SelectOption(label=location['name'], description=location['description'], emoji='🚶', value=str(location['role'])))
		# The placeholder is what will be shown when no option is selected.
		# The min and max values indicate we can only pick one of the three options.
		# The options parameter, contents shown above, define the dropdown options.
		super().__init__(
			placeholder="Куда вы хотите пойти?",
			min_values=1,
			max_values=1,
			options=options,
		)

	async def callback(self, interaction: discord.Interaction):
		# Use the interaction object to send a response message containing
		# the user's favourite colour or choice. The self object refers to the
		# Select object, and the values attribute gets a list of the user's
		# selected options. We only want the first one.
		#rol_b = get(interaction.guild.roles, id=interaction.data['values'])
		async_session = scoped_session(sessionmaker(
			engine, expire_on_commit=False, class_=AsyncSession
		))
		if interaction.data['values'][0] == 'work':
			async with async_session() as session:
				async with session.begin():
					usera = await session.execute(select(Users).where(Users.id == interaction.user.id))
					user = usera.scalars().first()
					if user:
						for rol2 in interaction.user.roles:
							if rol2.id in data.location_roles:
								await interaction.user.remove_roles(rol2)
						if user.in_path:
							await interaction.response.send_message(
						f"Ты уже идешь куда-то, уж извини, пока что маршрут нельзя менять, жди обнову)",
						ephemeral=True)
							return 'no'
					else:
						await interaction.response.send_message(f"Слушай, {interaction.user.mention}, мне кажется стоит сначала стать жителем.", ephemeral=True)
			#or rol2.id in data.work_roles
					await session.commit()
					await session.close()
		else:
			async with async_session() as session:
				async with session.begin():
					usera = await session.execute(select(Users).where(Users.id == interaction.user.id))
					user = usera.scalars().first()
					if user:
						for rol2 in interaction.user.roles:
							if rol2.id in data.location_roles:
								await interaction.user.remove_roles(rol2)
						if user.in_path:
							await interaction.response.send_message(
					f"Ты уже идешь куда-то, уж извини, пока что маршрут нельзя менять, жди обнову)",
							ephemeral=True)
							return 'no'
						user.next_pos=data.locationsbn[interaction.data['values'][0]]['role']
						await interaction.response.send_message(
								f"Ты выбрал отправился в {data.locationsbn[interaction.data['values'][0]]['name']}. Идти туда надо 5 секунд.",
					ephemeral=True)
						user.in_path=True
						user.next=time()+5
						user.last_pos=None
					else:
						await interaction.response.send_message(f"Слушай, {interaction.user.mention}, мне кажется стоит сначала стать жителем.", ephemeral=True)
			#or rol2.id in data.work_roles
					await session.commit()
					await session.close()
# Defines a simple View that allows the user to use the Select menu.
class LocationsView(discord.ui.View):
	def __init__(self, bot_: discord.Bot):
		self.bot = bot_
		super().__init__()

		# Adds the dropdown to our View object
		self.add_item(Locations(self.bot))

		# Initializing the view and adding the dropdown can actually be done in a one-liner if preferred:
		# super().__init__(Dropdown(self.bot))
