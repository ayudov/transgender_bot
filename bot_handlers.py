from bot import bot # Импортируем объект бота
from messages import * # Инмпортируем всё с файла сообщений
from buttons import *
from db import users_db
from telebot import types
from datetime import datetime, timezone
import pymongo


@bot.message_handler(commands=['start'])
# Выполняется, когда пользователь нажимает на start
def send_welcome(message):
	if not users_db.find_one({'user_id': message.from_user.id}):
		users_db.insert_one({'user_id' : message.from_user.id, 'Name' : '', 'Sex' : '', 'editing' : ''})		#Создаем новую запись
		bot.send_message(message.chat.id, HELLO_MESSAGE)
	else:
		bot.send_message(message.chat.id, HELLO_AGAIN_MESSAGE)


@bot.message_handler(content_types=["text"]) # Любой текст
def repeat_all_messages(message):
	if users_db.find_one({'user_id' : message.from_user.id, 'Name' : ''}):
		users_db.update_one({'user_id' : message.from_user.id}, {"$set" : {'Name' : message.text}}) #Обновляем имя
		bot.send_message(message.chat.id, NAME_UPDATED)
		bot.send_message(message.chat.id, "Пожалуйста, " + users_db.find_one({'user_id' : message.from_user.id})['Name'] + ", выбери пол:", reply_markup=keyboard_choose_sex)
	elif users_db.find_one({'user_id' : message.from_user.id, 'Sex' : ''}) or users_db.find_one({'user_id' : message.from_user.id, 'Sex' : 'Другое'}):
		users_db.update_one({'user_id' : message.from_user.id}, {"$set" : {'Sex' : message.text}})  	#Обновляем пол
		if users_db.find_one({'user_id' : message.from_user.id, 'Sex' : 'Другое'}):
			bot.send_message(message.chat.id, SEX_ENTER)
		else:
			bot.send_message(message.chat.id, 'Твой пол "' +  users_db.find_one({'user_id' : message.from_user.id})['Sex'] + '"')
			if not users_db.find_one({'user_id' : message.from_user.id, 'Name' : '', 'Sex' : ''}) or users_db.find_one({'user_id' : message.from_user.id, 'Name' : '', 'Sex' : 'Другое'}):
				bot.send_message(message.chat.id, SUCCESSFULLY_REGISTERED, reply_markup=keyboard_continue_conversation)	
	
		
	
	elif message.text == 'Поздороваться':
		if users_db.find_one({'user_id' : message.from_user.id, 'Sex' : 'Ж'}):friend_recourse = 'моя подруга,'
		elif users_db.find_one({'user_id' : message.from_user.id, 'Sex' : 'М'}):friend_recourse = 'мой друг,'
		else: friend_recourse = 'мой нестандартный друг,'
		if datetime.now().hour >= 0 and datetime.now().hour < 6:
			bot.send_message(message.chat.id, 'Доброй ночи, ' + friend_recourse + " " + users_db.find_one({'user_id' : message.from_user.id})['Name'], reply_markup=keyboard_continue_conversation)
		elif datetime.now().hour >= 6 and datetime.now().hour < 12:
			bot.send_message(message.chat.id, 'Доброе утро, ' + friend_recourse + " " + users_db.find_one({'user_id' : message.from_user.id})['Name'], reply_markup=keyboard_continue_conversation)
		elif datetime.now().hour >= 12 and datetime.now().hour < 18:
			bot.send_message(message.chat.id, 'Добрый день, ' + friend_recourse + " " + users_db.find_one({'user_id' : message.from_user.id})['Name'], reply_markup=keyboard_continue_conversation)
		elif datetime.now().hour >= 16 and datetime.now().hour < 24:
			bot.send_message(message.chat.id, 'Доброй ночи, ' + friend_recourse + " " + users_db.find_one({'user_id' : message.from_user.id})['Name'], reply_markup=keyboard_continue_conversation)	
	elif message.text == 'Удоли':
		users_db.delete_one({'user_id' : message.from_user.id})
		bot.send_message(message.chat.id, "Пока, жюк:(", reply_markup = keyboard_start_conversation)
	elif message.text == 'Сменить пол':
		bot.send_message(message.chat.id, "Пожалуйста, " + users_db.find_one({'user_id' : message.from_user.id})['Name'] + ", выбери пол:", reply_markup=keyboard_choose_sex)
		users_db.update_one({'user_id' : message.from_user.id}, {"$set" : {'Sex' : 'Другое'}}) 
	else:
		bot.send_message(message.chat.id, KEYBOARD_USAGE_ASKING)


		
		


if __name__ == '__main__':
    bot.polling(none_stop=True)