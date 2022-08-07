import discord
from bd.main import Base, engine, async_session, Users, select
from loguru import logger
intents = discord.Intents.all()
logger.info('Создаю инстанс бота')
bot = discord.Bot(intents=intents)
logger.info('Инстанс бота создан, создаю класс')
guild=1003620185711853618
import sys
class Data:
	def __init__(self):
		self.roles = {}
		self.locations = {
	'city_streets' : {'name':'[RP] Улицы в городе', 'id':1004035855314329600, 'locations':{}},
		'undercity_locations' : {'name': '[RP] Загород', 'id':1004035874960449607, 'locations':{}}
		}
		self.rolesd=[]
		self.rolesn=[]
		self.rolesid=[]
		self.locationsn=[]
		self.rolesh={}
		self.rolesi={}
		self.location_roles=[]
		self.work_roles = []
		self.locationsbn={}
		self.createPeople=discord.message.Message
		logger.info("Начинаю генерацию данных")
		self.set_locations()
		self.set_roles()
		self.paste()
		self.generate_data()
		logger.info("Генерация данных завершена")
		logger.debug('Начинаю вывод информации...\n\n')
		logger.debug('')
		for dikt in self.__dict__:
			logger.debug(f'{dikt} - \n{self.__dict__[dikt]}')

	@logger.catch
	def set_locations(self):
		self.locations['city_streets']['locations']['AllaSt']={
		'name': 'Улица Алы',
			'description':''
	}
		self.locations['city_streets']['locations']['cherruDetective']={
			'name': 'Детективное Агенство cherru',
			'description':''
		}
		self.locations['city_streets']['locations']['emporium']= {
			'name':'Эмпориум',
			'description':''
		}
		self.locations['city_streets']['locations']['KavinskiAvto'] = {
			'name': 'Автосервис Кавински',
			'description':''
		}
		self.locations['city_streets']['locations']['RadanHouse'] = {
			'name': 'Дом Радана',
			'description':''
		}
		self.locations['city_streets']['locations']['KateHouse'] = {
			'name': 'Дом Кейт',
			'description':''
		}
		self.locations['city_streets']['locations']['BomjSt'] = {
			'name': 'Улица Бомжей',
			'description':''
		}
		self.locations['city_streets']['locations']['MainPl'] = {
			'name': 'Центральная площадь',
			'description':''
		}
		self.locations['city_streets']['locations']['CRK'] = {
			'name': 'Церковь',
			'description':''
		}
		#self.locations['city_streets']['locations'][''] = {
		#	'name': ''
		#}
		self.locations['works'] = {
			'name':'Работы', 'locations' : {}
		}
	async def create_session(self):
		async with async_session() as session:
				self.session=session
	@logger.catch
	def generate_data(self):
		logger.info('Создаю локации...')
		for locations in self.locations:
			logger.debug(locations)
			logger.debug(self.locations)
			loc=self.locations[locations]
			logger.debug(loc)
			for location in loc['locations']:
				for name in ['role_id', 'chat_id']:
					if name not in loc['locations'][location]:
						loc['locations'][location][name] = None
				logger.debug(location)
				paste_data={
				'role':location,
					'category':locations,
					'name':loc['locations'][location]['name'],
					'role_id': loc['locations'][location]['role_id'],
					'description':loc['locations'][location]['description']
				}
				self.locationsn.append(paste_data)
				self.locationsbn[location]=paste_data
				try:
					self.location_roles.append(loc['locations'][location]['role_id'])
				except KeyError:
					pass
				logger.debug(self.locationsn)
		logger.info('Создаю роли...')
		for role in self.roles:
			role2 = self.roles[role]
			self.rolesh[role2['name']] = role
			self.rolesi[role2['id']] = role
			self.rolesd.append({
				'name': role2['name'],
				'description': role2['description'],
				'sticker': role2['sticker'],
			    'id': role2['id'],
			    'admin': role2['admin'],
			'role':role})
			self.work_roles.append(role2['role_id'])
			self.rolesn.append(role2['name'])
			self.rolesid.append(role2['id'])
	@logger.catch
	def set_roles(self):
		self.roles={
			'AV': {'name': 'Аниме Даббер', 'description': '', 'sticker': '😀', 'id': 0, 'admin': 0},
			'CH': {'name': 'Дитя', 'description': '', 'sticker': '😉', 'id': 0, 'admin': 1},
			'PL': {'name': 'Полицейский', 'description': '', 'sticker': '😉', 'id': 0, 'admin': 1},
			'ST': {'name': 'Секретарь', 'description': '', 'sticker': '😉', 'id': 0, 'admin': 1},
			'SC': {'name': 'Начинающий Комиссар', 'description': '', 'sticker': '😉', 'id': 0,
			       'admin': 1},
			'MC': {'name': 'Лучший Коммисар', 'description': '', 'sticker': '😉', 'id': 0,
			       'admin': 1},
			'BM': {'name': 'Бармен', 'description': '', 'sticker': '😉', 'id': 0, 'admin': 0},
			'CL': {'name': 'Клоун', 'description': '', 'sticker': '😉', 'id': 0, 'admin': 0},
			'BH': {'name': 'Бугхалтер', 'description': '', 'sticker': '😉', 'id': 1004006553059328000, 'admin': 0},
		}
	def paste(self):
		self.locations['city_streets']['locations']['AllaSt']['role_id'] = 1004295850396225556
		self.locations['city_streets']['locations']['AllaSt']['chat_id'] = 1004295853596491896
		self.locations['city_streets']['locations']['cherruDetective']['role_id'] = 1004295859128762408
		self.locations['city_streets']['locations']['cherruDetective']['chat_id'] = 1004295861636976710
		self.locations['city_streets']['locations']['emporium']['role_id'] = 1004295866338791514
		self.locations['city_streets']['locations']['emporium']['chat_id'] = 1004295868867940394
		self.locations['city_streets']['locations']['KavinskiAvto']['role_id'] = 1004295878644867072
		self.locations['city_streets']['locations']['KavinskiAvto']['chat_id'] = 1004295881333420082
		self.locations['city_streets']['locations']['RadanHouse']['role_id'] = 1004295886207197214
		self.locations['city_streets']['locations']['RadanHouse']['chat_id'] = 1004295889193545848
		self.locations['city_streets']['locations']['KateHouse']['role_id'] = 1004295894113456209
		self.locations['city_streets']['locations']['KateHouse']['chat_id'] = 1004295897934471170
		self.locations['city_streets']['locations']['BomjSt']['role_id'] = 1004295904997687346
		self.locations['city_streets']['locations']['BomjSt']['chat_id'] = 1004295907757539378
		self.locations['city_streets']['locations']['MainPl']['role_id'] = 1004295912367071262
		self.locations['city_streets']['locations']['MainPl']['chat_id'] = 1004295914900426812
		self.locations['city_streets']['locations']['CRK']['role_id'] = 1004295922940907600
		self.locations['city_streets']['locations']['CRK']['chat_id'] = 1004295926044708914
		self.roles['AV']['id'] = 1004066885131829329
		self.roles['CH']['id'] = 1004066888361451681
		self.roles['PL']['id'] = 1004066891217776763
		self.roles['ST']['id'] = 1004066893822439525
		self.roles['SC']['id'] = 1004066896154472588
		self.roles['MC']['id'] = 1004066898213883987
		self.roles['BM']['id'] = 1004066910645796975
		self.roles['CL']['id'] = 1004066912814252062
		self.locations['city_streets']['id'] = 1004066916081618964
		self.locations['undercity_locations']['id'] = 1004066942107267153
		self.locations['works']['id'] = 1004066944460259439
		self.roles['AV']['role_id'] = 1004066955310923857
		self.roles['AV']['work_id'] = 1004066957915590792
		self.roles['AV']['chatt_id'] = 1004066959320698880
		self.roles['AV']['chatv_id'] = 1004066960843227186
		self.roles['CH']['role_id'] = 1004066969433165934
		self.roles['CH']['work_id'] = 1004066973396766881
		self.roles['CH']['chatt_id'] = 1004066976349569104
		self.roles['CH']['chatv_id'] = 1004066977830142072
		self.roles['PL']['role_id'] = 1004066986709487758
		self.roles['PL']['work_id'] = 1004066988693401601
		self.roles['PL']['chatt_id'] = 1004066990278856714
		self.roles['PL']['chatv_id'] = 1004066991637790831
		self.roles['ST']['role_id'] = 1004067000357752872
		self.roles['ST']['work_id'] = 1004067002501038100
		self.roles['ST']['chatt_id'] = 1004067003461550112
		self.roles['ST']['chatv_id'] = 1004067004992454656
		self.roles['SC']['role_id'] = 1004067015390150791
		self.roles['SC']['work_id'] = 1004067018791735366
		self.roles['SC']['chatt_id'] = 1004067020255531038
		self.roles['SC']['chatv_id'] = 1004067021509640242
		self.roles['MC']['role_id'] = 1004067029294268559
		self.roles['MC']['work_id'] = 1004067031655653490
		self.roles['MC']['chatt_id'] = 1004067032976859157
		self.roles['MC']['chatv_id'] = 1004067034365165579
		self.roles['BM']['role_id'] = 1004067043093520404
		self.roles['BM']['work_id'] = 1004067045337473125
		self.roles['BM']['chatt_id'] = 1004067046444761229
		self.roles['BM']['chatv_id'] = 1004067047610785823
		self.roles['CL']['role_id'] = 1004067056456581290
		self.roles['CL']['work_id'] = 1004067058935418941
		self.roles['CL']['chatt_id'] = 1004067060441165854
		self.roles['CL']['chatv_id'] = 1004067061741408386
		self.roles['BH']['role_id'] = 1004067070411026494
		self.roles['BH']['work_id'] = 1004067073623851060
		self.roles['BH']['chatt_id'] = 1004067075230289960
		self.roles['BH']['chatv_id'] = 1004067076316598292


logger.info('Создаю объект класса')
data=Data()
logger.info('Класс создан')










logger.debug(sys.argv)
token = sys.argv[1]