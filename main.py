import numpy as np 
from numpy.fft import fft, ifft
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os
import sys  
import wave, sys

ptr=0

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        #Load the UI Page
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('task3.ui', self)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.player = QMediaPlayer() # initializer
        self.action_open_2.triggered.connect(self.play_sound)
        self.timer.timeout.connect(self.signal_plot)
        # self.pause_button.clicked.connect(self.pause)
        # self.play_button.clicked.connect(self.play)
        
    def play_sound(self):
        full_file_path = os.path.join(os.getcwd(), 'test.wav')
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
        self.timer.start()

    def signal_plot(self):
        global ptr
        spf = wave.open("test.wav", "r")
        # Extract Raw Audio from Wav File
        signal = spf.readframes(-1)
        signal = np.frombuffer(signal, "int16")
        fs = spf.getframerate()
        time = np.linspace(0, len(signal) / fs, num=len(signal))
        
        self.mainsignal_widget.setYRange(min(signal),max(signal))
        self.mainsignal_widget.setXRange(0 + ptr, 1 + ptr)
        self.mainsignal_widget.plot(time, signal)
        ptr+=0.5

               
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())

