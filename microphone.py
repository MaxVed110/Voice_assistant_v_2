import speech_recognition


class Microphone:

    # Инициализация объекта для прослушивания
    def __init__(self):
        self.sr = speech_recognition.Recognizer()
        self.sr.pause_threshold = 1  # ToDo
        self.sr.energy_threshold = 1000

    # Функция для прослушивания микрофона
    def listen_command(self, parameter: True):
        with speech_recognition.Microphone() as micro:
            self.sr.adjust_for_ambient_noise(source=micro, duration=0.5)
            print('Можно говорить')
            audio = self.sr.listen(source=micro, timeout=5, phrase_time_limit=5)  # ToDo добавить задержку
            try:
                #  audio = sr.listen(source=micro)
                phrase = self.sr.recognize_google(audio_data=audio, language='ru-RU').lower()
                if parameter:
                    return phrase
                else:
                    return phrase.split(' ')
            except speech_recognition.UnknownValueError:
                print('Ошибка, повторите фразу')
