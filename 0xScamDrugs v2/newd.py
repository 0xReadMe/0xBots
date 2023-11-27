import telebot
import string
import random
import datetime
import requests
import json
from decimal import Decimal
import sqlite3
bot = telebot.TeleBot("921618047:AAEinIm6nSmkHkd2nwFdtB6XA7KU4oIfik4")
print("bot initialized!")

admin = 531995934 #ID администратора бота, можно получить через бота @userinfobot
qiwi = 79997777777

secret_key = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6Im8xcTZvei0wMCIsInVzZXJfaWQiOiI3OTYxNDY1NzAxOSIsInNlY3JldCI6ImJkYjBmODdhNTI5OTllM2Q0YWVkZmVmNjE4NmM4ZWNjOWU0MmY5ZGQzYjJkYzIwNzgwNGY1NjdiNmYyYWVhNWUifX0="
qiwi_token = "133c92d95ff351cc8aa2c3585db9a102"


#Текст меню
startText = """
	*Добро пожаловать в DemoSnusBot!*
	Здесь ты можешь купить снюс твоих любимых марок по самой выгодной цене!
	Для того, чтобы открыть каталог, нажми кнопку КАТАЛОГ!
	"""

startGorodText = """
	*Добро пожаловать в DemoSnusBot!*
	Пожалуйста, выбери свой город.
	"""

#Текст FAQ
faqText = """
Тут текст FAQ
"""

#Текст помощи
helpText = """
Выберите, что вам нужно сделать
"""

usersteps = {}
useradmin = {}
userchosen = {}
usercity = {}


def getValuesFromDB(cmd, arg):
	db = sqlite3.connect("bot.db")
	c = db.cursor()
	c.execute(cmd, arg)
	result = c.fetchall()
	c.close()
	return result

def setValuesToDB(cmd, arg):
	db = sqlite3.connect("bot.db")
	c = db.cursor()
	c.execute(cmd, arg)
	db.commit()
	c.close()
	return True

# Старый usersready на текстовом файле
# def usersready():
# 	userstxt = open("users.txt", "r")
# 	d = userstxt.read().split('\n')
# 	userstxt.close()
# 	return d


# Новый usersready на sqlite3
def isuserready(userid):
	isready = getValuesFromDB('SELECT * FROM users WHERE id = ?', (userid,))
	return isready

def userswrite(userid, country):
	return setValuesToDB('INSERT INTO users VALUES (?, ?)', (userid, country))

def usersremove(userid):
	return setValuesToDB('DELETE FROM users WHERE id = ?', (userid,))

# def userswrite(userid):
# 	users = usersready()
# 	userstxt = open("users.txt", "w")
# 	users.append(str(userid))
# 	text = "\n".join(users)
# 	userstxt.write(text)
# 	userstxt.close()
# 	return True

# def usersremove(userid):
# 	users = usersready()
# 	userstxt = open("users.txt", "w")
# 	users.remove(str(userid))
# 	if userid in usercity:
# 		usercity.pop(userid)
# 	text = "\n".join(users)
# 	userstxt.write(text)
# 	userstxt.close()
# 	return True

cities = {"Москва": ["Измайлово",
					 "Сокольники",
					 "Внуково",
					 "Кунцево",
					 "Крюково",
					 "Щукино",
					 "Лефортово",
					 "Выхино-Жулебина",
					 "Медведково",
					 "Якиманка",
					 "Отрадное"],

		  "Санкт-Петербург": ["Центральный район",
		  					  "Невский район",
		  					  "Кировский район",
		  					  "Петроградский район",
		  					  "Московский район",
		  					  "Василеостровской район",
		  					  "Главная"],

		  "Ростов-На-Дону": ["Ворошиловский",
		  					 "Железнодорожный",
		  					 "Кировский",
		  					 "Ленинский",
		  					 "Октябрьский",
		  					 "Первомайский",
		  					 "Пролетарский",
		  					 "Советский"],

		 "Екатеринбург": ["Верх-Исетский",
		 				  "Железнодорожный",
		 				  "Кировский",
		 				  "Ленинский",
		 				  "Октябрьский",
		 				  "Орджоникидзевский",
		 				  "Чкаловский"],

		 "Челябинск": ["Калининский",
		 			   "Курчатовский",
		 			   "Ленинский",
		 			   "Металлургический",
		 			   "Советский",
		 			   "Тракторозаводский",
		 			   "Центральный"],

		 "Новосибирск": ["Дзержинский",
		 				 "Заельцовский",
		 				 "Калининский",
		 				 "Кировский",
		 				 "Ленинский",
		 				 "Октябрьский",
		 				 "Советский"],

		 "Нижний Новгород": ["Автозаводский",
		 					 "Канавинский",
		 					 "Ленинский",
		 					 "Московский",
		 					 "Нижегородский",
		 					 "Приокский",
		 					 "Советский",
		 					 "Сормовский"],

		 "Казань": ["Авиастроительный",
		 			"Кировский",
		 			"Московский",
		 			"Ново-Савиновский",
		 			"Приволжский",
		 			"Советский"],

		 "Омск": ["Кировский",
		 		  "Ленинский",
		 		  "Октябрьский",
		 		  "Советский",
		 		  "Центральный"],

		 "Самара": ["Октябрьский",
		 			"Советский",
		 			"Промышленный",
		 			"Кировский"],

		 "Краснодар": ["Западный",
		 			   "Карасунский",
		 			   "Прикубанский",
		 			   "Центральный"],

		 "Саратов": ["Заводской",
		 			 "Октябрьский",
		 			 "Ленинский",
		 			 "Кировский"],

		 "Тюмень": ["Восточный",
		 			"Калининский",
		 			"Ленинский",
		 			"Центральный"],

		 "Барнаул": ["Железнодорожный",
		 			 "Индустриальный",
		 			 "Ленинский",
		 			 "Октябрьский",
		 			 "Центральный"],

		 "Иркутск": ["Кировский",
		 			 "Куйбышевский",
		 			 "Ленинский",
		 			 "Октябрьский",
		 			 "Свердловский"],

		 "Ярославль": ["Дзержинский",
		 			   "Заволжский",
		 			   "Фрунзенский"],

		 "Владивосток": ["Ленинский",
		 				 "Первомайский",
		 				 "Первореченский"],

		 "Оренбург": ["Дзержинский",
		 			  "Промышленный",
		 			  "Ленинский"],

		 "Томск": ["Кировский",
		 		   "Ленинский",
		 		   "Октябрьский",
		 		   "Советский"],

		 "Воронеж": ["Железнодорожный",
		 			 "Коминтерновский",
		 			 "Левобережный",
		 			 "Ленинский",
		 			 "Советский",
		 			 "Центральный"],

		 "Пермь": ["Дзержинский",
		 		   "Индустриальный",
		 		   "Кировский",
		 		   "Мотовилихинский",
		 		   "Орджоникидзевский",
		 		   "Свердловский"],

		 "Волгоград": ["Тракторозаводский",
		 			   "Краснооктябрьский",
		 			   "Дзержинский",
		 			   "Советский",
		 			   "Кировский",
		 			   "Красноармейский"],

		 "Уфа": ["Калининский",
		 		 "Кировский",
		 		 "Октябрьский",
		 		 "Орджоникидзевский",
		 		 "Советский"],

		 "Красноярск": ["Железнодорожный",
		 				"Кировский",
		 				"Ленинский",
		 				"Октябрьский",
		 				"Свердловский",
		 				"Советский"]
		}


goods = {"Kurwa": {"90MG Blackcurrant": 150, 
				   "90MG Blueberry": 150,
				   "90MG Bubblegum": 150,
				   "90MG Kiwi": 150,
				   "90MG Mango": 150,
				   "90MG Pineapple": 150,
				   "90MG Purple Grape": 150,
				   "90MG Вишня": 150,
				   "90MG Чифирь": 150,
				   "90MG Extremely Strong": 150,
				   "90MG Tic Tac": 150,
				   "90MG Ванильная кола": 150,
				   "90MG Морс": 150},

		 "Mad": {"Blackberry": 150,
		 		 "Cherry": 150,
		 		 "Fatality 100MG": 180,
		 		 "Mint": 150},

		 "Corvus": {"Flash Orange": 120,
		 			"Hulk Feijoa": 120,
		 			"Joker Wild Berries": 120,
		 			"Logan Melon": 120,
		 			"Brutal Menthol": 120,
		 			"Extreme Menthol": 120,
		 			"Strong Menthol": 120},

		 "Boshki": {"Hardcore 100MG Forest Berry": 180,
		 			"Super Strong Fresh Aloe": 180,
		 			"Super Strong Gummy Bear": 180,
		 			"Super Strong Menthol": 180},

		 "Nictech": {"Extremely Strong": 180,
		 			 "Kasta Red": 140,
		 			 "Slim Barberry": 150,
		 			 "Slim Citrus Mix": 150,
		 			 "Slim Energy": 150,
		 			 "Slim Tropic Mix": 150,
		 			 "Strong": 140},
		 "Arqa": {"65MG Cold Bergamot Candy": 150,
		 		  "65MG Cold Berry Lemonade": 150,
		 		  "65MG Cold Caramel Ice Cream": 150,
		 		  "65MG Cold Chokeberry Cocktail": 150,
		 		  "65MG Cold Extreme Cola": 150,
		 		  "65MG Cold Winter Tale": 150,
		 		  "Black Cold Barberry": 120,
		 		  "Black Cold Cherry": 120,
		 		  "Black Cold Citrus Mix": 120,
		 		  "Black Cold Green Apple": 120,
		 		  "Black Cold Mint": 120},

		 "Lyft": {"Berry Frost Mellow Slim": 130,
		 		  "Blueberry Slim": 130,
		 		  "Freeze X-Strong Slim": 130,
		 		  "Ice Cool Strong Slim": 130,
		 		  "Lime Slim": 130,
		 		  "Lime Strong Slim": 130,
		 		  "Limited Edition Strawberry Bloom Slim": 150,
		 		  "Liquorice Strong Slim": 130,
		 		  "Melon Slim": 130,
		 		  "Mint Easy Slim": 130,
		 		  "Mint Slim": 130,
		 		  "Polar Mint Medium Slim": 130,
		 		  "Tropic Breeze Slim": 130,
		 		  "Winterchill X-Strong Slim": 130},

		 "Vote": {"20MG Cherry": 150,
		 		  "20MG Cola": 150,
		 		  "20MG Green Apple": 150,
		 		  "20MG Strawberry": 150,
		 		  "40MG Cherry": 150,
		 		  "40MG Cola": 150,
		 		  "40MG Green Apple": 150,
		 		  "40MG Strawberry": 150,
		 		  "60MG Cherry": 150,
		 		  "60MG Cola": 150,
		 		  "60MG Green Apple": 150,
		 		  "60MG Strawberry": 150},

		 "Taboo": {"80 Mint": 130,
		 		   "Extreme Cold Energy": 130,
		 		   "Extreme Grape": 130,
		 		   "Extreme Kiwi & Strawberry": 130,
		 		   "Strong Mint": 130},

		 "Fedrs Ice Cool": {"Mint": 150,
		 					"Energy": 150,
		 					"Pear": 150,
		 					"Spearmint": 150,
		 					"Barberry": 150,
		 					"Melon": 150,
		 					"Cola Vanilla": 150,
		 					"Mint Skull & Energy Skull": 150},

		 "Скиф": {"Fruits Арбуз Яблоко": 150,
		 		  "Fruits Мята Яблоко": 150,
		 		  "Strong Mint Белый": 150,
		 		  "Super Extreme Mint Коричневый": 150,
		 		  "Super Extreme Mint Красный": 150,
		 		  "Ultra Strong Mint Синий": 130},

		 "Alfa": {"Cold Клубника": 130,
		 		  "Cold Кокос": 130,
		 		  "Cold Мята": 130,
		 		  "Cold Черешня": 130,
		 		  "Cold Черника": 130,
		 		  "Cold Яблоко": 130,
		 		  "Cold Лайм": 130},

		 "Blax": {"Black Edition Cold Dry Extreme Hard Lemon & Lime": 130,
		 		  "Black Edition Cold Dry Extreme Hard Strawberry & Raspberry": 130,
		 		  "Black Edition Cold Dry Ultra Strong": 130,
		 		  "Slim & White Cola Cherry": 150,
		 		  "Slim & White Grapefruit": 150,
		 		  "Slim & White Milkshake": 150,
		 		  "150 Barberry": 180,
		 		  "150 Bubble Gum": 180,
		 		  "150 Energy": 180,
		 		  "150 Strawberry Raspberry": 180,
		 		  "Black Edition Cold Dry Extreme Hard": 130,
		 		  "Black Edition Cold Dry Extreme Hard Cherry & Cola": 130},

		 "Самоубийца 249 МГ": {"Energy Burn": 200,
		 					   "Мята": 200,
		 					   "Малина": 200,
		 					   "Яблоко": 200},

		 "Cuba": {"Silver": 120,
		 		  "Gold": 120,
		 		  "Power": 140,
		 		  "Watermelon": 140,
		 		  "Ананас": 140,
		 		  "Вишневый сок": 140,
		 		  "Земляника": 140,
		 		  "Йогурт": 140}
		 }

### КЛАВИАТУРЫ

goodsKb = telebot.types.ReplyKeyboardMarkup(True)
goodsKb.row("Вернуться в меню")
for good in goods:
	goodsKb.row(good)

startKb = telebot.types.ReplyKeyboardMarkup(True)
rows = ["Каталог", "FAQ", "Помощь"]
for row in rows:
	startKb.row(row)

paymentKb = telebot.types.ReplyKeyboardMarkup(True)
paymentKb.row("Qiwi")
paymentKb.row("Карта")

payKb = telebot.types.ReplyKeyboardMarkup(True)
payKb.row("Вернуться в меню")
payKb.row("Оплатил")

helpKb = telebot.types.ReplyKeyboardMarkup(True)
helpKb.row("Сменить город")
helpKb.row("Вызвать администратора")
helpKb.row("Вернуться в меню")

def getGoodList(goodStr):
	d = goodStr.split(' | ')
	if d[0] in goods and d[1] in goods[d[0]]:
		price = goods[d[0]][d[1]]
		good = [d[0], d[1], price]
		return good
	else:
		return False


def generateCatalog(name):
	kb = telebot.types.ReplyKeyboardMarkup(True)
	kb.row("Вернуться в каталог")
	for good in goods[name]:
		kb.row(name + " | " + good + " | Цена: " + str(goods[name][good]))
	return kb


def generateCities():
	kb = telebot.types.ReplyKeyboardMarkup(True)
	for city in cities:
		kb.row(city)
	return kb


def generateAreas(name):
	kb = telebot.types.ReplyKeyboardMarkup(True)
	for area in cities[name]:
		kb.row(area)
	return kb

### ФУНКЦИИ ДЛЯ БОТА

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def makeInvoice(amount):
	billId = random.randrange(1, 10000000000000000)
	dateNow = datetime.datetime.now() + datetime.timedelta(hours=3)
	expirationDateTime = dateNow.strftime('%Y-%m-%dT%H:%M:%S+03:00')
	amount = str(round(Decimal(float(amount)), 2)) #прости меня, господи
	data = {"amount": {"currency": "RUB", "value": amount}, "comment": "Оплата товара", "expirationDateTime": expirationDateTime}
	headers = {"Authorization": "Bearer " + secret_key, "Accept": "application/json", "Content-Type": "application/json"}
	req = requests.put("https://api.qiwi.com/partner/bill/v1/bills/{0}".format(str(billId)), data=json.dumps(data), headers = headers)
	req = req.json()
	if "errorCode" in req:
		print("Error in making invoice!" + req["description"])
		raise
		return False
	else:
		return req["payUrl"]


def getHistory():
	url = "https://edge.qiwi.com/payment-history/v2/persons/{0}/payments".format(str(qiwi))
	headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer " + qiwi_token}
	req = requests.get(url, params={"rows": 1, "operation": "IN"}, headers = headers)
	if req.status_code == 200:
		req = req.json()
		return req
	return req
	# raise ValueError

previousTransactions = [getHistory()]

print("everything loaded!")

### ОБРАБОТКА СООБЩЕНИЙ

@bot.message_handler(commands=['start'])
def start(message):
	if not isuserready(message.from_user.id):
		bot.send_message(message.chat.id, startGorodText, parse_mode="markdown", reply_markup = generateCities())
		print("sent cities to {0}".format(str(message.from_user.id)))
		return
	bot.send_message(message.chat.id, startText, parse_mode="markdown", reply_markup = startKb)
	print("got start msg from id {0}".format(str(message.from_user.id)))


@bot.message_handler(content_types=['text'])
def send_text(message):
	print("got msg from id {0} : {1}".format(str(message.from_user.id), message.text))
	if message.text in cities and message.from_user.id not in usercity:
		bot.send_message(message.chat.id, "Выбери свой район", reply_markup = generateAreas(message.text))
		usercity[message.from_user.id] = message.text


	elif message.from_user.id in usercity and message.text in cities[usercity[message.from_user.id]]:
		userswrite(message.from_user.id, usercity[message.from_user.id])
		start(message)


	elif message.text.lower() in ["меню", "вернуться в меню"]:
		start(message)


	elif message.text.lower() in ["каталог", "вернуться в каталог"]:
		bot.send_message(message.chat.id, "*Список марок:* (список можно пролистывать)", reply_markup = goodsKb, parse_mode="markdown")
	

	elif message.text in goods:
		bot.send_message(message.chat.id, "*Каталог марки {0}:* (список можно проматывать)".format(message.text), reply_markup = generateCatalog(message.text), parse_mode = "markdown")
		print("sent catalog {0}".format(message.text))
	

	elif message.from_user.id in usersteps and usersteps[message.from_user.id] == "Qiwi":
		text = """
		Вы выбрали товар *{0}*
		Стоимость товара: *{1}*
		Счет для оплаты товара: *{2}*

		При переводе на Qiwi *обязательно* укажите следующий комментарий: `{3}` (с телефона этот комментарий можно скопировать долгим тапом по нему)
		Если при переводе вы не укажете данный комментарий, то *оплата не засчитается!*

		Когда вы завершите оплату, нажмите кнопку *ОПЛАТИЛ!* 
		"""
		choose = userchosen[message.from_user.id]
		price = goods[choose[0]][choose[1]]
		wallet = qiwi
		readyText = text.format(choose[0] + " " + choose[1], price, wallet, randomString())
		bot.send_message(message.chat.id, readyText, parse_mode = "markdown", reply_markup = payKb)
		del(usersteps[message.from_user.id])
		print("sent pay window to user {0}".format(str(message.from_user.id)))
	

	elif message.from_user.id in usersteps and usersteps[message.from_user.id] == "Карта":
		text = """
		Вы выбрали товар <b>{0}</b>
		Стоимость товара: <b>{1}</b>
		Ссылка для оплаты товара: {2}

		Для оплаты вам нужно перейти по ссылке и оплатить товар.

		Когда вы завершите оплату, нажмите кнопку <b>ОПЛАТИЛ!</b>
		"""
		choose = userchosen[message.from_user.id]
		price = goods[choose[0]][choose[1]]
		link = makeInvoice(int(price))
		#link = "test"
		del(usersteps[message.from_user.id])
		readyText = text.format(choose[0] + " " + choose[1], price, link)
		bot.send_message(message.chat.id, readyText, parse_mode = "HTML", reply_markup = payKb)
		print("sent invoice window to user {0}".format(str(message.from_user.id)))
	

	elif message.text in ["Qiwi", "Карта"] and message.from_user.id in userchosen:
		usersteps[message.from_user.id] = message.text
		bot.send_message(message.chat.id, "Пожалуйста, введите свой адрес для доставки, в формате: Улица, номер дома, квартира:", reply_markup = telebot.types.ReplyKeyboardRemove())
	

	elif message.text.lower() == "оплатил":
		bot.send_message(message.chat.id, "Оплата не найдена! Попробуйте еще раз.")
		trans = [getHistory()]
		if trans != previousTransactions:
			bot.send_message(admin, "!!! Пополнение киви! Получена оплата от {0}".format(str(message.from_user.id)))
		print("GOT PAY CONFIRM!! user: {0}".format(str(message.from_user.id)))
	
	
	elif len(message.text.split(' | ')) == 3:
		d = getGoodList(message.text)
		if d:
			userchosen[message.from_user.id] = [d[0], d[1]]
			bot.send_message(message.chat.id, "Выберите удобный способ оплаты", reply_markup = paymentKb)
			print("sent good to user {0} for price of {1}".format(str(message.from_user.id), str(d[2])))
	
	
	elif message.text.lower() == "faq":
		bot.send_message(message.chat.id, faqText, parse_mode="markdown")
		print("sent faq to {0}".format(str(message.from_user.id)))
	

	
	elif message.text.lower() == "помощь":
		bot.send_message(message.chat.id, helpText, reply_markup = helpKb, parse_mode="markdown")
		print("sent help to {0}".format(str(message.from_user.id)))
	

	elif message.text.lower() == "сменить город" and isuserready(message.from_user.id):
		usersremove(message.from_user.id)
		start(message)
		print("sent change city to {0}".format(str(message.from_user.id)))
	

	elif message.from_user.id in useradmin:
		useradmin.pop(message.from_user.id)
		bot.forward_message(admin, message.chat.id, message.message_id)
		bot.send_message(message.chat.id, "Администратор получил ваше сообщение и ответит вам в ближайшее время!", reply_markup = startKb)
	

	elif message.text.lower() == "вызвать администратора":
		useradmin[message.from_user.id] = 1
		bot.send_message(message.chat.id, "Пожалуйста, напишите вашу проблему в чат.", reply_markup = telebot.types.ReplyKeyboardRemove())

try:
	bot.polling()
except Exception as exc:
	bot.send_message(admin, "ВНИМАНИЕ!!! Бот упал, произошла ошибка! Тип ошибки: {0} Текст ошибки: {1}".format(str(type(exc)), str(exc)))