from time import time
import numpy as np 
from numpy.fft import fft, ifft
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import QUrl,QThreadPool,pyqtSlot,QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os
import sys  
import wave, sys
from scipy.io import wavfile
import scipy
import vlc 
condition=0 


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        #Load the UI Page
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('task3.ui', self)
        self.thread_manager = QThreadPool()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.player = QMediaPlayer() # initializer
        self.signal = []
        self.time = []
        self.fs = 0
        self.ptr=0
        self.action_open_2.triggered.connect(lambda:self.open_audio_file())
        self.timer.timeout.connect(self.signal_plot)
        self.pause_button.clicked.connect(self.pause)
        self.play_button.clicked.connect(self.play) 
        # self.equalize_button.clicked.connect(self.equalizee)
        self.equalize_button.clicked.connect(self.equalizee)
        
       
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(200)
        self.volume_slider.setValue(100)
        self.volume_slider.setTickInterval(20)
        self.volume_slider.setSingleStep(20)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        self.volume_slider.valueChanged.connect( self.adjust_volume)
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

    def adjust_volume(self):
        value = int(self.volume_slider.value())
        self.media.audio_set_volume(value)
    def equalizee(self):
        self.timer.start()
        # [bass , piano--- , altoSaxophone--- , guitar--- , flute, bell]
        freq_min = [0, 1000, 250]
        freq_max = [800, 2000, 900]
        # freq_min = [0, 1000, 250, 2000, 262, 73]
        # freq_max = [800, 2000, 900, 15000, 2092, 1172]


        Gains = []
        Gains.append(self.instrument1_slider.value())
        Gains.append(self.instrument2_slider.value())
        Gains.append(self.instrument3_slider.value())
      
        
        self.fs, self.data = wavfile.read(self.full_file_path)
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
        self.media.stop()
        self.playAudioFile('new.wav') 
        
      
    def open_audio_file(self):
        self.timer.start()
        self.full_file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Open Song', QtCore.QDir.rootPath(), 'wav(*.wav)')
        self.playAudioFile(self.full_file_path)
        spf = wave.open(self.full_file_path, "r")
        self.signal = spf.readframes(-1)
        self.signal = np.frombuffer(self.signal, "int16")
        self.fs = spf.getframerate()
        self.time = np.linspace(0, len(self.signal) / self.fs, num=len(self.signal))
    
           

    def playAudioFile(self, full_file_path):
        #self.pushButton_play.setText("Pause")
        
        self.media = vlc.MediaPlayer(full_file_path)
        self.media.play()

        self.fs, self.data = wavfile.read(full_file_path)  
       
    def play(self):
        self.media.play()
        self.timer.start()
    
    def pause(self):
        self.media.pause()
        self.timer.stop()
    
      
    def signal_plot(self):
        fs = self.fs
        interval = int((fs/2))
        print(interval)
        

        # Extract Raw Audio from Wav File
        self.spf = wave.open(self.full_file_path, "r")
        self.mainsignal_widget.setYRange(min(self.signal),max(self.signal))
        self.mainsignal_widget.setXRange(self.time[self.ptr],self.time[self.ptr+interval] )
        self.mainsignal_widget.plot(self.time[self.ptr:self.ptr+interval], self.signal[self.ptr:self.ptr+interval])
        self.ptr+=interval
        print(self.time[self.ptr])



        

               
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())

