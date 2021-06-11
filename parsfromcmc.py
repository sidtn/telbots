from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import telebot

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'500',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'API_KEY',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

def creat_price_lists(list, index_valute):
    price_list = []
    for coin in list:
        for keys in coin.keys():
            if coin['symbol'] == index_valute:
                price_list.append(coin['quote'])
                break
    return price_list

def creat_ptice_dict(list):
    price_dict = {}
    for dict_price in list:
        for keys, values in dict_price.items():
            for key, value in values.items():
                price_dict['Цена'] = round(values['price'],5)
                price_dict['Изменение за последние сутки'] = round(values['percent_change_24h'], 2)
                price_dict['Изменение за месяц'] = round(values['percent_change_30d'], 2)
                price_dict['Капитализация'] = round(values['market_cap'])
    return price_dict

coins = (data['data'])


bot = telebot.TeleBot('API_KEY')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Введите индеск криптовалюты, например 'btc'")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    valute = message.text.upper()
    price = creat_price_lists(coins, valute)
    try:
        price_dict = creat_ptice_dict(price)
        bot.reply_to(message, 'Цена : {} USD\n'
                              'Изменение за последние сутки : {} %\n'
                              'Изменение за месяц : {} %\n'
                              'Капитализация : {} USD'
                             .format(price_dict['Цена'],
                             price_dict['Изменение за последние сутки'],
                             price_dict['Изменение за месяц'],
                             price_dict['Капитализация']))
    except:
        bot.reply_to(message, 'Такого индекса не существует, попробуйте ще раз.')


bot.polling()
