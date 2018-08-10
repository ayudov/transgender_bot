from telebot import types
from messages import * 	

#Кнопки для выбора пола
keyboard_choose_sex = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_male = types.KeyboardButton(text = MALE_B)
button_female = types.KeyboardButton(text = FEMALE_B)
button_other = types.KeyboardButton(text = OTHER_B)
keyboard_choose_sex.add(button_male, button_female, button_other)

#Кнопки для продолжения диалога
keyboard_continue_conversation = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_hello = types.KeyboardButton(text = HELLO_B)
button_settings = types.KeyboardButton(text = SETTINGS_B)
button_cat = types.KeyboardButton(text = CAT_B)
keyboard_continue_conversation.add(button_hello, button_settings, button_cat)

#Кнопки для выбора опции
keyboard_choose_option = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_change_name = types.KeyboardButton(text = CHANGE_NAME_B)
button_change_sex = types.KeyboardButton(text = CHANGE_SEX_B)
keyboard_choose_option.add(button_change_name, button_change_sex)

#Кнопки для возврата назад
keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_back = types.KeyboardButton(text = BACK_B)
keyboard_back.add(button_back)