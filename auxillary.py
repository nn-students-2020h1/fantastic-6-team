"""Additional functions for comfortable usage of bot"""
# работа с файлами
from os import path, remove
# системное время для логов
from datetime import datetime
# корректный вывод docstring'ов для задекорированных команд
from functools import wraps

from telegram import Update

# ----------------------------------------------------------
# <LESSON 3. ИСКЛЮЧЕНИЯ, ДЕКОРАТОРЫ>


def log_errors(func_to_decorate):
    """Логирование ошибок в файл."""
    @wraps(func_to_decorate)  # сохраняем для декоратора
    # docstring оборачиваемой функции (нужно для /features)
    def wrapper(*args, **kwargs):
        update = args[0]
        if not isinstance(update, Update):
            update = args[1]
        try:
            # проверяем функцию и пытаемся запустить
            if not update:
                raise UpdateError("Impossible to get update!")
            if not hasattr(update, 'effective_user'):
                raise UpdateError(f"Incorrect update format!")
            return func_to_decorate(*args, **kwargs)
        except Exception as err_code:
            # если не работает - логи в файл
            now = datetime.now()
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
        if not isinstance(update, Update):
            update = args[1]
        if update and hasattr(update, 'message') and hasattr(update, 'effective_user'):
            # пытаемся открыть файл
            try:
                log_file = open('log_actions.txt', 'r')
            except IOError:
                # не открывается -> файла нет -> создаем
                with open('log_actions.txt', 'tw', encoding='utf-8'):
                    pass

            now = datetime.now()
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

# </LESSON 3. ИСКЛЮЧЕНИЯ, ДЕКОРАТОРЫ>
# ----------------------------------------------------------
# <Вспомогательные функции и классы>


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


def rip(file):
    """Удаление в три буквы для ленивых"""
    if path.exists(file):
        remove(file)


class UpdateError(Exception):
    """Класс исключений с удобным комментарием"""
    def __init__(self, text):
        self.txt = text
