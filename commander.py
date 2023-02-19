import os
import tkinter as tk
import webbrowser
import pyttsx3

from random import choice
from tkinter.filedialog import askdirectory
from serpapi import GoogleSearch
from microphone import Microphone

microphone = Microphone()


# Озвучивание ответов помощника
def answer_function(text: str):
    answer = pyttsx3.init(debug=True)
    answer.say(text)
    answer.runAndWait()
    answer.stop()


# Приветствие
def greeting():
    answer_function('Приветствую, что хотели?')
    return 'Приветствую, что хотели?'


# Перезагрузка/выключение ПК
def shutdown_reboot_pc(value: str):
    commander_s = ['выключи', 'выруби', 'отключи']
    commander_r = ['перезагрузка', 'перезагрузи', 'ребут']
    if any(x in value for x in commander_s):
        text = 'Выключение через 3 секунды'
        answer_function(text)
        os.system('shutdown /s /t 3')
        return text
    if any(x in value for x in commander_r):
        text = 'Перезагрузка через 3 секунды'
        answer_function(text)
        os.system('shutdown /r /t 3')
        return text


# Создать новый список дел или добавить запись (записная книжка)
def create_todo_list():
    answer_function('Что добавим в список дел?')
    phrase = microphone.listen_command(parameter=True)
    if os.path.exists('To_Do_list.txt'):
        x = 'w'
    else:
        x = 'a'
    with open('To_Do_list.txt', x) as file:
        file.write(f'{phrase}\n')
    answer_function(f'Задача {phrase} записана в список дел')
    return "Выполнено"


# Показать список дел
def view_todo_list():
    answer_function('Показываю список дел')
    if os.path.exists('To_Do_list.txt'):
        with open('To_Do_list.txt') as file:
            for line in file:
                return line
    else:
        return 'Список дел пуст'


# Запуск музыки
def play_sound():
    answer_function('Музыка так музыка')
    if list_commands['directory'] == '0':
        window = tk.Tk()
        intro = tk.Label(text="Выберите папку с музыкой\n(для продолжения закройте это окно)",
                         width=40, height=4, font='Times 20')
        intro.pack()
        window.mainloop()
        folderlocation = askdirectory()
        list_commands['directory'] = folderlocation

    files = os.listdir(list_commands['directory'])
    if len(files) != 0:
        random_file = f'{choice(files)}'
        answer_function(f'Колбасимся под {random_file.split("/")[-1]}')
        os.startfile(fr"C:\Users\Максим\Desktop\Music\{random_file}")
        return f'Слушаем {random_file.split("/")[-1]}'
    else:
        text = 'Музыки по адресу нет'
        answer_function(text)
        return text


# Поиск в интернете и выдача первой ссылки
def internet_search():
    answer_function('Что хотите найти?')
    phrase = microphone.listen_command(parameter=True)
    parameter = {
        "engine": "yandex",
        "text": phrase,
        "api_key": "1a15ef08c83fb7bba62201558cd28c125d1eccab2a77a808e84ed7aa55f20d3f"
    }
    try:
        search = GoogleSearch(parameter)
        dict_results = search.get_dict()
        list_res = [dict_results['organic_results'][0]['link'], dict_results['organic_results'][0]['snippet']]

        # ToDo, посмотреть выдачу (правильность)
        # print(dict_results['organic_results'][0]['link'])
        # print(dict_results['organic_results'][0]['snippet'])

        answer_function(dict_results['organic_results'][0]['snippet'])
        return f'{list_res[0]} \n{list_res[1]}'
    except FileNotFoundError:
        text = 'Такого браузера нет. Пожалуйста, скачайте его или переместите в другую директорию (PFx86)'
        answer_function(text)
        return text


# Открывание ссылок
def open_internet_search():
    answer_function('Какую ссылку открыть?')
    phrase = microphone.listen_command(parameter=True)
    parameter = {
        "engine": "yandex",
        "text": phrase,
        "api_key": "1a15ef08c83fb7bba62201558cd28c125d1eccab2a77a808e84ed7aa55f20d3f"
    }
    try:
        search = GoogleSearch(parameter)
        dict_results = search.get_dict()
        webbrowser.register('YandexBrowser', None,
                            webbrowser.BackgroundBrowser(
                                r'C:\Program Files (x86)\Yandex\YandexBrowser\Application\browser.exe'))
        webbrowser.get('YandexBrowser').open_new_tab(dict_results['organic_results'][0]['link'])
        return 'Открыто'
    except FileNotFoundError:
        text = 'Такого браузера нет. Пожалуйста, скачайте его или переместите в другую директорию (PFx86)'
        answer_function(text)
        return text


# Открытие приложений
def opener_application(text):
    def opener(path: str, name: str):
        try:
            os.startfile(path)
            answer_function(f'Открываю {name}')
        except FileNotFoundError:
            text_ans = 'В стандартизированной директории приложение не найдено'
            answer_function(text_ans)
            return text_ans

    # Открыть браузер (Яндекс по умолчанию)
    def open_browser():
        answer_function('Открываю Яндекс')
        try:
            files = r'C:\Program Files (x86)\Yandex\YandexBrowser\Application\browser.exe'
            os.startfile(files)
        except FileNotFoundError:
            text_ans = 'Такого браузера нет. Пожалуйста, скачайте его или переместите в другую директорию (PFx86)'
            answer_function(text_ans)
            return text_ans

    programs = {
        'дискорд': r'C:\Users\Максим\AppData\Local\Discord\Update.exe',
        'телеграм': r'C:\Users\Максим\AppData\Roaming\Telegram Desktop\Telegram.exe',
        'калькулятор': 'calc',
        'ножницы': 'snippingtool'
    }

    for word in text:
        if word in programs.keys():
            opener(programs[word], word)
        if word in ['браузер', 'интернет']:
            open_browser()


# Список команд
list_commands = {
    'commands': {
        ('привет', 'максон', 'эй'): greeting,
        ('добавить', 'задача', 'дело'): create_todo_list,
        ('посмотреть', 'список', 'список', 'дел'): view_todo_list,
        ('включи', 'музыку', 'музон', 'музыка'): play_sound,
        ('поиск', 'найди'): internet_search,
        ('выключи', 'перезагрузи', 'выруби', 'отключи', 'перезагрузка', 'ребут'): shutdown_reboot_pc,
        ('открой', 'перейди', 'покажи', 'открой ссылку'): open_internet_search
    },
    'directory': '0'
}
