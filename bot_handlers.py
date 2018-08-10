from datetime import datetime
import random
import os
import re
from google_images_download import google_images_download

from bot import bot
from buttons import *
from db import users_db


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if users_db.count_documents({USER_ID: message.from_user.id}) != 1:
        if users_db.count_documents({USER_ID: message.from_user.id}) == 0:
            users_db.insert_one({USER_ID: message.from_user.id,
                                NAME: '',
                                SEX: '',
                                STATE: ENTER_NAME,
                                REG_TIME: datetime.utcnow()})   
            bot.send_message(message.chat.id, HELLO_MESSAGE)
        while users_db.count_documents({USER_ID: message.from_user.id}) > 1:
            users_db.delete_one({USER_ID: message.from_user.id})
    else:
        bot.send_message(message.chat.id, HELLO_AGAIN_MESSAGE)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    #  Получаем информацию о пользователе
    user = users_db.find_one({USER_ID: message.from_user.id}) 

    # Ввод имени
    if user[STATE] == ENTER_NAME:
        #  if all([user[USER_ID] == message.from_user.id, user[SEX] == '']):
        if user[SEX] == '':
            users_db.update_one({USER_ID: message.from_user.id}, {"$set": {NAME: message.text, STATE: ENTER_SEX}})
            bot.send_message(message.chat.id, NAME_UPDATED + "\n" + CHOOSE_SEX_ASKING.format(users_db.find_one({USER_ID: user[USER_ID]})[NAME]), reply_markup=keyboard_choose_sex)
        else:
            if message.text == BACK_B:
                bot.send_message(message.chat.id, CHOOSE_OPTION_ASKING, reply_markup=keyboard_choose_option)
                users_db.update_one({USER_ID: user[USER_ID]}, {"$set": {STATE: CHOOSE_OPTION}})
            else:
                users_db.update_one({USER_ID: user[USER_ID]}, {"$set": {NAME: message.text, STATE: CONTINUE_CONVERSATION}})
                bot.send_message(message.chat.id, NAME_UPDATED, reply_markup=keyboard_continue_conversation)

    #  Ввод пола
    elif user[STATE] == ENTER_SEX:
        if any([message.text == MALE_B, message.text == FEMALE_B, message.text == OTHER_B]):
            users_db.update_one({USER_ID: user[USER_ID]},
                                {"$set": {SEX: message.text,STATE: CONTINUE_CONVERSATION}})
            bot.send_message(message.chat.id,
                             SEX_UPDATED + '\n' + YOUR_SEX.format(users_db.find_one({USER_ID: user[USER_ID]})[SEX]),
                             reply_markup=keyboard_continue_conversation)
        elif re.search('[a-zA-Z\d]', message.text):
            bot.send_message(message.chat.id, CHAR_ASKING)
        else:
            bot.send_message(message.chat.id, KEYBOARD_USAGE_ASKING)
        
    #  Продолжение диалога
    elif user[STATE] == CONTINUE_CONVERSATION:
        if message.text == SETTINGS_B:
            bot.send_message(message.chat.id, CHOOSE_OPTION_ASKING, reply_markup=keyboard_choose_option)
            users_db.update_one({USER_ID: user[USER_ID]}, {"$set": {STATE: CHOOSE_OPTION}})
        elif message.text == HELLO_B:
            MY_FRIEND_DICT = {MALE_B: MY_FRIEND_M, FEMALE_B: MY_FRIEND_F, OTHER_B: MY_FRIEND_NA}
            if 0 <= datetime.now().hour < 6:
                time_recourse = GOOD_NIGHT
            elif 6 <= datetime.now().hour < 12:
                time_recourse = GOOD_MORNING
            elif 6 <= datetime.now().hour < 18:
                time_recourse = GOOD_DAY
            elif 18 <= datetime.now().hour < 24:
                time_recourse = GOOD_EVENING
            bot.send_message(message.chat.id, time_recourse + MY_FRIEND_DICT[user[SEX]] + user[NAME], reply_markup=keyboard_continue_conversation)
        elif message.text == CAT_B:
            response = google_images_download.googleimagesdownload()   #class instantiation

            arguments = {"keywords": "cats", "limit": 10, "print_urls": True}   #creating list of arguments
            paths = response.download(arguments)   #passing the arguments to the function
            path_to_photo = random.choice(os.listdir('C:\Users\Admin\Documents\Telegram Bots\transgendebrot\downloads\cats'))
            bot.send_photo(chat_id=chat_id, photo=open(path_to_photo, 'rb'))
            #print(paths)   #printing absolute paths of the downloaded images
            '''#print(search('cats images')) # returns 10 or less results

            from urllib.request import urlopen
            html = urlopen("http://www.google.com/")
            print(html)'''
            '''html_page = urlopen('https://www.google.com/images?source=hp&q=cat')
            soup = BeautifulSoup(html_page)
            images = []
            for img in soup.findAll('img'):
                images.append(img.get('src'))

            print(html_page)
            print(images)'''
            
            '''file = StringIO(urlopen('https://www.google.com/images?source=hp&q=cat').read())
            img = Image.open(file)'''
            #AIzaSyBnfuhm0-3nmpJiKALee699gGLPeqegovQ
            #cats = requests('https://www.google.com/imghp/cats.png')
            #cats = requests.get('http://bipbap.ru/wp-content/uploads/2017/09/5.jpg')
            #cats = "https://www.imdb.com/search/title?release_date={}-01-01,2018-12-31&amp;user_rating={}&amp;genres={}".format(1999, 0, 'horror')
            #params = {"chat_id": user[USER_ID],"text": cats,"parse_mode": "HTML",}
            #requests.get("https://api.telegram.org/{}/sendMessage".format(config.TOKEN),params=params)
            #bot.send_message(message.chat.id, cats)
            #bot.send_message(message.chat.id, open('https://cs8.pikabu.ru/post_img/2016/12/28/1/1482881197192578721.jpg', 'rb'))
            #webbrowser.open_new_tab('https://www.google.ru/search?q=cats&newwindow=1&espv=2&source=lnms&tbm=isch&sa=X')
        else: bot.send_message(message.chat.id, KEYBOARD_USAGE_ASKING)
            
    #  Смена имени и пола
    elif user[STATE] == CHOOSE_OPTION:
        if message.text == CHANGE_SEX_B:
            bot.send_message(message.chat.id, CHOOSE_SEX_ASKING.format(user[NAME]), reply_markup=keyboard_choose_sex)
            users_db.update_one({USER_ID: user[USER_ID]}, {"$set": {SEX: '', STATE: ENTER_SEX}}) 
        elif message.text == CHANGE_NAME_B:
            bot.send_message(message.chat.id, CHOOSE_NAME_ASKING.format(user[NAME]), reply_markup=keyboard_back)    
            users_db.update_one({USER_ID: user[USER_ID]}, {"$set": {STATE: ENTER_NAME}}) 
        else:
            bot.send_message(message.chat.id, KEYBOARD_USAGE_ASKING)
        
    #  Неверный ввод
    else:
        bot.send_message(message.chat.id, KEYBOARD_USAGE_ASKING)


@bot.message_handler(content_types=['sticker', 'user', 'chat', 'photo', 'audio', 'document', 'video', 'voice', 'contact', 'location', 'venue', 'userprofilephotos', 'file'])
def answer_sticker(message):
    bot.send_message(message.chat.id, TEXT_USAGE_ASKING)    


if __name__ == '__main__':
    bot.polling(none_stop=True)
