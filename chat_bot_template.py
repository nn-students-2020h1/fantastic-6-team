#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging

from setup import PROXY, TOKEN
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

#Декоратор для подсчета и записи в файл
def log_action(function):
    def inner(*args, **kwargs):
        update = args[0]

        if update and hasattr(update, 'message') and hasattr(update, 'effective_user'):
            LOG_ACTIONS = open('command.txt', 'r')
            string = LOG_ACTIONS.readlines()
            if len(string) > 4:
                string.pop(0)
            string.append(f'{update.effective_user.first_name},{ function.__name__},{update.message.text}\n')
            LOG_ACTIONS.close()
            LOG_ACTIONS = open('command.txt', 'w')
            LOG_ACTIONS.writelines(string)
            LOG_ACTIONS.close()
        return function(*args, **kwargs)
    return inner




@log_action
def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Привет, {update.effective_user.first_name}!')


@log_action
def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('понимаю.')
@log_action
#Функция вывода истории сообщений
def history(update: Update, context: CallbackContext):
    LOG_ACTIONS = open('command.txt', 'r')
    strings = LOG_ACTIONS.readlines()
    count=len(strings)
    message=f'This last {count} action:\n'
    for i in range(count):
        string=strings[i].split(",")
        message+=f'user:{string[0]}\n' \
                 f'function:{string[1]}\n' \
                 f'message:{string[2]}\n'

    update.message.reply_text(f'{message}\n')


@log_action
def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    #update.message.reply_text(update.message.text)
    if  update.message.text=="Понимаю":
        update.message.reply_text("Получается ты гений")
    else:
        update.message.reply_text("Получается я гений")




def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


def main():
    bot = Bot(
        token=TOKEN,
        base_url=PROXY,  # delete it if connection via VPN
    )
    updater = Updater(bot=bot, use_context=True)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))
    updater.dispatcher.add_handler(CommandHandler('history', history))

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
