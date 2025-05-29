import telebot
from telebot import types
import requests
import json
import threading
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import os
import math

bot = telebot.TeleBot('TOKEN')
matplotlib.use('agg')

def appending_crypto():
    last_time = 0
    last_day = 0
    while True:
        if last_day == datetime.now().day:
            if last_time != datetime.now().hour:
                with open('crypto_data/crypto_graph.json') as f:
                    templates = json.load(f)
                    for temp in templates:
                        response = requests.get(f'https://api.coinbase.com/v2/exchange-rates?currency={temp}').json()
                        templates[temp].append(response['data']['rates']['RUB'])

                        with open('crypto_data/crypto_graph.json', 'w') as file:
                            json.dump(templates, file)

            last_time = datetime.now().hour
        else:
            with open('crypto_data/crypto_graph.json') as f:
                templates = json.load(f)
                for temp in templates:
                    templates[temp] = []

                    with open('crypto_data/crypto_graph.json', 'w') as file:
                        json.dump(templates, file)
        
        last_day = datetime.now().day

oup = threading.Thread(target=appending_crypto, daemon=True)
oup.start()

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот который поможет тебе в трейденге, спросишь типо СКАМ?!\n' + 
                     'Нет кончено это не скам а просто симулятор!\nИ ваще регай аккаун командой /reg_accaunt и иди играй биоробот с нижнего интирнета!\n' + 
                     'А ну и что бы всё выглядело типо дорого на смайлики 🤑🤑🤑')
    
@bot.message_handler(commands=['reg_accaunt'])
def handle_start(message):
    write_data = {'name': message.from_user.first_name, 'BTC': 0, 'ETH': 0, 'USDT': 10000, 'XRP': 0, 'Buy1': '', 'Buy2': '', 'BuyL': -1}

    with open(f'accaunts/{message.from_user.id}.json', 'w') as file:
        json.dump(write_data, file)

    bot.send_message(message.chat.id, 'Аккунт успешно создан!')

@bot.message_handler(commands=['price'])
def handle_start(message):
    if os.path.exists(f'accaunts/{message.from_user.id}.json'):
        keyboard = types.InlineKeyboardMarkup()

        BTCButt = types.InlineKeyboardButton(text='BTC', callback_data='1BTC')
        ETCButt = types.InlineKeyboardButton(text='ETH', callback_data='1ETH')
        keyboard.row(BTCButt, ETCButt)

        USDTButt = types.InlineKeyboardButton(text='USDT', callback_data='1USDT')
        XRPButt = types.InlineKeyboardButton(text='XRP', callback_data='1XRP')
        keyboard.row(USDTButt, XRPButt)

        bot.send_message(message.chat.id, 'Выберите монету что бы узнать ее динамику', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Чё совсем тикток головного мозга?\nАККАУН РЕГНУТЬ СКАЗАЛИ')

@bot.message_handler(commands=['buy'])
def handle_start(message):
    if os.path.exists(f'accaunts/{message.from_user.id}.json'):
        keyboard = types.InlineKeyboardMarkup()

        BTCButt = types.InlineKeyboardButton(text='BTC', callback_data='2BTC')
        ETCButt = types.InlineKeyboardButton(text='ETH', callback_data='2ETH')
        keyboard.row(BTCButt, ETCButt)

        USDTButt = types.InlineKeyboardButton(text='USDT', callback_data='2USDT')
        XRPButt = types.InlineKeyboardButton(text='XRP', callback_data='2XRP')
        keyboard.row(USDTButt, XRPButt)

        bot.send_message(message.chat.id, 'Выберите монету за которую хотите купить', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Чё совсем тикток головного мозга?\nАККАУН РЕГНУТЬ СКАЗАЛИ')

@bot.message_handler(commands=['my'])
def handle_start(message):
    if os.path.exists(f'accaunts/{message.from_user.id}.json'):
        with open(f'accaunts/{message.from_user.id}.json') as f:
            templates = json.load(f)
        
        bot.send_message(message.chat.id, f'У вас есть:\nBTC в количестве {templates['BTC']}\nETH в количестве {templates['ETH']}\n' +
                         f'USDT в количестве {templates['USDT']}\nXRP в количестве {templates['XRP']}')
    else:
        bot.send_message(message.chat.id, 'Чё совсем тикток головного мозга?\nАККАУН РЕГНУТЬ СКАЗАЛИ')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data[0] == '1':
            dta = call.data[1:]
            bot.delete_message(call.message.chat.id, call.message.message_id)

            bot.send_message(call.message.chat.id, 'Идёт создание графика...')

            response = requests.get(f'https://api.coinbase.com/v2/exchange-rates?currency={dta}').json()

            with open('crypto_data/crypto_graph.json') as f:
                templates = json.load(f)

            with open(f'accaunts/{call.from_user.id}.json') as f:
                templates2 = json.load(f)

            plt.plot([math.ceil(float(i)) for i in templates[dta]], marker = 'o')
            plt.savefig('matplot_im/plot_im.png')

            bot.send_photo(call.message.chat.id, open('matplot_im/plot_im.png', 'rb'), caption=f'Цена на {dta} сейчас: {str(response['data']['rates']['RUB'])}\n' + 
                           f'У вас {str(templates2[dta])}')

            os.remove('matplot_im/plot_im.png')
            plt.close()

        if call.data[0] == '2':
            dta = call.data[1:]
            bot.delete_message(call.message.chat.id, call.message.message_id)

            with open(f'accaunts/{call.from_user.id}.json') as f:
                templates = json.load(f)

            templates['Buy1'] = dta

            with open(f'accaunts/{call.from_user.id}.json', 'w') as file:
                json.dump(templates, file)

            keyboard = types.InlineKeyboardMarkup()

            BTCButt = types.InlineKeyboardButton(text='BTC', callback_data='3BTC')
            ETCButt = types.InlineKeyboardButton(text='ETH', callback_data='3ETH')
            keyboard.row(BTCButt, ETCButt)

            USDTButt = types.InlineKeyboardButton(text='USDT', callback_data='3USDT')
            XRPButt = types.InlineKeyboardButton(text='XRP', callback_data='3XRP')
            keyboard.row(USDTButt, XRPButt)

            bot.send_message(call.message.chat.id, f'Выберите монету которую хотите купить за {dta}', reply_markup=keyboard)
        
        if call.data[0] == '3':
            dta = call.data[1:]
            bot.delete_message(call.message.chat.id, call.message.message_id)

            with open(f'accaunts/{call.from_user.id}.json') as f:
                templates = json.load(f)

            templates['Buy2'] = dta

            bot.send_message(call.message.chat.id, f'Укажите количество {templates['Buy2']} которое хотите купить за {templates['Buy1']}')

            with open(f'accaunts/{call.from_user.id}.json', 'w') as file:
                json.dump(templates, file)

        if call.data == 'YesCB':
            with open(f'accaunts/{call.from_user.id}.json') as f:
                templates = json.load(f)

            response = float(requests.get(f'https://api.coinbase.com/v2/exchange-rates?currency={templates['Buy2']}').json()['data']['rates'][templates['Buy1']]) * float(templates['BuyL'])
            bot.delete_message(call.message.chat.id, call.message.message_id)

            if response < templates[templates['Buy1']]:
                bot.send_message(call.message.chat.id, f'Вы успешно купили {templates['Buy2']}!')

                templates[templates['Buy2']] += templates['BuyL']
                templates[templates['Buy1']] -= response

                templates['Buy1'] = ''
                templates['Buy2'] = ''
                templates['BuyL'] = -1
            else:
                bot.send_message(call.message.chat.id, f'Вам не хватает {templates['Buy1']}!')

                templates['Buy1'] = ''
                templates['Buy2'] = ''
                templates['BuyL'] = -1

            with open(f'accaunts/{call.from_user.id}.json', 'w') as file:
                json.dump(templates, file)

        if call.data == 'NoCB':
            with open(f'accaunts/{call.from_user.id}.json') as f:
                templates = json.load(f)

            templates['Buy1'] = ''
            templates['Buy2'] = ''
            templates['BuyL'] = -1

            with open(f'accaunts/{call.from_user.id}.json', 'w') as file:
                json.dump(templates, file)

            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Ок')

@bot.message_handler(content_types = ['text'])
def main(message):
    if os.path.exists(f'accaunts/{message.from_user.id}.json'):
        if message.text.isdigit() == True:
            with open(f'accaunts/{message.from_user.id}.json') as f:
                templates = json.load(f)

            if templates['Buy1'] != '' and templates['Buy2'] != '':
                templates['BuyL'] = int(message.text)

                response = float(requests.get(f'https://api.coinbase.com/v2/exchange-rates?currency={templates['Buy2']}').json()['data']['rates'][templates['Buy1']]) * float(message.text)

                with open(f'accaunts/{message.from_user.id}.json', 'w') as file:
                    json.dump(templates, file)

                keyboard = types.InlineKeyboardMarkup()

                YesCB = types.InlineKeyboardButton(text='Да!', callback_data='YesCB')
                NoCB = types.InlineKeyboardButton(text='Нет', callback_data='NoCB')
                keyboard.row(YesCB, NoCB)

                bot.send_message(message.chat.id, f'Цена составит {str(response)}\nВы точно хотите купить?', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Чё совсем тикток головного мозга?\nАККАУН РЕГНУТЬ СКАЗАЛИ')

bot.polling(none_stop=True)