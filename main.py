from random import random
from time import time
from tkinter import OFF
import numpy as np 
from numpy.fft import fft, ifft
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QSlider, QLabel
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from pydub import AudioSegment
from pydub.playback import play
import os
import sys  
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from scipy import signal
import wave, sys
from scipy.io import wavfile
import scipy
import pyqtgraph as pg
import vlc 
piano_status= False
drums_status= False


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        #Load the UI Page
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('task3.ui', self)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.signal = []
        self.time = []
        self.fs = 0
        self.ptr=0
       
        self.selected_note= ''
        self.full_file_path = ""
        self.player = QMediaPlayer() # initializer
        self.action_open_2.triggered.connect(lambda:self.open_audio_file())
        self.timer.timeout.connect(self.signal_plot)
        self.pause_button.clicked.connect(self.pause)
        self.play_button.clicked.connect(self.play)
        self.equalize_button.clicked.connect(self.equalizee)
        self.piano_label.mousePressEvent  = self.piano
        self.drums_label.mousePressEvent = self.drums
        self.xylo_label.mousePressEvent = self.xylophone
        self.piano_filter.clicked.connect(self.piano_filters)
        self.drums_filter.clicked.connect(self.drums_filters)
        # self.piano.connect(self.playinstrument)
        # self.drums.connect(self.playinstrument)
        # self.xylophone.connect(self.playinstrument)
        #define slider widget
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.setTickInterval(10)
        self.volume_slider.setSingleStep(10)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        self.volume_slider.valueChanged.connect( self.adjust_volume)

        self.piano_slider.setMinimum(0)
        self.piano_slider.setMaximum(100)
        self.piano_slider.setValue(100)
        self.piano_slider.setTickInterval(10)
        self.piano_slider.setSingleStep(10)
        self.piano_slider.setTickPosition(QSlider.TicksBelow)
        self.piano_slider.valueChanged.connect( self.adjust_volume)
        self.piano_slider.valueChanged.connect( self.slider_text)

        self.xylo_slider.setMinimum(0)
        self.xylo_slider.setMaximum(100)
        self.xylo_slider.setValue(100)
        self.xylo_slider.setTickInterval(10)
        self.xylo_slider.setSingleStep(10)
        self.xylo_slider.setTickPosition(QSlider.TicksBelow)
        self.xylo_slider.valueChanged.connect( self.adjust_volume)
        self.xylo_slider.valueChanged.connect( self.slider_text)

        self.drums_slider.setMinimum(0)
        self.drums_slider.setMaximum(100)
        self.drums_slider.setValue(100)
        self.drums_slider.setTickInterval(10)
        self.drums_slider.setSingleStep(10)
        self.drums_slider.setTickPosition(QSlider.TicksBelow)
        self.drums_slider.valueChanged.connect( self.adjust_volume)
        self.drums_slider.valueChanged.connect( self.slider_text)


        self.volume_slider.valueChanged.connect( self.slider_text)
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
     
    def piano_filters(self):
         global piano_status
         piano_status=not piano_status
         


    def drums_filters(self):
        global drums_status
        drums_status=not drums_status

    def adjust_volume(self,sender):
        sender = self.sender()  # This is what you need
        value = int(sender.value())
        print(value)
        self.media.audio_set_volume(value)


    def slider_text(self, value):
        sender = self.sender()  # This is what you need
        if sender == self.volume_slider:
            self.volume_number.setText(str(value))
        elif sender == self.drums_slider:
            self.drums_slider_number.setText(str(value))
        elif sender == self.piano_slider:
            self.piano_volume_number.setText(str(value))
        else:
            self.xylo_volume_number.setText(str(value))

    # def change_volume_label(self):
    #     self.volume_number.setText(str(value)) 


    def xylophone(self, event):
         x= event.pos().x()
         y= event.pos().y()

         if x/self.xylo_label.size().width() > 0.05 and x/self.xylo_label.size().width() < 0.14 and y/self.xylo_label.size().width() > 0.15 and y/self.xylo_label.size().width() < 0.30 :
            print("Bar 1") 
            self.selected_note="Bar 1.wav"
            

         if x/self.xylo_label.size().width() > 0.16 and x/self.xylo_label.size().width() < 0.25 and y/self.xylo_label.size().width() > 0.13 and y/self.xylo_label.size().width() < 0.32 :
            print("Bar 2")
            self.selected_note="Bar 2.wav"

         if x/self.xylo_label.size().width() > 0.28 and x/self.xylo_label.size().width() < 0.37 and y/self.xylo_label.size().width() > 0.12 and y/self.xylo_label.size().width() < 0.33 :
            print("Bar 3")
            self.selected_note="Bar 3.wav"

         if x/self.xylo_label.size().width() > 0.40 and x/self.xylo_label.size().width() < 0.49 and y/self.xylo_label.size().width() > 0.1 and y/self.xylo_label.size().width() < 0.33 :
            print("Bar 4")
            self.selected_note="Bar 4.wav"

         if x/self.xylo_label.size().width() > 0.51 and x/self.xylo_label.size().width() < 0.60 and y/self.xylo_label.size().width() > 0.08 and y/self.xylo_label.size().width() < 0.36 :
            print("Bar 5")
            self.selected_note="Bar 5.wav"

         if x/self.xylo_label.size().width() > 0.63 and x/self.xylo_label.size().width() < 0.72 and y/self.xylo_label.size().width() > 0.05 and y/self.xylo_label.size().width() < 0.38 :
            print("Bar 6")
            self.selected_note="Bar 6.wav"

         if x/self.xylo_label.size().width() > 0.75 and x/self.xylo_label.size().width() < 0.84 and y/self.xylo_label.size().width() > 0.03 and y/self.xylo_label.size().width() < 0.4 :
            print("Bar 7")
            self.selected_note="Bar 7.wav"
        
         if x/self.xylo_label.size().width() > 0.86 and x/self.xylo_label.size().width() < 0.96 and y/self.xylo_label.size().width() > 0.2 and y/self.xylo_label.size().width() < 0.42 :
            print("Bar 8")
            self.selected_note="Bar 8.wav"
         self.playinstrument() 
         


        #  print(x)
        #  print(y)

    
    def drums(self, event):
        global drums_status
        x= event.pos().x()
        y= event.pos().y()
        if x/self.drums_label.size().width() > 0.027 and x/self.drums_label.size().width() < 0.26 and y/self.drums_label.size().width() > 0.009 and y/self.drums_label.size().width() < 0.07 :
            print("Ride Cymbal") 
            self.selected_note="Ride Cymbal.wav"

        if x/self.drums_label.size().width() > 0.733 and x/self.drums_label.size().width() < 1.00 and y/self.drums_label.size().width() > 0.03 and y/self.drums_label.size().width() < 0.10 :
            print("Hi-Hat Cymbal") 
            self.selected_note="Hi-Hat Cymbal.wav"

        if x/self.drums_label.size().width() > 0.53 and x/self.drums_label.size().width() < 0.69 and y/self.drums_label.size().width() > 0.10 and y/self.drums_label.size().width() < 0.25 :
            print("Medium Tom") 
            if drums_status==False:
                self.selected_note="Medium Tom.wav" 
            else :
                self.selected_note="Medium Tom_f.wav" 
            

        if x/self.drums_label.size().width() > 0.21 and x/self.drums_label.size().width() < 0.50 and y/self.drums_label.size().width() > 0.05 and y/self.drums_label.size().width() < 0.20 :
            print("High Tom")
            if drums_status== False:
                self.selected_note="High Tom.wav" 
            else :
                self.selected_note="High Tom_f.wav" 

        if x/self.drums_label.size().width() > 0.05 and x/self.drums_label.size().width() < 0.24 and y/self.drums_label.size().width() > 0.15 and y/self.drums_label.size().width() < 0.50 :
            print("Stand Tom") 
            self.selected_note="Stand Tom.wav"

        if x/self.drums_label.size().width() > 0.41 and x/self.drums_label.size().width() < 0.72 and y/self.drums_label.size().width() > 0.30 and y/self.drums_label.size().width() < 1.0 :
            print("Bass Drum") 
            if drums_status==False:
                self.selected_note="Bass Drum.wav" 
            else :
                self.selected_note="Bass Drum_f.wav" 
            print(self.selected_note)

        if x/self.drums_label.size().width() > 0.76 and x/self.drums_label.size().width() < 0.84 and y/self.drums_label.size().width() > 0.20 and y/self.drums_label.size().width() < 0.63 :
            print("Snare Drum") 
            self.selected_note="Snare Drum.wav"
        self.playinstrument() 
       

        # print(x)
        # print(y)
    

    def piano(self,event):
        global piano_status
        x = event.pos().x()
        y = event.pos().y() 

        if x/self.piano_label.size().width() > 0.15 and x/self.piano_label.size().width() < 0.20  and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 1") 
            if piano_status==False:
                self.selected_note="White Key 1.wav" 
            else:
                self.selected_note="White Key 1_f.wav" 

        if x/self.piano_label.size().width() > 0.20 and x/self.piano_label.size().width() < 0.25 and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 2")
            self.selected_note="White Key 2.wav"
            

        if x/self.piano_label.size().width() > 0.25 and x/self.piano_label.size().width() < 0.30 and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 3")
            self.selected_note="White Key 3.wav"

        if x/self.piano_label.size().width() > 0.30 and x/self.piano_label.size().width() < 0.35 and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 4")
            self.selected_note="White Key 4.wav"
            if piano_status==False:
                self.selected_note="White Key 4.wav" 
            else :
                self.selected_note="White Key 4_f.wav"
            print(self.selected_note) 

        if x/self.piano_label.size().width() > 0.35 and x/self.piano_label.size().width() < 0.40 and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 5")
            self.selected_note="White Key 5.wav"

        if x/self.piano_label.size().width() > 0.40 and x/self.piano_label.size().width() < 0.45 and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 6")
            self.selected_note="White Key 6.wav"

        if x/self.piano_label.size().width() > 0.45 and x/self.piano_label.size().width() < 0.50 and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 7")
            self.selected_note="White Key 7.wav"

        if x/self.piano_label.size().width() > 0.50 and x/self.piano_label.size().width() < 0.55 and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 8")
            self.selected_note="White Key 1.wav"

        if x/self.piano_label.size().width() > 0.55 and x/self.piano_label.size().width() < 0.60 and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 9")
            self.selected_note="White Key 2.wav"

        if x/self.piano_label.size().width() > 0.60 and x/self.piano_label.size().width() < 0.65 and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 10")
            self.selected_note="White Key 3.wav"

        if x/self.piano_label.size().width() > 0.65 and x/self.piano_label.size().width() < 0.70 and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 11")
            self.selected_note="White Key 4.wav"

        if x/self.piano_label.size().width() > 0.70 and x/self.piano_label.size().width() < 0.75 and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 12")
            self.selected_note="White Key 5.wav"

        if x/self.piano_label.size().width() > 0.75 and x/self.piano_label.size().width() < 0.80 and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 13")
            self.selected_note="White Key 6.wav"

        if x/self.piano_label.size().width() > 0.80 and x/self.piano_label.size().width() < 0.85 and y/self.piano_label.size().width() > 0.30 and y/self.piano_label.size().width() < 0.40 :
            print("White Key 14")
            self.selected_note="White Key 7.wav"

        if x/self.piano_label.size().width() > 0.18 and x/self.piano_label.size().width() < 0.22 and y/self.piano_label.size().width() > 0.10 and y/self.piano_label.size().width() < 0.29 :
            print("Black Key 1")
            self.selected_note="Black Key 1.wav"

        if x/self.piano_label.size().width() > 0.23 and x/self.piano_label.size().width() < 0.27 and y/self.piano_label.size().width() > 0.10 and y/self.piano_label.size().width() < 0.29 :
            print("Black Key 2")
            self.selected_note="Black Key 2.wav"

        if x/self.piano_label.size().width() > 0.34 and x/self.piano_label.size().width() < 0.37 and y/self.piano_label.size().width() > 0.10 and y/self.piano_label.size().width() < 0.29 :
            print("Black Key 3")
            self.selected_note="Black Key 3.wav"

        if x/self.piano_label.size().width() > 0.39 and x/self.piano_label.size().width() < 0.42 and y/self.piano_label.size().width() > 0.10 and y/self.piano_label.size().width() < 0.29 :
            print("Black Key 4")
            self.selected_note="Black Key 4.wav"

        if x/self.piano_label.size().width() > 0.44 and x/self.piano_label.size().width() < 0.47 and y/self.piano_label.size().width() > 0.10 and y/self.piano_label.size().width() < 0.29 :
            print("Black Key 5")
            self.selected_note="Black Key 5.wav"

        if x/self.piano_label.size().width() > 0.54 and x/self.piano_label.size().width() < 0.57 and y/self.piano_label.size().width() > 0.10 and y/self.piano_label.size().width() < 0.29 :
            print("Black Key 6")
            self.selected_note="Black Key 1.wav"

        if x/self.piano_label.size().width() > 0.59 and x/self.piano_label.size().width() < 0.62 and y/self.piano_label.size().width() > 0.10 and y/self.piano_label.size().width() < 0.29 :
            print("Black Key 7")
            self.selected_note="Black Key 2.wav"

        if x/self.piano_label.size().width() > 0.69 and x/self.piano_label.size().width() < 0.73 and y/self.piano_label.size().width() > 0.10 and y/self.piano_label.size().width() < 0.29 :
            print("Black Key 8")
            self.selected_note="Black Key 3.wav"

        if x/self.piano_label.size().width() > 0.74 and x/self.piano_label.size().width() < 0.78 and y/self.piano_label.size().width() > 0.10 and y/self.piano_label.size().width() < 0.29 :
            print("Black Key 9")
            self.selected_note="Black Key 4.wav"

        if x/self.piano_label.size().width() > 0.79 and x/self.piano_label.size().width() < 0.83 and y/self.piano_label.size().width() > 0.10 and y/self.piano_label.size().width() < 0.29 :
            print("Black Key 10")
            self.selected_note="Black Key 5.wav"
        self.playinstrument()
    
    def equalizee(self):
        self.timer.start()
       
        freq_min = [0, 1000, 250]
        freq_max = [800, 2000, 900] #gets max and min freq of 3 instruements drums, piano and xylo respectively 
      


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
        self.spectrogram('new.wav')     
      
    def open_audio_file(self):

        self.full_file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Open Song', QtCore.QDir.rootPath(), 'wav(*.wav)')
        self.playAudioFile(self.full_file_path)
        spf = wave.open(self.full_file_path, "r")
        self.signal = spf.readframes(-1) # gets signals
        self.signal = np.frombuffer(self.signal, "int16") 
        self.fs = spf.getframerate() 
        self.time = np.linspace(0, len(self.signal) / self.fs, num=len(self.signal)) 
        self.timer.start()
        self.spectrogram(self.full_file_path)
    
    def spectrogram(self,file_name):
        sample_rate, samples = wavfile.read(file_name)
        print(sample_rate)
        print(samples.flatten())
        SpectorgramFrequency, SpectorgramTime, Sxx = signal.spectrogram(samples.flatten(), sample_rate)
        self.spectrogram_widget.canvas.axes.pcolormesh(SpectorgramTime, SpectorgramFrequency, 10*np.log(Sxx))
        self.spectrogram_widget.canvas.draw()
        # self.Canvas.draw()       

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
        if(self.ptr+interval >= self.time.size):
            self.timer.stop()
        self.mainsignal_widget.setXRange(self.time[self.ptr],self.time[self.ptr+interval] )
        self.mainsignal_widget.plot(self.time[self.ptr:self.ptr+interval], self.signal[self.ptr:self.ptr+interval])
        self.ptr+=interval
        # print(self.time[self.ptr])

   
    
    def playinstrument(self):
         self.media = vlc.MediaPlayer(self.selected_note)
         self.media.play()



        # # for playing wav file
        # note = AudioSegment.from_wav(self.selected_note)
        # print('playing sound using  pydub')
        # play(note)

               
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())