import telebot
import cfg

bot = telebot.TeleBot(cfg.config['token'])

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Добавить дело')
keyboard1.row('Удалить дело')
keyboard1.row('Скачать txt','Список дел')	
keyboard1.row('Очистка','Помощь')


@bot.message_handler(commands = ['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Привет! Я помогу тебе с делами)', reply_markup = keyboard1)

@bot.message_handler(commands = ['help'])
def help_message(message):
	bot.send_message(message.chat.id, 'Бот может сохранять и удалять ваши дела\nСписок команд:\n/a *текст* - добавить дело\n/d - *текст* - удалить дело\n/c - очистить\n/sh - вывести список\n/file - скачать список txt')

#Добавить дело
@bot.message_handler(commands = ['a'])
def rec_message(message):
	str1 = message.text
	str1 = str1[:0] + str1[3:]
	filePath = str(message.from_user.id) + ".txt"
	#summ = sum(1 for line in open(filePath,'r'))
	#print(summ)
	#summ = summ + 1
	file = open(filePath, 'a')
	file.write('- ' + str1 + '\n')
	file.close

#Удалить дело
@bot.message_handler(commands = ['d'])
def del_message(message):
	str1 = message.text
	str1 = str1[:0] + str1[3:]
	filePath = str(message.from_user.id) + ".txt"
	file = open(filePath, 'r')
	lines = file.readlines()
	file.close()
	file = open(filePath, 'w')
	for line in lines:
		if line != str1 + "\n":
			file.write(line)
	file.close()

#Удалить все дела
@bot.message_handler(commands = ['c'])
def cl_message(message):
	filePath = str(message.from_user.id) + ".txt"
	open(filePath,'w').close()
	bot.send_message(message.chat.id, 'Готово!\nДел больше нет')

#Просмотр списка дел
@bot.message_handler(commands = ['sh'])
def show_message(message):
	filePath = str(message.from_user.id) + ".txt"
	file = open(filePath, 'r')
	#bot.send_message(message.chat.id, 'Ваши дела: ')
	if(file.read()):
		file.seek(0)
		bot.send_message(message.chat.id, 'Ваши дела: ')
		bot.send_message(message.chat.id, file.read())
	else:
		bot.send_message(message.chat.id, 'У вас нет дел')
	#bot.send_message(message.chat.id, file.read())
	file.seek(0)
	file.close

#Скачать список дел
@bot.message_handler(commands = ['file'])
def file_message(message):
	filePath = str(message.from_user.id) + ".txt"
	file = open(filePath, 'rb')
	#bot.send_document(message.chat.id, file)
	if(file.read()):
		file.seek(0)
		bot.send_document(message.chat.id, file)
	else:
		bot.send_message(message.chat.id, 'У вас нет списка дел')
	file.close()



@bot.message_handler(content_types = ['text'])
def get_text(message):
   if message.text.lower() == 'привет':
	   bot.send_message(message.chat.id, 'Привет!')
   elif message.text == 'Добавить дело':
       bot.send_message(message.chat.id, 'Чтобы добавить дело, используй /a\nПример: /a ляляля')
   elif message.text == 'Удалить дело':
       bot.send_message(message.chat.id, 'Чтобы удалить дело, используйте /d \nПример: /d - ляляля')
   elif message.text == 'Скачать txt':
       file_message(message)
   elif message.text == 'Список дел':
       show_message(message)
   elif message.text == 'Очистка':
       cl_message(message)  
   elif message.text == 'Помощь':
       help_message(message)
   else:
	   bot.send_message(message.chat.id, 'Я тебя не понимаю, используй /help')


bot.polling(none_stop = True, interval = 0)