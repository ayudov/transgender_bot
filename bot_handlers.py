from datetime import datetime
# import re

from browse import *

from bot import bot
from buttons import *
from db import users_db


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not users_db.find_one({USER_ID: message.from_user.id}):
        users_db.insert_one({USER_ID: message.from_user.id,
                             NAME: '',
                             SEX: '',
                             STATE: ENTER_NAME,
                             REG_TIME: datetime.utcnow()})
        bot.send_message(message.chat.id, HELLO_MESSAGE)
    else:
        bot.send_message(message.chat.id, HELLO_AGAIN_MESSAGE)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    # Получаем информацию о пользователе
    user = users_db.find_one({USER_ID: message.from_user.id})

    # Ввод имени
    if user[STATE] == ENTER_NAME:
        if user[SEX] == '':
            users_db.update_one({USER_ID: message.from_user.id}, {"$set": {NAME: message.text, STATE: ENTER_SEX}})
            bot.send_message(message.chat.id, NAME_UPDATED + "\n" + CHOOSE_SEX_ASKING.format(
                users_db.find_one({USER_ID: user[USER_ID]})[NAME]), reply_markup=keyboard_choose_sex)
        else:
            if message.text == BACK_B:
                bot.send_message(message.chat.id, CHOOSE_OPTION_ASKING, reply_markup=keyboard_choose_option)
                users_db.update_one({USER_ID: user[USER_ID]}, {"$set": {STATE: CHOOSE_OPTION}})
            else:
                users_db.update_one({USER_ID: user[USER_ID]},
                                    {"$set": {NAME: message.text, STATE: CONTINUE_CONVERSATION}})
                bot.send_message(message.chat.id, NAME_UPDATED, reply_markup=keyboard_continue_conversation)

    # Ввод пола
    elif user[STATE] == ENTER_SEX:
        if any([message.text == MALE_B, message.text == FEMALE_B, message.text == OTHER_B]):
            users_db.update_one({USER_ID: user[USER_ID]}, {"$set": {SEX: message.text, STATE: CONTINUE_CONVERSATION}})
            bot.send_message(message.chat.id,
                             SEX_UPDATED + '\n' + YOUR_SEX.format(users_db.find_one({USER_ID: user[USER_ID]})[SEX]),
                             reply_markup=keyboard_continue_conversation)
        # elif re.search('[a-zA-Z\d]', message.text):
        #    bot.send_message(message.chat.id, CHAR_ASKING)
        else:
            bot.send_message(message.chat.id, KEYBOARD_USAGE_ASKING)

    # Продолжение диалога
    elif user[STATE] == CONTINUE_CONVERSATION:
        if message.text == SETTINGS_B:
            bot.send_message(message.chat.id, CHOOSE_OPTION_ASKING, reply_markup=keyboard_choose_option)
            users_db.update_one({USER_ID: user[USER_ID]}, {"$set": {STATE: CHOOSE_OPTION}})
        elif message.text == HELLO_B:
            my_friend_dict = {MALE_B: MY_FRIEND_M, FEMALE_B: MY_FRIEND_F, OTHER_B: MY_FRIEND_NA}
            if 0 <= datetime.now().hour < 6:
                time_recourse = GOOD_NIGHT
            elif 6 <= datetime.now().hour < 12:
                time_recourse = GOOD_MORNING
            elif 12 <= datetime.now().hour < 18:
                time_recourse = GOOD_DAY
            elif 16 <= datetime.now().hour < 24:
                time_recourse = GOOD_EVENING
            bot.send_message(message.chat.id, time_recourse + my_friend_dict[user[SEX]] + user[NAME],
                             reply_markup=keyboard_continue_conversation)
        elif message.text == CAT_B:
            #url=web()
            bot.send_photo(message.chat.id, photo=web())
        else:
            bot.send_message(message.chat.id, KEYBOARD_USAGE_ASKING)

    # Смена имени и пола
    elif user[STATE] == CHOOSE_OPTION:
        if message.text == CHANGE_SEX_B:
            bot.send_message(message.chat.id, CHOOSE_SEX_ASKING.format(user[NAME]), reply_markup=keyboard_choose_sex)
            users_db.update_one({USER_ID: user[USER_ID]}, {"$set": {SEX: '', STATE: ENTER_SEX}})
        elif message.text == CHANGE_NAME_B:
            bot.send_message(message.chat.id, CHOOSE_NAME_ASKING.format(user[NAME]), reply_markup=keyboard_back)
            users_db.update_one({USER_ID: user[USER_ID]}, {"$set": {STATE: ENTER_NAME}})
        else:
            bot.send_message(message.chat.id, KEYBOARD_USAGE_ASKING)

    # Неверный ввод
    else:
        bot.send_message(message.chat.id, KEYBOARD_USAGE_ASKING)


@bot.message_handler(
    content_types=['sticker', 'user', 'chat', 'photo', 'audio', 'document', 'video', 'voice', 'contact', 'location',
                   'venue', 'file'])
def answer_sticker(message):
    bot.send_message(message.chat.id, TEXT_USAGE_ASKING)


'''
if __name__ == '__main__':
    bot.polling(none_stop=True)
'''
