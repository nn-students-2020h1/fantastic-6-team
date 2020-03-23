"""Fantastic Bot by Team Six"""

# !/usr/local/bin/python3
# -*- coding: utf-8 -*-

# <BASIC IMPORTS>
import logging
from setup import PROXY, TOKEN
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

# <LESSON 3>
# работа с файлами
import os
# системное время для логов
import datetime
# красиво берем последние N строк из файла
from collections import deque
# корректный вывод docstring'ов для задекорированных команд
from functools import wraps

# <LESSON 4>
# запросы и парсинг
import requests
# рандомные факты про котиков
from random import randint

# <LESSON 5>
import csv
STOP_YEAR = 2019  # до какого года листать базу если не можем получить файл
COVID_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/' \
               'master/csse_covid_19_data/csse_covid_19_daily_reports/'

# <ADDITIONAL>
# встроенная клавиатура в сообщениях и обработка нажатий
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler

bot = Bot(token=TOKEN, base_url=PROXY)
HISTORY_SIZE = 5  # сколько действий в логе выводить по запросу

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Функционал сгруппирован по урокам
# ----------------------------------------------------------
# <LESSON 3. ИСКЛЮЧЕНИЯ, ДЕКОРАТОРЫ>


def rip(file):
    """Удаление в три буквы для ленивых"""
    if os.path.exists(file):
        os.remove(file)


def cleaner(func_to_decorate):
    """Удаляет временные файлы перед запуском func_to_decorate"""
    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        rip('index.html')
        rip('avatar.jpeg')
        rip('log_actions.txt')
        rip('log_actions_short.txt')
        rip('log_errors.txt')
        rip('log_errors_short.txt')
        rip('china_data.csv')
        rip('china_data_prev.csv')
        func_to_decorate(*args, **kwargs)
    return wrapper


def log_errors(func_to_decorate):
    """Логирование ошибок в файл."""
    @wraps(func_to_decorate)  # сохраняем для декоратора
    # docstring оборачиваемой функции (нужно для /features)
    def wrapper(*args, **kwargs):
        update = args[0]
        try:
            # проверяем функцию и пытаемся запустить
            if not update:
                raise UpdateError("Impossible to get update!")
            if not hasattr(update, 'effective_user'):
                raise UpdateError(f"Incorrect update format!")
            return func_to_decorate(*args, **kwargs)
        except Exception as err_code:
            # если не работает - логи в файл
            now = datetime.datetime.now()
            content = {
                'time': now.strftime("%H:%M:%S %d.%m.%y"),
                'user': update.effective_user.first_name,
                'function': func_to_decorate.__name__,
                'error': str(err_code)
                }

            with open('log_errors.txt', 'a') as log_file:
                for key, value in content.items():
                    log_file.writelines(f"{key}: {value}\n")
                log_file.write("\n")
            return None
    return wrapper


def log_actions(func_to_decorate):
    """Логирование действий в файл."""
    @wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        update = args[0]
        if update and hasattr(update, 'message') and hasattr(update, 'effective_user'):
            # пытаемся открыть файл
            try:
                log_file = open('log_actions.txt', 'r')
            except IOError:
                # не открывается -> файла нет -> создаем
                with open('log_actions.txt', 'tw', encoding='utf-8'):
                    pass

            now = datetime.datetime.now()
            content = {
                'time': now.strftime("%H:%M:%S %d.%m.%y"),
                'user': update.effective_user.first_name,
                'function': func_to_decorate.__name__,
                'message': update.message.text
                }

            with open('log_actions.txt', 'a') as log_file:
                for key, value in content.items():
                    log_file.writelines(f"{key}: {value}\n")
                log_file.write("\n")
        return func_to_decorate(*args, **kwargs)
    return wrapper


@log_actions
@log_errors
def history(update: Update, context: CallbackContext):
    """Показать последние <HISTORY_SIZE> сообщений по запросу /history."""
    button_0 = InlineKeyboardButton('Actions', callback_data="0-history-log_actions.txt")
    button_1 = InlineKeyboardButton('Errors', callback_data="1-history-log_errors.txt")
    keyboard = [[button_0], [button_1]]
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Какой лог смотрим?', reply_markup=keyboard_markup)


@log_actions
@log_errors
def history_size(update: Update, context: CallbackContext):
    """Показать текущий размер выводимой истории действий."""
    update.message.reply_text(f'Сейчас я настроен на вывод {HISTORY_SIZE} сообщений.')


@log_actions
@log_errors
def change_history_size(update: Update, context: CallbackContext):
    """Изменить размер выводимой истории действий"""
    button_0 = InlineKeyboardButton('3', callback_data="0-ch_hist_size-3")
    button_1 = InlineKeyboardButton('5', callback_data="1-ch_hist_size-5")
    button_2 = InlineKeyboardButton('10', callback_data="2-ch_hist_size-10")
    keyboard = [[button_0], [button_1], [button_2]]
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Сколько показывать?', reply_markup=keyboard_markup)


def get_log(filename, num=None, update=None):
    """Получить из файла <filename> последние <num> событий"""
    if not num:
        num = HISTORY_SIZE
    try:
        with open(filename) as f:
            # очередь в которую влезет NUM событий
            events = deque(maxlen=num)
            # формируем каждое событие как список параметров- строк с данными
            data = []
            for line in f:
                # события отделены друг от друга пустой строкой
                if line != '\n':
                    # пока нет разделителя - собираем все строки для данного события
                    data.append(line.strip('\n').split(': '))
                else:
                    # нашли разделитель - превращаем собранное событие в словарь, и по новой
                    events.append(dict(data))
                    data = []
        if num == 3:
            word = "события"
        else:
            word = "событий"
        message = f'Последние {num} {word}: \n\n'
        for event in events:
            for key in event:
                message += f'{key}: {event[key]}\n'
            message += '\n'
        return message
    except IOError:
        if update:
            update.callback_query.message.reply_text(f'Не могу прочитать {filename}...'
                                                     f' Он точно есть?')
        return None


# </LESSON 3. ИСКЛЮЧЕНИЯ, ДЕКОРАТОРЫ>>
# ----------------------------------------------------------
# <LESSON 4. МОДУЛИ, ПАКЕТЫ, REQUESTS, JSON>


@log_actions
@log_errors
def ping_intel(update: Update, context: CallbackContext):
    """Пропинговать сайт Intel (задание 2, урок по requests)"""
    r = requests.get('http://www.intel.com')
    if r.status_code == 200:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(r.text)
            update.message.reply_text('Я сохранил себе html, смотри!')
            bot.send_document(chat_id=update.effective_chat.id, document=open('index.html', 'rb'))
    else:
        update.message.reply_text(f'Не могу открыть! Ошибка {r.status_code}')


@log_actions
@log_errors
def git_pic(update: Update, context: CallbackContext):
    """Утащить с Github аватарку (задание 3, урок по requests).
    В каталоге проекта должен находиться файл login.txt c логином и паролем."""
    try:
        with open('login.txt', 'r') as f:
            login = f.readline().strip('\n')
            passw = f.readline().strip('\n')

        url = 'https://api.github.com/user'

        r = requests.get(url, auth=(login, passw))
        if not r.status_code == 200:
            raise ConnectionError

        url = r.json()['avatar_url']

        r = requests.get(url)
        if not r.status_code == 200:
            raise ConnectionError

        with open('avatar.jpeg', 'wb') as f:
            f.write(r.content)
        update.message.reply_text('А кто это у нас такой красивый?')
        bot.send_document(chat_id=update.effective_chat.id, document=open('avatar.jpeg', 'rb'))

    except ConnectionError:
        update.message.reply_text(f"{url} недоступен, ошибка {r.status_code}.")
    except IOError:
        update.message.reply_text('У меня нет твоего login.txt, сорян :(')


def cat_facts_main():
    """Собрать и отсортировать анекдоты про котиков с сайта."""
    url = 'https://cat-fact.herokuapp.com/facts'
    r = requests.get(url)
    if not r.status_code == 200:
        raise ConnectionError
    all_facts = r.json()['all']
    facts = []
    for fact in all_facts:
        if fact['type'] == 'cat':
            pair = fact['upvotes'], fact['text']
            facts.append(pair)
    facts.sort(key=lambda d: d[0], reverse=True)
    return facts


@log_actions
@log_errors
def cat_facts_best(update: Update, context: CallbackContext):
    """Отправить самый популярный факт про котика с сайта."""
    best = cat_facts_main()[0]
    update.message.reply_text(best[1])
    update.message.reply_text(f"Этот факт оценили {best[0]} человек.")


@log_actions
@log_errors
def cat_facts_random(update: Update, context: CallbackContext):
    """Отправить рандомный факт с сайта."""
    facts = cat_facts_main()
    any_fact = facts[randint(0, len(facts)-1)]
    update.message.reply_text(any_fact[1])
    update.message.reply_text(f"Лайков: {any_fact[0]}")


# </LESSON 4>
# ----------------------------------------------------------
# <LESSON 5. API Telegram и CSV>


def date_to_string(date, human=False, split='-'):
    """Собираем из словаря date что-то удобное:
    human=False: название <MM-DD-YYYY>.csv
    human=True: <DD MM YYYY>, между цифрами split"""
    # ВАЖНО: в репозитории формат файлов <МЕСЯЦ>-<ДЕНЬ>-<ГОД>!
    if not human:
        length = len(str(date['month']))
        filename = str(date['month']).zfill(3 - length) + '-'
        length = len(str(date['day']))
        filename += str(date['day']).zfill(3 - length) + '-'
        filename += str(date['year']) + '.csv'
    else:
        length = len(str(date['day']))
        filename = str(date['day']).zfill(3 - length) + split
        length = len(str(date['month']))
        filename += str(date['month']).zfill(3 - length) + split
        filename += str(date['year'])
    return filename


def filename_to_date(filename):
    """Собираем из названия файла удобный словарь для даты"""
    values = filename[:10].split('-')
    keys = ['month', 'day', 'year']
    date = {}
    for k, v in zip(keys, values):
        date[k] = int(v)
    return date


def search_back(date, stop_year, from_url):
    """Ищем на сайте <from_url> файлы с данными, начиная с даты,
    предшествующей <date>, пока не найдем или не достигнем <stop_year>"""
    date = date.copy()
    while True:
        date['day'] -= 1
        if date['day'] == 0:
            date['day'] = 31
            date['month'] -= 1
        if date['month'] == 0:
            date['month'] = 31
            date['year'] -= 1
        if date['year'] == stop_year:
            raise FileNotFoundError
        filename = date_to_string(date)
        url = from_url + filename
        r = requests.get(url)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)
            return filename


@log_actions
@log_errors
def corono_stats(update: Update, context: CallbackContext):
    """Получить с github свежие данные по коронавирусу."""
    try:
        # проверяем сегодняшний день
        date = datetime.datetime.now()
        date = {'day': date.day, 'month': date.month, 'year': date.year}

        filename = date_to_string(date)
        url = COVID_URL + filename
        r = requests.get(url)

        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)
        else:
            filename = search_back(date, STOP_YEAR, COVID_URL)

        button_0 = InlineKeyboardButton('Мир', callback_data=f"0-covid-world-{filename}")
        button_1 = InlineKeyboardButton('Китай', callback_data=f"1-covid-china-{filename}")

        keyboard = [[button_0],
                        [button_1]]

        keyboard_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Где смотрим ситуацию?', reply_markup=keyboard_markup)

    except FileNotFoundError:
        update.message.reply_text(f"Я проверил данные до {STOP_YEAR} года, файлов не найдено :(")
    except ConnectionError:
        update.message.reply_text(f"{url} недоступен, ошибка {r.status_code}.")
    except IOError:
        update.message.reply_text('У меня нет твоего login.txt, сорян :(')


@log_errors
def covid_world_handler(update: Update, context: CallbackContext, filename):
    """Получить данные по зараженным в  мире"""
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        infected = 0
        dead = 0
        for row in reader:
            infected += (int(row['Confirmed']))
            dead += (int(row['Deaths']))
    update.callback_query.message.reply_text(f'В сумме в мире было подтверждено'
                                             f' {infected} зараженных. Проверь сам:')
    bot.send_document(chat_id=update.effective_chat.id, document=open(filename, 'rb'))
    update.callback_query.message.reply_text(f'Да не переживай ты так, из них умерло всего {dead} человек!')


def get_china_data(database_in, database_out):
    """Получить из <database_in> таблицу co значениями из <header> и записать в <database_out>"""
    notes = []
    with open(database_in, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Country/Region'].find('China') != -1:
                notes.append(row)

    with open(database_out, 'w', newline='') as csvfile:
        header = ['Province', 'Last Update', 'Current Cases']
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for row in notes:
            writer.writerow({
                'Province': row["Province/State"],
                'Last Update': row['Last Update'],
                'Current Cases': int(row['Confirmed']) - int(row['Recovered']) - int(row['Deaths'])
            })


@log_errors
def covid_china_handler(update: Update, context: CallbackContext, filename):
    """Получить данные по зараженным в Китае"""
    # актуальная база и дата
    date_actual = filename_to_date(filename)
    get_china_data(filename, 'china_data.csv')

    # прошлая база и дата
    filename_previous = search_back(date_actual, STOP_YEAR, COVID_URL)
    date_previous = filename_to_date(filename_previous)
    get_china_data(filename_previous, 'china_data_prev.csv')

    # приятный глазу вид date_actual и date_previous для ответов бота
    before = date_to_string(date_previous, human=True, split='/')
    after = date_to_string(date_actual, human=True, split='/')

    update.callback_query.message.reply_text(f'Ну-ка, что там у китайцев?'
                                             f' Последний отчет - за {after}:')
    bot.send_document(chat_id=update.effective_chat.id, document=open('china_data.csv', 'rb'))

    # читаем свежую статистику по провинциям
    notes = []
    with open('china_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            notes.append(row)

    # записываем зараженные на данный момент провинции, порядок как в notes
    infected_provinces = [i['Province'] for i in notes]

    # читаем статистику по провинциям из прошлого файла
    with open('china_data_prev.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # для каждой строчки проверяем, не заражена ли сейчас провинция
            # итерируемся именно по её номеру в списке notes
            for number in range(len(infected_provinces)):
                if row['Province'] == infected_provinces[number]:
                    # если заражена - по номеру в списке получаем число больных
                    # и находим, на сколько оно изменилось с прошлого файла
                    notes[number]['Current Cases'] = int(notes[number]['Current Cases'])\
                                                     - int(row['Current Cases'])
                    break

    notes.sort(key=lambda d: int(d['Current Cases']), reverse=True)

    BOOST_INFECTED_TOP = 5
    message = ''
    for data, counter in zip(notes, range(BOOST_INFECTED_TOP)):
        message += f"{data['Province']} - {data['Current Cases']} новых заражённых.\n"

    update.callback_query.message.reply_text(f'Топ-5 провинций по новым зараженным'
                                             f' за период с {before} по {after}:')
    update.callback_query.message.reply_text(message)
    update.callback_query.message.reply_text(f'Всего заражено провинций: {len(notes)} . Жуть какая.')


# </LESSON 5. API Telegram и CSV>
# ----------------------------------------------------------
# <ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ, КЛАВИАТУРЫ>


class UpdateError(Exception):
    """Класс исключений с удобным комментарием"""
    def __init__(self, text):
        self.txt = text


@log_actions
@log_errors
def features(update: Update, context: CallbackContext):
    """Показать все возможности бота по запросу /features со справкой."""
    # настраиваем кнопки
    feature_0 = InlineKeyboardButton('/start', callback_data="0-doc-start")
    feature_1 = InlineKeyboardButton('/help', callback_data="1-doc-chat_help")
    feature_2 = InlineKeyboardButton('/echo', callback_data="2-doc-echo")
    feature_3 = InlineKeyboardButton('/features', callback_data="3-doc-features")
    feature_4 = InlineKeyboardButton('/history', callback_data="4-doc-history")
    feature_5 = InlineKeyboardButton('/history_size', callback_data="5-doc-history_size")
    feature_6 = InlineKeyboardButton('/change_history_size',
                                     callback_data="6-doc-change_history_size")
    feature_7 = InlineKeyboardButton('/ping_intel', callback_data="7-doc-ping_intel")
    feature_8 = InlineKeyboardButton('/git_pic', callback_data="8-doc-git_pic")
    feature_9 = InlineKeyboardButton('/сat_facts_best', callback_data="9-doc-cat_facts_best")
    feature_10 = InlineKeyboardButton('/сat_facts_random', callback_data="10-doc-cat_facts_random")
    feature_11 = InlineKeyboardButton('/corono_stats', callback_data="11-doc-corono_stats")

    # настраиваем клавиатуру
    keyboard = [[feature_0, feature_1, feature_2],
                [feature_3],
                [feature_4, feature_5],
                [feature_6],
                [feature_7, feature_8],
                [feature_9, feature_10],
                [feature_11]]

    keyboard_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Про какую из функций ты хочешь узнать?',
                              reply_markup=keyboard_markup)


def features_handler(update: Update, context: CallbackContext, response):
    """Обработка нажатий кнопок в функции features"""

    update.callback_query.message.reply_text(f"Справка для функции: /{response[2]}")
    try:
        # получаем из имени функции саму функцию, из нее - ее docstring
        # ловим возможные ошибки т.к. пользуемся eval
        func = eval(response[2])
        update.callback_query.message.reply_text(func.__doc__)
    except Exception as err_code:  # широкий except т.к. неизвестно, что может пойти не так
        update.callback_query.message.reply_text(f'Упс! \n {str(err_code)}')
        update.callback_query.message.reply_text(f"{response[2]}: docstring функции недоступен")


def history_handler(update: Update, context: CallbackContext):
    """Обработка нажатий кнопок в функции history"""
    try:
        filename = update.callback_query.data.split('-')[2]  # filename
        message = get_log(filename, update=update)

        if message:
            filename = filename[0:-4] + '_short.txt'
            with open(filename, 'tw', encoding='utf-8') as log:
                log.writelines(message)

            update.callback_query.message.reply_text(message)
            update.callback_query.message.reply_text(f'И ещё лови свой лог файлом.')
            bot.send_document(chat_id=update.effective_chat.id, document=open(filename, 'rb'))

    except Exception as err_code:
        update.callback_query.message.reply_text("Упс! Ошибка при обработке нажатия кнопок!")
        update.callback_query.message.reply_text(str(err_code))


def change_history_size_handler(update: Update, context: CallbackContext, response):
    """Обработка нажатий кнопок в функции change_history_size"""
    global HISTORY_SIZE
    HISTORY_SIZE = int(response[2])
    update.callback_query.message.reply_text(f'Окей, пусть будет {HISTORY_SIZE}.')


def callback_worker(update: Update, context: CallbackContext):
    """Обработка запросов, полученных с клавиатуры"""
    try:
        response = update.callback_query.data.split('-', 3)
        # формат строки callback_query.data для моих клавиатур:
        # <номер кнопки>-<id>-<данные для работы функции>-<название файла, если есть>
        if response[1] == "doc":
            features_handler(update, context, response)
        elif response[1] == "history":
            history_handler(update, context)
        elif response[1] == "ch_hist_size":
            change_history_size_handler(update, context, response)
        elif response[1] == "covid":
            filename = response[3]
            if response[2] == 'world':
                covid_world_handler(update, context, filename)
            elif response[2] == 'china':
                covid_china_handler(update, context, filename)

    except Exception as err_code:
        update.callback_query.message.reply_text("Упс! Ошибка при обработке нажатия кнопок!")
        update.callback_query.message.reply_text(str(err_code))


# </ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ, КЛАВИАТУРЫ>
# ----------------------------------------------------------
# <СТАНДАРТНЫЕ ФУНКЦИИ БОТА>


@cleaner
@log_actions
@log_errors
def start(update: Update, context: CallbackContext):
    """Выкинуть мусор и отправить приветственное сообщение по запросу /start."""
    update.message.reply_text(f'Привет, {update.effective_user.first_name}!')


@log_actions
@log_errors
def chat_help(update: Update, context: CallbackContext):
    """Помочь пользователю по запросу /help."""
    update.message.reply_text('Введи команду /start для начала. \n'
                              'Команда /features - мои возможности.')


def echo(update: Update, context: CallbackContext):
    """Эхо сообщения собеседника, отправляется по умолчанию."""
    update.message.reply_text(update.message.text)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


def main():
    updater = Updater(bot=bot, use_context=True)

    # Define a few command handlers. These usually take the two arguments update and
    # context. Error handlers also receive the raised TelegramError object in error.

    # (time, user, function, message/error, \n)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))

    # <FEATURES FROM FANTASTIC SIX>
    updater.dispatcher.add_handler(CommandHandler('features', features))
    updater.dispatcher.add_handler(CommandHandler('history', history))
    updater.dispatcher.add_handler(CommandHandler('history_size', history_size))
    updater.dispatcher.add_handler(CommandHandler('change_history_size', change_history_size))
    updater.dispatcher.add_handler(CommandHandler('ping_intel', ping_intel))
    updater.dispatcher.add_handler(CommandHandler('git_pic', git_pic))
    updater.dispatcher.add_handler(CommandHandler('cat_facts_best', cat_facts_best))
    updater.dispatcher.add_handler(CommandHandler('cat_facts_random', cat_facts_random))
    updater.dispatcher.add_handler(CommandHandler('corono_stats', corono_stats))

    updater.dispatcher.add_handler(CallbackQueryHandler(callback_worker))
    # </FEATURES FROM FANTASTIC SIX>

    # on noncommand i.e message - echo the message on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()
