import telebot
from config import TOKEN
import save_data as SD
import datetime
import random

bot = telebot.TeleBot(TOKEN)

def save(message, callback):
    # markup = telebot.types.ReplyKeyboardRemove(selective=False)
    # bot.send_message(message.chat.id, '...', reply_markup=markup)
    try:
        callback(message.text)
    except Exception as e:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bot.reply_to(message, f"{now} [Данные потеряны]: {e}")
    else:
        bot.reply_to(message, 'Данные сохранены')

def save_glucose(message):
    save(message, SD.save_glucose)

def save_insulin(message):
    save(message, SD.save_insulin)

def save_food(message):
    save(message, SD.save_food)

def check_num(message, num, attempt):
    if message.text == str(num):
        bot.reply_to(message, f'Верно! С {attempt} попытки')
    else:
        mess = bot.send_message(message.chat.id, 'Неверно! Попробуй еще:')
        bot.register_next_step_handler(mess, check_num, num, attempt + 1)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Добро пожаловать!')
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('Сохранить данные')
    item2 = telebot.types.KeyboardButton('Угадать число')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Выберите, что вы хотите сделать', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Сохранить данные':
        markup = telebot.types.InlineKeyboardMarkup(row_width=3)
        item1 = telebot.types.InlineKeyboardButton('Глюкоза', callback_data='glucose')
        item2 = telebot.types.InlineKeyboardButton('Инсулин', callback_data='insulin')
        item3 = telebot.types.InlineKeyboardButton('Еда', callback_data='food')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Тип данных', reply_markup=markup)
    elif message.text == 'Угадать число':
        num = random.randint(1, 10)
        mess = bot.send_message(message.chat.id, 'Угадайте число от 1 до 10')
        bot.register_next_step_handler(mess, check_num, num, 1)
    """ params = message.text.split()
    print(params)
    if len(params) == 3:
        return
    else:
        # bot.send_message(message.chat.id, 'Неопознанная строка. Вводить данные нужно так: Глюкоза Инсулин ХЕ')
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        item1 = telebot.types.InlineKeyboardButton('Глюкоза', callback_data='glucose')
        item2 = telebot.types.InlineKeyboardButton('Инсулин', callback_data='insulin')
        item3 = telebot.types.InlineKeyboardButton('Еда', callback_data='food')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Что?', reply_markup=markup) """

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    if call.data == 'glucose':
        bot.reply_to(call.message, 'Введите значение глюкозы (mmol/l):')
        bot.register_next_step_handler(call.message, save_glucose)
    elif call.data == 'insulin':
        bot.reply_to(call.message, 'Введите значение введенного инсулина (ед):')
        bot.register_next_step_handler(call.message, save_insulin)
    elif call.data == 'food':
        bot.reply_to(call.message, 'Введите значение объема еды (ХЕ):')
        bot.register_next_step_handler(call.message, save_food)

bot.infinity_polling()