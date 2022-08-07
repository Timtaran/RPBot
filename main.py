import time

import discord
from vkbottle.tools.dev.loop_wrapper import LoopWrapper
from discord.utils import get
from bd.functions import help, get_info, add_user
from bd import functions
from discord import option
import random
from cog2 import RoleButton, DropdownView, select, Users, LocationsView
from config import *
lw = LoopWrapper()

overwrite_everyone = discord.PermissionOverwrite()
overwrite_everyone.view_channel=False
overwrite_everyone.connect=False

overwrite_work = discord.PermissionOverwrite()
overwrite_work.view_channel=True
overwrite_work.send_messages=False
overwrite_work.create_public_threads=False
overwrite_work.create_private_threads=False
overwrite_work.connect=True
overwrite_work.speak=False

overwrite_chat = discord.PermissionOverwrite()
overwrite_chat.view_channel=True
overwrite_chat.send_messages=True
overwrite_chat.create_public_threads=True
overwrite_chat.create_private_threads=True
overwrite_chat.connect=True
overwrite_work.speak=True
##################
@lw.interval(seconds=3)
async def repeated_task():
	session = data.session
	async with session.begin_nested():
		result = await session.execute(select(Users))
		a1 = result.scalars().fetchall()
		for user in a1:
			if user.next:
				if user.next_pos in data.rolesi:
					user.last_pos = 'work'
					user.in_path = False
					user.next_pos = None
					user.next = None
					user_d = await bot.fetch_user(user.id)
					await user_d.send(f"Вы пришли в {data.locationsbn[user.last_pos]['name']} ебать")
					role = get(bot.get_guild(guild).roles, id=data.locationsbn[user.last_pos]['role_id'])
					guild2 = bot.get_guild(guild)
					user2 = await guild2.fetch_member(user.id)
					await user2.add_roles(role)
				elif user.next < time.time():
					user.last_pos=user.next_pos
					user.in_path=False
					user.next_pos=None
					user.next=None
					user_d=await bot.fetch_user(user.id)
					await user_d.send(f"Вы пришли в {data.locationsbn[user.last_pos]['name']} ебать")
					role=get(bot.get_guild(guild).roles, id=data.locationsbn[user.last_pos]['role_id'])
					guild2 = bot.get_guild(guild)
					user2=await guild2.fetch_member(user.id)
					await user2.add_roles(role)
		await session.commit()
		await session.close()
async def create_db():
	await functions.create()
@logger.catch
@bot.event
async def on_ready(*args, **kwargs):
	await data.create_session()
	#await create_db()
	lw.run_forever(loop=bot.loop)
	view = DropdownView(bot)
	channel = bot.get_channel(1003661876393148558)
	view2 = discord.ui.View()
	view2.add_item(RoleButton())
	await channel.purge()
	data.createPeople = await channel.send("Чтобы попасть в Альт-Сити нажмите кнопку ниже.", view=view2)
	await channel.send('Выберите профессию:', view=view)
	await channel.send('Куда вы хотите пойти?', view=LocationsView(bot))
	logger.debug('ready')
############################
@logger.catch
@discord.default_permissions(administrator=True)
@bot.slash_command()
async def setup(ctx: discord.ApplicationContext):
	def add(mes, msg):
		msg = msg + f"{mes} \n"
		return msg
	msg=''
	await ctx.respond(f'Начинаю создание ролей...', ephemeral=True)
	names=[]
	for rol in ctx.guild.roles:
		names.append(rol.name)
	for rol2 in data.rolesn:
		if rol2 not in names:
			channel=await ctx.guild.create_role(name=rol2)
			await ctx.author.send(f'Создана новая роль "{rol2}", ID роли - {channel.id}, сообщите его <@440408198168576001> для добавления в конфиг.')
			msg = add(f"self.roles['{data.rolesh[rol2]}']['id'] = {channel.id}",msg)
	await ctx.respond(f'Начинаю создание категорий и каналов...', ephemeral=True)
	ct = []
	chnls = []
	for cat in ctx.guild.categories:
		ct.append(cat.name)
		for chn in cat.channels:
			chnls.append(chn.name)
	for cat2 in data.locations:
		cat3=data.locations[cat2]
		logger.debug(cat3)
		logger.debug(cat2)
		logger.debug(ct)
		if cat3['name'] not in ct:
			logger.debug(cat3)
			logger.debug(cat2)
			logger.debug(ct)
			category= await ctx.guild.create_category(name=cat3['name'])
			await ctx.author.send(
				f'Создана новая категория "{category.name}", ID категории - {category.id}, сообщите его <@440408198168576001> для добавления в конфиг.')
			msg = add(f"self.locations['{cat2}']['id'] = {category.id}", msg)
			for ch in cat3['locations']:
				chn=cat3['locations'][ch]
				role = await ctx.guild.create_role(name=chn['name'])
				await ctx.author.send(
					f'Создана новая роль "{role.name}", ID роли - {role.id}, сообщите его <@440408198168576001> для добавления в конфиг.')
				msg = add(f"self.locations['{cat2}']['locations']['{ch}']['role_id'] = {role.id}", msg)
				channel_chat = await ctx.guild.create_text_channel(category=category, name=chn['name'].lower().replace(' ', '-'))
				await ctx.author.send(
					f'Создан новый чат "{channel_chat.name}", ID чата - {channel_chat.id}, сообщите его <@440408198168576001> для добавления в конфиг.')
				msg = add(f"self.locations['{cat2}']['locations']['{ch}']['chat_id'] = {channel_chat.id}", msg)
				await channel_chat.set_permissions(ctx.guild.default_role, overwrite=overwrite_everyone)
				await channel_chat.set_permissions(role, overwrite=overwrite_chat)
		else:
			for locat in cat3['locations']:
				category=get(ctx.guild.categories, id=cat3['id'])
				loce = cat3['locations'][locat]
				logger.debug(loce['name'].lower().replace(' ', '-'))
				logger.debug(chnls)
				if loce['name'].lower().replace(' ', '-') not in chnls:
					role = await ctx.guild.create_role(name=loce['name'])
					await ctx.author.send(
						f'Создана новая роль "{role.name}", ID роли - {role.id}, сообщите его <@440408198168576001> для добавления в конфиг.')
					msg = add(f"self.locations['{cat2}']['locations']['{locat}']['role_id'] = {role.id}", msg)
					channel_chat = await ctx.guild.create_text_channel(category=category,
					                                                   name=loce['name'].lower().replace(' ', '-'))
					await ctx.author.send(
						f'Создан новый чат "{channel_chat.name}", ID чата - {channel_chat.id}, сообщите его <@440408198168576001> для добавления в конфиг.')
					msg = add(f"self.locations['{cat2}']['locations']['{locat}']['chat_id'] = {channel_chat.id}", msg)
					await channel_chat.set_permissions(ctx.guild.default_role, overwrite=overwrite_everyone)
					await channel_chat.set_permissions(role, overwrite=overwrite_chat)
	await ctx.respond(f'Начинаю создание работ...', ephemeral=True)
	logger.debug('Я дошел до работ')
	if 'Работы' in ct:
		categ=get(ctx.guild.categories, name='Работы')
	else:
		categ=await ctx.guild.create_category(name='Работы')
		await ctx.author.send(f'Создана категория Работы, ее ID - {categ.id}, сообщите эту информацию <@440408198168576001>.')
	channels=[]
	for channel in ctx.guild.channels:
		channels.append(channel.name)
	for work in data.rolesd:
		logger.debug(work)
		if work['name']+" Чат" in channels or work['name'].lower()+"-чат" in channels:
			logger.debug(work)
		else:
			role = await ctx.guild.create_role(name=work['name'] + " Работа")
			await ctx.author.send(f'Создана новая роль "{role.name}", ID роли - {role.id}, сообщите его <@440408198168576001> для добавления в конфиг.')
			msg = add(f"self.roles['{data.rolesh[work['name']]}']['role_id'] = {role.id}", msg)
			channel_work=await ctx.guild.create_text_channel(name=work['name'].lower().replace(' ', '-')+"-работа", category=categ)
			channel_chat_tc = await ctx.guild.create_text_channel(name=work['name'].lower().replace(' ', '-') + "-чат", category=categ)
			channel_chat_vc = await ctx.guild.create_voice_channel(name=work['name'] + " Чат", category=categ)
			await ctx.author.send(
				f'Были созданы каналы (channel_work, channel_chat_tc, channel_chat_vc) их ID - {channel_work.id}, {channel_chat_tc.id}, {channel_chat_vc.id} (соответственно).')
			msg = add(f"self.roles['{data.rolesh[work['name']]}']['work_id'] = {channel_work.id}", msg)
			msg = add(f"self.roles['{data.rolesh[work['name']]}']['chatt_id'] = {channel_chat_tc.id}", msg)
			msg = add(f"self.roles['{data.rolesh[work['name']]}']['chatv_id'] = {channel_chat_vc.id}", msg)
			await channel_work.set_permissions(ctx.guild.default_role, overwrite=overwrite_everyone)
			await channel_work.set_permissions(role, overwrite=overwrite_work)
			await channel_chat_tc.set_permissions(ctx.guild.default_role, overwrite=overwrite_everyone)
			await channel_chat_tc.set_permissions(role, overwrite=overwrite_chat)
			await channel_chat_vc.set_permissions(ctx.guild.default_role, overwrite=overwrite_everyone)
			await channel_chat_vc.set_permissions(role, overwrite=overwrite_chat)
	await ctx.respond(f'Установка завершена', ephemeral=True)
	file = open(f'file-{random.randint(1, 9999)}-{random.choice(help)}.txt', 'w')
	file.write(msg)
	file.close()
@logger.catch
@discord.default_permissions(administrator=True)
@bot.slash_command(description="Если ты используешь эту команду, то всему живому пиздец(а если точнее, то категории).")
async def clear(ctx: discord.ApplicationContext):
	locations = []# delcategory is our ID (category)
	roles=[]
	msg=""
	for rol2 in data.rolesd:
		roles.append(rol2['id'])
	for loc in data.locations:
		locations.append(data.locations[loc]['name']) # Get all channels of the category
	await ctx.respond(f'Начинаю чистку сервера от бота... (перед началом очистите конфиг, бот оставит все роли персонажей)', ephemeral=True)
	await ctx.respond(f'Удаляю роли...', ephemeral=True)
	for role in ctx.guild.roles:
		for rol in data.rolesn:
			if rol in role.name:
				if role.id not in roles:
					await role.delete()
	await ctx.respond(f'Удаляю категории и каналы...', ephemeral=True)
	for category in ctx.guild.categories:
		if category.name in locations:
			for channel in category.channels: # We search for all channels in a loop
				try:
					await channel.delete() # Delete all channels
				except AttributeError: # If the category does not exist/channels are gone
					pass
			await category.delete()
	await ctx.respond(f'Чистка завершена :)', ephemeral=True)

bot.run(token)