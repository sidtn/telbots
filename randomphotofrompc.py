import telebot
import os
import random

path = 'D:\photo'

def creat_list_photo(dir_path):
    listp = []
    for adress, dirs, files in os.walk(dir_path):
        for file in files:
            if '.jpg' or '.png' in file:
                listp.append(os.path.join(adress, file))
    return(listp)	

list_pic = creat_list_photo(path)

bot = telebot.TeleBot('API_KEY')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет, напиши что-нибудь сюда!")

@bot.message_handler(func=lambda m: True)
def send_photo(message):
    img = open(random.choice(list_pic), 'rb')
    try:
        bot.send_message(message.chat.id, 'Вот тебе случайная фотка с компа:')
        bot.send_photo(message.chat.id, img)
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так, попробуй еще.')

bot.polling()
