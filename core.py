from commander import *

from PyQt5 import QtWidgets, QtCore
import form_two_t

import threading


# Основной класс
class Assistant(QtWidgets.QMainWindow, form_two_t.Ui_MainWindow, threading.Thread):

    def __init__(self):
        super(Assistant, self).__init__()
        self.setupUi(self)
        self.microphone = Microphone()
        self.work = True
        ##
        self.pushButton.pressed.connect(self.start_thread_assistant)
        self.pushButton_2.pressed.connect(self.off_assistant)
        self.not_result = True

    # Рабочий цикл
    def run_assistant(self):
        self.output_answer('Привет, я Максон, что хотели?')
        answer_function('Привет, я Максон, что хотели?')
        n = 0
        while self.work:
            n += 1
            print(f'цикл {n}')
            phrase = self.microphone.listen_command(False)
            phrase_us = QtWidgets.QListWidgetItem()
            phrase_us.setTextAlignment(QtCore.Qt.AlignRight)
            phrase_us.setText(f'Я: \n  {phrase}')
            self.listWidget.addItem(phrase_us)
            for word in phrase:
                for key in list_commands['commands'].keys():
                    if word in key:
                        answer = list_commands['commands'][key](phrase)
                        self.output_answer(answer)
                        self.not_result = False
                        break
            if self.not_result:
                self.output_answer('Я пока не понимаю такой команды')

    def output_answer(self, answer):
        phrase_assis = QtWidgets.QListWidgetItem()
        phrase_assis.setTextAlignment(QtCore.Qt.AlignLeft)
        phrase_assis.setText(f'Максон: \n {answer}')
        self.listWidget.addItem(phrase_assis)

    def start_thread_assistant(self):
        self.work = True
        thread_one = threading.Thread(target=self.run_assistant, args=())
        thread_one.start()

    def off_assistant(self):
        self.work = False
