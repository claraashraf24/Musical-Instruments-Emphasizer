import numpy as np 
from numpy.fft import fft, ifft
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os
import sys  
import wave, sys
from scipy.io import wavfile
import scipy
condition=0 

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
        self.pause_button.clicked.connect(self.pause)
        self.play_button.clicked.connect(self.replay) 
        self.equalize_button.clicked.connect(self.equalizee)
        self.sliders = [self.instrument1_slider,self.instrument2_slider,self.instrument3_slider]
        for i in range(len(self.sliders)):
            self.sliders[i].setOrientation(QtCore.Qt.Horizontal)
            self.sliders[i].setMinimum(0)
            self.sliders[i].setMaximum(10)
            self.sliders[i].setValue(1)
            self.sliders[i].setTickInterval(1)
            self.sliders[i].setSingleStep(1)
            self.sliders[i].setTickPosition(QSlider.TicksBelow)
            #self.sliders[i].setObjectName(self.sliders_names[i])

    
    def equalizee(self):
        global condition
        condition=1
        full_file_path = os.path.join(os.getcwd(), 'test.wav')
        # [bass , piano--- , altoSaxophone--- , guitar--- , flute, bell]
        freq_min = [0, 1000, 250]
        freq_max = [800, 2000, 900]
        # freq_min = [0, 1000, 250, 2000, 262, 73]
        # freq_max = [800, 2000, 900, 15000, 2092, 1172]


        Gains = []
        Gains.append(self.instrument1_slider.value())
        Gains.append(self.instrument2_slider.value())
        Gains.append(self.instrument3_slider.value())
      
        
        self.fs, self.data = wavfile.read(full_file_path)
        self.data = self.data / 2.0 ** 15
        N = len(self.data)

        rfft_coeff = np.fft.rfft(self.data)
        frequencies = np.fft.rfftfreq(N, 1. / self.fs)

        for i in range(3):
            for j in range(len(frequencies)):
                if frequencies[j] >= freq_min[i] and frequencies[j] <= freq_max[i]:
                    rfft_coeff[j] = rfft_coeff[j] * Gains[i]

        Equalized_signal = np.fft.irfft(rfft_coeff)
        scipy.io.wavfile.write('new.wav', self.fs, Equalized_signal)
        #self.media.stop()
        self.timer.stop()
        self.play_sound('new.wav')        
        
    def play_sound(self):
        full_file_path = os.path.join(os.getcwd(), 'test.wav')
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
        self.timer.start()
    
    def pause(self):
        self.player.pause()
        self.timer.stop()
    
    def replay(self):
        self.player.play()
        self.timer.start(500)
        
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

