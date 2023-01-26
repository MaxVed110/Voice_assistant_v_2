from commander import *

from PyQt5 import QtWidgets, QtCore, QtGui
import form_ui

import threading

work = True


# Основной класс
class Assistant(QtWidgets.QMainWindow, form_ui.Ui_MainWindow, threading.Thread):

    def __init__(self):
        super(Assistant, self).__init__()
        self.setupUi(self)
        self.microphone = Microphone()
        ##
        self.pushButton.pressed.connect(self.start_thread_assistant)

    # Рабочий цикл
    def run_assistant(self):
        phrase_assis = QtWidgets.QListWidgetItem()
        phrase_assis.setTextAlignment(QtCore.Qt.AlignLeft)
        phrase_assis.setText('Максон: \nПривет, я Максон, что хотели?')
        answer_function('Привет, я Максон, что хотели?')
        n = 0
        global work
        work = True
        while work:
            n += 1
            print(f'цикл {n}')
            phrase = self.microphone.listen_command()
            phrase_us = QtWidgets.QListWidgetItem()
            phrase_us.setTextAlignment(QtCore.Qt.AlignRight)
            phrase_us.setText(f'Я: \n  {phrase}')
            self.listWidget.addItem(phrase_us)
            for key in list_commands['commands'].keys():
                if phrase in key:
                    answer = list_commands['commands'][key]()
                    phrase_assis.setText(f'Максон: \n{answer}')
                    continue
                else:
                    print('Повтори фразу')
                    continue

    def start_thread_assistant(self):
        thread_one = threading.Thread(target=self.run_assistant, args=())
        thread_one.start()

    def off_assistant(self):
        global work
        work = False



