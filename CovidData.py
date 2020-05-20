"""Class for COVID data processing"""

from datetime import datetime, timedelta  # удобные операции со временем
from datetime import date
from requests import get as r_get
from copy import copy
from csv import DictReader, DictWriter
from os import path, remove


class CovidData:
    """Realizes operations with data tables about COVID-19
    One instance = one date and all information about this date"""

    STOP_YEAR = 2019  # до какого года листать базу если не можем получить файл
    COVID_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/' \
                'master/csse_covid_19_data/csse_covid_19_daily_reports/'
    CACHE = []  # список имен сохраненных таблиц

    # ----------------------------------------------------------
    # МАГИЧЕСКИЕ МЕТОДЫ
    # ----------------------------------------------------------

    def __init__(self):
        pass  # статический класс

    # ----------------------------------------------------------
    # МЕТОДЫ ДЛЯ ПОЛУЧЕНИЯ И УДАЛЕНИЯ ФАЙЛОВ
    # ----------------------------------------------------------

    @staticmethod
    def find_latest():
        date_obj = datetime.today()  # type: date
        existing_data_filename = CovidData.get_data_file(CovidData.date_to_filename(date_obj))  # type: str
        if not existing_data_filename:
            try:
                existing_data_filename = CovidData.search_back(date_obj)  # type: str or Exception
            except FileNotFoundError:
                return None
        return existing_data_filename  # type: str or None

    @staticmethod
    def remove_data_file(filename: str):
        """Удаление из системы данных"""
        if path.exists(filename):
            remove(filename)
        CovidData.CACHE.remove(filename)
        print(filename)

    @staticmethod
    def remove_all_data():
        """Удаление из системы данных"""
        for i in CovidData.CACHE:  # type: str
            CovidData.remove_data_file(i)

    # ----------------------------------------------------------
    # МЕТОДЫ ДЛЯ ПОЛУЧЕНИЯ РАЗЛИЧНЫХ ДАННЫХ ПО COVID-19 ИЗ ФАЙЛОВ
    # ----------------------------------------------------------

    @staticmethod
    def basic_world_stats(filename: str):
        with open(filename, 'r') as file:
            reader = DictReader(file)
            infected = 0  # type: int
            dead = 0  # type: int
            for row in reader:
                infected += (int(row['Confirmed']))
                dead += (int(row['Deaths']))
            stats = {"infected": infected, "dead": dead}
            return stats  # type: dict

    @staticmethod
    def country_data_agregator(countryname, database_in, database_out=None):
        """Получить из <database_in> таблицу co значениями из <header> и записать в <database_out>"""
        if not database_out:
            database_out = countryname + "_data.csv"
            CovidData.CACHE.append(database_out)
        notes = []
        with open(database_in, 'r') as file:
            reader = DictReader(file)
            try:  # пытаемся искать записи в новом формате
                for row in reader:
                    if row['Country_Region'].find(countryname) != -1:
                        notes.append(row)
            except KeyError:  # не нашли: пытаемся искать в старом формате
                for row in reader:
                    if row['Country/Region'].find(countryname) != -1:
                        notes.append(row)

        with open(database_out, 'w', newline='') as csvfile:
            header = ['Province', 'Last Update', 'Current Cases']
            writer = DictWriter(csvfile, fieldnames=header)
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

    @staticmethod
    def agregated_data_comparison(database_curr, database_prev, number=None):
        """Получить из <database_out> предыдущей функции динамику по провинциям"""
        # читаем свежую статистику по провинциям
        notes = []
        with open(database_curr, 'r') as csvfile:
            notes = list(DictReader(csvfile))

        # записываем зараженные на данный момент провинции, порядок как в notes
        infected_provinces = [i['Province'] for i in notes]

        # читаем статистику по провинциям из прошлого файла
        with open(database_prev, 'r') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                # для каждой строчки проверяем, не заражена ли сейчас провинция
                # итерируемся именно по её номеру в списке notes
                for number in range(len(infected_provinces)+1):
                    if row['Province'] == infected_provinces[number]:
                        # если заражена - по номеру в списке получаем число больных
                        # и находим, на сколько оно изменилось с прошлого файла
                        notes[number]['Current Cases'] = int(notes[number]['Current Cases']) \
                                                         - int(row['Current Cases'])
                        break

        notes.sort(key=lambda d: int(d['Current Cases']), reverse=True)

        if not number:
            number = len(notes)
        message = ''
        for data, counter in zip(notes, range(number+1)):
            if int(data['Current Cases']) < 0:
                new = f"число зараженных сократилось на {-1*data['Current Cases']}."
            elif int(data['Current Cases']) == 0:
                new = f"без изменений."
            else:
                new = f"зафиксировано {data['Current Cases']} новых заражённых."

            if data['Province']:
                province = f"{data['Province']}"
            else:
                province = "<регион не указан>"

            message += f"{province} - {new}\n"

        stats = {"mesg": message, "amount": len(notes)}
        return stats  # type: dict

    # ----------------------------------------------------------
    # ОБЩИЕ МЕТОДЫ
    # ----------------------------------------------------------

    @staticmethod
    def date_to_filename(date_obj):
        """Конвертируем дату в имя файла"""
        return date_obj.strftime("%m-%d-%Y.csv")

    @staticmethod
    def filename_to_date(filename):
        """Собираем из названия файла правильную дату"""
        values = filename[:10].split('-')
        # datetime.date имеет вид year, month, day
        date_obj = date(int(values[2]), int(values[0]), int(values[1]))
        return date_obj  # type: date

    @staticmethod
    def get_data_file(filename):
        """Получение данных в систему через API"""
        url = CovidData.COVID_URL + filename
        r = r_get(url)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)
            CovidData.CACHE.append(filename)
            return filename  # type: str
        else:
            return None

    @staticmethod
    def search_back(date_obj):
        """Поиск на сайте файла с данными, начиная с даты,
        предшествующей <date>, пока не найдем или не достигнем <stop_year>"""
        date_obj = copy(date_obj)
        while True:
            date_obj = date_obj - timedelta(1)  # type: date
            if date_obj.year == CovidData.STOP_YEAR:
                raise FileNotFoundError
            existing_data_file = CovidData.get_data_file(CovidData.date_to_filename(date_obj))
            if existing_data_file:  # type: str or None
                return existing_data_file  # type: str

    @staticmethod
    def step_back(date_obj):
        """Поиск на сайте файла с данными за день, предшествовавший <date>"""
        date_obj = copy(date_obj)  # type: date
        date_obj = date_obj - timedelta(1)
        if date_obj.year == CovidData.STOP_YEAR:
            raise FileNotFoundError
        existing_data_file = CovidData.get_data_file(CovidData.date_to_filename(date_obj))
        if existing_data_file:  # type: str or None
            return existing_data_file  # type: str
        else:
            raise FileNotFoundError
