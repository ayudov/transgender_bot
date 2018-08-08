from datetime import datetime, timezone
import re

import pymongo
from telebot import types

from bot import bot
from messages import * 													     
from buttons import *
from db import users_db


@bot.message_handler(commands=['start'])
def send_welcome(message):
	if users_db.count_documents({'user_id': message.from_user.id}) != 1:
		if users_db.count_documents({'user_id': message.from_user.id}) == 0:
			users_db.insert_one({'user_id': message.from_user.id,
								'Name': '',
								'Sex': '',
								'menu item': '',
								'reg time by UTC': datetime.utcnow()})	
			bot.send_message(message.chat.id, HELLO_MESSAGE)
		while users_db.count_documents({'user_id': message.from_user.id}) > 1:
			users_db.delete_one({'user_id': message.from_user.id})
	else: bot.send_message(message.chat.id, HELLO_AGAIN_MESSAGE)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
# Смена имени
	if users_db.find_one({'user_id': message.from_user.id, 'Name': ''}):					
		users_db.update_one({'user_id': message.from_user.id},														
							{"$set": {'Name': message.text}})																				
		if users_db.find_one({'user_id': message.from_user.id,
							'Sex': ''}):
			bot.send_message(message.chat.id, 
							NAME_UPDATED + "\n" + CHOOSE_SEX_ASKING.format(users_db.find_one({'user_id': message.from_user.id})['Name']),
							reply_markup=keyboard_choose_sex)
		else:
			bot.send_message(message.chat.id,
							NAME_UPDATED,
							reply_markup=keyboard_continue_conversation)
			users_db.update_one({'user_id': message.from_user.id},
								{"$set": {'menu item': CONTINUE_CONVERSATION}})
# Смена пола
	elif users_db.find_one({'user_id': message.from_user.id, 'Sex': ''}):																	
		if any([message.text == MALE_B, message.text == FEMALE_B, message.text == OTHER_B]):
			users_db.update_one({'user_id': message.from_user.id},
								{"$set": {'Sex': message.text,'menu item': CONTINUE_CONVERSATION}})  	
			bot.send_message(message.chat.id,
							SEX_UPDATED + '\n' + YOUR_SEX.format(users_db.find_one({'user_id': message.from_user.id})['Sex']),
							reply_markup=keyboard_continue_conversation)
		elif re.search('[a-zA-Z\d]', message.text): bot.send_message(message.chat.id, CHAR_ASKING)
		else: bot.send_message(message.chat.id, KEYBOARD_USAGE_ASKING)
# Ответ на "поздороваться"
	elif message.text == 'Поздороваться' and users_db.find_one({'user_id': message.from_user.id, 'menu item': CONTINUE_CONVERSATION}):	
		if users_db.find_one({'user_id': message.from_user.id, 'Sex': 'Ж'}):friend_recourse = MY_FRIEND_F
		elif users_db.find_one({'user_id': message.from_user.id, 'Sex': 'М'}):friend_recourse = MY_FRIEND_M
		elif users_db.find_one({'user_id': message.from_user.id, 'Sex': 'Другой'}):friend_recourse = MY_FRIEND_NA
		if datetime.now().hour >= 0 and datetime.now().hour < 6: time_recourse = GOOD_NIGHT
		elif datetime.now().hour >= 6 and datetime.now().hour < 12: time_recourse = GOOD_MORNING
		elif datetime.now().hour >= 12 and datetime.now().hour < 18: time_recourse = GOOD_DAY
		elif datetime.now().hour >= 16 and datetime.now().hour < 24: time_recourse = GOOD_EVENING
		bot.send_message(message.chat.id,
						time_recourse + friend_recourse + users_db.find_one({'user_id': message.from_user.id})['Name'],
						reply_markup=keyboard_continue_conversation)
# Настройки
	elif message.text == 'Настройки' and users_db.find_one({'user_id': message.from_user.id, 'menu item': CONTINUE_CONVERSATION}):
		bot.send_message(message.chat.id, CHOOSE_OPTION_ASKING, reply_markup=keyboard_choose_option)
		users_db.update_one({'user_id': message.from_user.id},
							{"$set": {'menu item': CHOOSE_OPTION}})
# Запрос на смену пола
	elif message.text == 'Сменить пол' and users_db.find_one({'user_id': message.from_user.id, 'menu item': CHOOSE_OPTION}):	
		bot.send_message(message.chat.id, 
						CHOOSE_SEX_ASKING.format(users_db.find_one({'user_id': message.from_user.id})['Name']),
						reply_markup=keyboard_choose_sex)
		users_db.update_one({'user_id': message.from_user.id},
							{"$set": {'Sex': '', 'menu item': ''}}) 
# Запрос на смену имени
	elif message.text == 'Сменить имя' and users_db.find_one({'user_id': message.from_user.id, 'menu item': CHOOSE_OPTION}):
		bot.send_message(message.chat.id,
						CHOOSE_NAME_ASKING.format(users_db.find_one({'user_id': message.from_user.id})['Name']))	
		users_db.update_one({'user_id': message.from_user.id},
							{"$set": {'Name': '', 'menu item': ''}}) 
# Неверный ввод
	else: bot.send_message(message.chat.id, KEYBOARD_USAGE_ASKING)																			

		
if __name__ == '__main__':
    bot.polling(none_stop=True)