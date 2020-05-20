"""Fantastic Bot by Team Six"""

# !/usr/local/bin/python3
# -*- coding: utf-8 -*-

# <BASIC IMPORTS>
import logging

from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

# <LESSON 3>
# работа с файлами
import os

# красиво берем последние N строк из файла
from collections import deque


# <LESSON 4>
# запросы и парсинг
import requests
# рандомные факты про котиков
from random import randint

# <LESSON 5>
import csv
from copy import copy
from datetime import datetime, date, timedelta  # удобные операции со временем
STOP_YEAR = 2019  # до какого года листать базу если не можем получить файл
COVID_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/' \
               'master/csse_covid_19_data/csse_covid_19_daily_reports/'

# <ADDITIONAL>
# встроенная клавиатура в сообщениях и обработка нажатий
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler

# <LESSON 6. OOP>
import auxillary as aux


class FantasticBot:
    # <LESSON 6. OOP>

    def __init__(self, TOKEN, PROXY, HISTORY_SIZE=5):
        self.bot = Bot(token=TOKEN, base_url=PROXY)
        self.updater = Updater(bot=self.bot, use_context=True)
        self.h_size = HISTORY_SIZE  # сколько действий в логе выводить по запросу

        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logger = logging.getLogger(__name__)

    # </LESSON 6. OOP>
    # ----------------------------------------------------------
    # # <LESSON 3. ИСКЛЮЧЕНИЯ, ДЕКОРАТОРЫ>>

    @aux.log_actions
    @aux.log_errors
    def history(self, update: Update, context: CallbackContext):
        """Показать последние <HISTORY_SIZE> сообщений по запросу /history."""
        button_actions = InlineKeyboardButton('Actions', callback_data="0-history-log_actions.txt")
        button_errors = InlineKeyboardButton('Errors', callback_data="1-history-log_errors.txt")
        keyboard = [[button_actions], [button_errors]]
        keyboard_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Какой лог смотрим?', reply_markup=keyboard_markup)

    @aux.log_actions
    @aux.log_errors
    def history_size(self, update: Update, context: CallbackContext):
        """Показать текущий размер выводимой истории действий."""
        update.message.reply_text(f'Сейчас я настроен на вывод {self.h_size} сообщений.')

    @aux.log_actions
    @aux.log_errors
    def change_history_size(self, update: Update, context: CallbackContext):
        """Изменить размер выводимой истории действий"""
        button_0 = InlineKeyboardButton('3', callback_data="0-ch_hist_size-3")
        button_1 = InlineKeyboardButton('5', callback_data="1-ch_hist_size-5")
        button_2 = InlineKeyboardButton('10', callback_data="2-ch_hist_size-10")
        keyboard = [[button_0], [button_1], [button_2]]
        keyboard_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Сколько показывать?', reply_markup=keyboard_markup)

    def get_log(self, filename, num=None, update=None):
        """Получить из файла <filename> последние <num> событий"""
        if not num:
            num = self.h_size
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

    @aux.log_actions
    @aux.log_errors
    def ping_intel(self, update: Update, context: CallbackContext):
        """Пропинговать сайт Intel (задание 2, урок по requests)"""
        r = requests.get('http://www.intel.com')
        if r.status_code == 200:
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(r.text)
                update.message.reply_text('Я сохранил себе html, смотри!')
                self.bot.send_document(chat_id=update.effective_chat.id, document=open('index.html', 'rb'))
        else:
            update.message.reply_text(f'Не могу открыть! Ошибка {r.status_code}')

    @aux.log_actions
    @aux.log_errors
    def git_pic(self, update: Update, context: CallbackContext):
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
            self.bot.send_document(chat_id=update.effective_chat.id, document=open('avatar.jpeg', 'rb'))

        except ConnectionError:
            update.message.reply_text(f"{url} недоступен, ошибка {r.status_code}.")
        except IOError:
            update.message.reply_text('У меня нет твоего login.txt, сорян :(')

    @staticmethod
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

    @aux.log_actions
    @aux.log_errors
    def cat_facts_best(self, update: Update, context: CallbackContext):
        """Отправить самый популярный факт про котика с сайта."""
        best = FantasticBot.cat_facts_main()[0]
        update.message.reply_text(best[1])
        update.message.reply_text(f"Этот факт оценили {best[0]} человек.")

    @aux.log_actions
    @aux.log_errors
    def cat_facts_random(self, update: Update, context: CallbackContext):
        """Отправить рандомный факт с сайта."""
        facts = FantasticBot.cat_facts_main()
        any_fact = facts[randint(0, len(facts)-1)]
        update.message.reply_text(any_fact[1])
        update.message.reply_text(f"Лайков: {any_fact[0]}")

    # </LESSON 4>
    # ----------------------------------------------------------
    # <LESSON 5. API Telegram и CSV>

    @staticmethod
    def filename_to_date(filename):
        """Делаем из названия файла удобный объект date"""
        values = filename[:10].split('-')
        # datetime.date имеет вид year, month, day
        date_obj = date(int(values[2]), int(values[0]), int(values[1]))
        return date_obj

    @staticmethod
    def search_back(date_obj, stop_year, from_url):
        """Ищем на сайте <from_url> файлы с данными, начиная с даты,
        предшествующей <date>, пока не найдем или не достигнем <stop_year>"""
        date_obj = copy(date_obj)
        while True:
            date_obj = date_obj - timedelta(1)
            if date_obj.year == stop_year:
                raise FileNotFoundError
            filename = date_obj.strftime("%m-%d-%Y.csv")
            url = from_url + filename
            r = requests.get(url)
            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(r.content)
                return filename

    @aux.log_actions
    @aux.log_errors
    def corono_stats(self, update: Update, context: CallbackContext):
        """Получить с github свежие данные по коронавирусу."""
        try:
            # проверяем сегодняшний день
            date_obj = datetime.today()
            filename = date_obj.strftime("%m-%d-%Y.csv")

            url = COVID_URL + filename
            r = requests.get(url)

            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(r.content)
            else:
                filename = FantasticBot.search_back(date_obj, STOP_YEAR, COVID_URL)

            button_world = InlineKeyboardButton('Мир', callback_data=f"0-covid-world-{filename}")
            button_china = InlineKeyboardButton('Китай', callback_data=f"1-covid-china-{filename}")

            keyboard = [[button_world],
                        [button_china]]

            keyboard_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Где смотрим ситуацию?', reply_markup=keyboard_markup)

        except FileNotFoundError:
            update.message.reply_text(f"Я проверил данные до {STOP_YEAR} года, файлов не найдено :(")
        except ConnectionError:
            update.message.reply_text(f"{url} недоступен, ошибка {r.status_code}.")
        except IOError:
            update.message.reply_text('У меня нет твоего login.txt, сорян :(')

    @aux.log_errors
    def covid_world_handler(self, update: Update, context: CallbackContext, filename):
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
        self.bot.send_document(chat_id=update.effective_chat.id, document=open(filename, 'rb'))
        update.callback_query.message.reply_text(f'Да не переживай ты так, из них умерло всего {dead} человек!')

    @staticmethod
    def get_china_data(database_in, database_out):
        """Получить из <database_in> таблицу co значениями из <header> и записать в <database_out>"""
        notes = []
        with open(database_in, 'r') as file:
            reader = csv.DictReader(file)
            try:  # пытаемся искать записи в новом формате
                for row in reader:
                    if row['Country_Region'].find('China') != -1:
                        notes.append(row)
            except KeyError:  # не нашли: пытаемся искать в старом формате
                for row in reader:
                    if row['Country/Region'].find('China') != -1:
                        notes.append(row)

        with open(database_out, 'w', newline='') as csvfile:
            header = ['Province', 'Last Update', 'Current Cases']
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            try:  # пытаемся искать записи в новом формате
                for row in notes:
                    writer.writerow({
                        'Province': row["Province_State"],
                        'Last Update': row['Last_Update'],
                        'Current Cases': int(row['Confirmed']) - int(row['Recovered']) - int(row['Deaths'])
                    })
            except KeyError:  # не нашли: пытаемся искать в старом формате
                for row in notes:
                    writer.writerow({
                        'Province': row["Province/State"],
                        'Last Update': row['Last Update'],
                        'Current Cases': int(row['Confirmed']) - int(row['Recovered']) - int(row['Deaths'])
                    })

    @aux.log_errors
    def covid_china_handler(self, update: Update, context: CallbackContext, filename):
        """Получить данные по зараженным в Китае"""
        # актуальная база и дата
        date_actual = FantasticBot.filename_to_date(filename)
        FantasticBot.get_china_data(filename, 'china_data.csv')

        # прошлая база и дата
        filename_previous = FantasticBot.search_back(date_actual, STOP_YEAR, COVID_URL)
        date_previous = FantasticBot.filename_to_date(filename_previous)
        FantasticBot.get_china_data(filename_previous, 'china_data_prev.csv')

        # приятный глазу вид date_actual и date_previous для ответов бота
        before = date_previous.strftime("%d/%m/%Y")
        after = date_actual.strftime("%d/%m/%Y")

        update.callback_query.message.reply_text(f'Ну-ка, что там у китайцев?'
                                                 f' Последний отчет - за {after}:')
        self.bot.send_document(chat_id=update.effective_chat.id, document=open('china_data.csv', 'rb'))

        # читаем свежую статистику по провинциям
        notes = []
        with open('china_data.csv', 'r') as csvfile:
            notes = list(csv.DictReader(csvfile))

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
    # <ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ, ОБРАБОТЧИКИ, КЛАВИАТУРЫ>

    def features_set_keyboard(self):
        """Формирование клавиатуры справки по функциям"""
        # настраиваем кнопки
        feature_0 = InlineKeyboardButton('/start', callback_data="0-doc-start")
        feature_1 = InlineKeyboardButton('/help', callback_data="1-doc-help")
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
        return keyboard_markup

    @aux.log_actions
    @aux.log_errors
    def features(self, update: Update, context: CallbackContext):
        """Показать все возможности бота по запросу /features со справкой."""

        update.message.reply_text('Про какую из функций ты хочешь узнать?',

                                  reply_markup=self.features_set_keyboard())

    def features_handler(self, update: Update, context: CallbackContext, response):
        """Обработка нажатий кнопок в функции features"""

        try:
            # получаем из имени функции саму функцию, из нее - ее docstring
            # ловим возможные ошибки т.к. пользуемся eval
            func = eval("FantasticBot."+response[2])

            update.callback_query.message.reply_text("Узнать что-то ещё:", reply_markup=self.features_set_keyboard())
            update.callback_query.message.reply_text(f"Справка для функции: /{response[2]}")
            update.callback_query.message.reply_text(func.__doc__)

        except Exception as err_code:  # широкий except т.к. неизвестно, что может пойти не так
            update.callback_query.message.reply_text(f'Упс! \n {str(err_code)}')
            update.callback_query.message.reply_text(f"{response[2]}: docstring функции недоступен")

    def history_handler(self, update: Update, context: CallbackContext):
        """Обработка нажатий кнопок в функции history"""
        try:
            filename = update.callback_query.data.split('-')[2]  # filename
            message = self.get_log(filename, update=update)

            if message:
                filename = filename[0:-4] + '_short.txt'
                with open(filename, 'tw', encoding='utf-8') as log:
                    log.writelines(message)

                update.callback_query.message.reply_text(message)
                update.callback_query.message.reply_text(f'И ещё лови свой лог файлом.')
                self.bot.send_document(chat_id=update.effective_chat.id, document=open(filename, 'rb'))

        except Exception as err_code:
            update.callback_query.message.reply_text("Упс! Ошибка при обработке нажатия кнопок!")
            update.callback_query.message.reply_text(str(err_code))

    def change_history_size_handler(self, update: Update, context: CallbackContext, response):
        """Обработка нажатий кнопок в функции change_history_size"""
        self.h_size = int(response[2])
        update.callback_query.message.reply_text(f'Окей, пусть будет {self.h_size}.')

    def callback_worker(self, update: Update, context: CallbackContext):
        """Обработка запросов, полученных с клавиатуры"""
        try:
            response = update.callback_query.data.split('-', 3)
            # формат строки callback_query.data для моих клавиатур:
            # <номер кнопки>-<id>-<данные для работы функции>-<название файла, если есть>
            if response[1] == "doc":
                self.features_handler(update, context, response)
            elif response[1] == "history":
                self.history_handler(update, context)
            elif response[1] == "ch_hist_size":
                self.change_history_size_handler(update, context, response)
            elif response[1] == "covid":
                filename = response[3]
                if response[2] == 'world':
                    self.covid_world_handler(update, context, filename)
                elif response[2] == 'china':
                    self.covid_china_handler(update, context, filename)

        except Exception as err_code:
            update.callback_query.message.reply_text("Упс! Ошибка при обработке нажатия кнопок!")
            update.callback_query.message.reply_text(str(err_code))

    # </ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ, КЛАВИАТУРЫ>
    # ----------------------------------------------------------
    # <СТАНДАРТНЫЕ ФУНКЦИИ БОТА>

    @staticmethod
    @aux.cleaner
    @aux.log_actions
    @aux.log_errors
    def start(update: Update, context: CallbackContext):
        """Выкинуть мусор и отправить приветственное сообщение по запросу /start."""
        update.message.reply_text(f'Привет, {update.effective_user.first_name}!')

    @staticmethod
    @aux.log_actions
    @aux.log_errors
    def help(update: Update, context: CallbackContext):
        """Помочь пользователю по запросу /help."""
        update.message.reply_text('Введи команду /start для начала. \n'
                                  'Команда /features - мои возможности.')

    @staticmethod
    def echo(update: Update, context: CallbackContext):
        """Эхо сообщения собеседника, отправляется по умолчанию."""
        update.message.reply_text(update.message.text)

    def error(self, update: Update, context: CallbackContext):
        """Log Errors caused by Updates."""
        self.logger.warning(f'Update {update} caused error {context.error}')

    def run_bot(self):
        # Define a few command handlers. These usually take the two arguments: update and
        # context. Error handlers also receive the raised TelegramError object in error.

        # (time, user, function, message/error, \n)

        # on different commands - answer in Telegram
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.help))

        # <FEATURES FROM FANTASTIC SIX>
        self.updater.dispatcher.add_handler(CommandHandler('features', self.features))
        self.updater.dispatcher.add_handler(CommandHandler('history', self.history))
        self.updater.dispatcher.add_handler(CommandHandler('history_size', self.history_size))
        self.updater.dispatcher.add_handler(CommandHandler('change_history_size', self.change_history_size))
        self.updater.dispatcher.add_handler(CommandHandler('ping_intel', self.ping_intel))
        self.updater.dispatcher.add_handler(CommandHandler('git_pic', self.git_pic))
        self.updater.dispatcher.add_handler(CommandHandler('cat_facts_best', self.cat_facts_best))
        self.updater.dispatcher.add_handler(CommandHandler('cat_facts_random', self.cat_facts_random))
        self.updater.dispatcher.add_handler(CommandHandler('corono_stats', self.corono_stats))

        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.callback_worker))
        # </FEATURES FROM FANTASTIC SIX>

        # on noncommand i.e message - echo the message on Telegram
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.echo))

        # log all errors
        self.updater.dispatcher.add_error_handler(self.error)

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()



