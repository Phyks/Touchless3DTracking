#!/usr/bin/env python3

import wave
import math
import pyaudio

NomFichier = "temp"
Monson = wave.open(NomFichier, 'w')

channels = 1  # Mono
sample_size = 1  # Size of a sample -> 8 bits
sampling_freq = 44100  # Sampling frequency

freq = 440  # Note frequency
length = 5  # Length of the note in seconds
level = 150  # Between 0 (max < 0) and 255 (max > 0), 0 is 127

sample_number = int(length*sampling_freq)

parameters = (channels, sample_size, sampling_freq, sample_number, 'NONE',
              'not compressed')

Monson.setparams(parameters)  # File header

for i in range(0, sample_number):
    value = int(128.0+level*math.sin(2.0*math.pi*freq*i/sampling_freq))
    wave.struct.pack('h', value)

    Monson.close()

wf = open(NomFichier, 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                               channels=wf.getnchannels(),
                               rate=wf.getframerate(),
                               output=True)

data = wf.readframes(CHUNK)

while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()
            
p.terminate()
