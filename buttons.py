from telebot import types

#Кнопки для выбора пола
keyboard_choose_sex = types.ReplyKeyboardMarkup(True, True)
button_male = types.KeyboardButton(text = 'М')
button_female = types.KeyboardButton(text = 'Ж')
button_other = types.KeyboardButton(text = 'Другое')
keyboard_choose_sex.add(button_male, button_female, button_other)

#Кнопки для продолжения диалога
keyboard_continue_conversation = types.ReplyKeyboardMarkup(True, True)
button_hello = types.KeyboardButton(text = 'Поздороваться')
button_change = types.KeyboardButton(text = 'Сменить пол')
keyboard_continue_conversation.add(button_hello, button_change)

#Кнопка для начала диалога
keyboard_start_conversation = types.ReplyKeyboardMarkup(True, True)
button_start = types.KeyboardButton(text = '/start')
keyboard_start_conversation.add(button_start)