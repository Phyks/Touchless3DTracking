#!/usr/bin/env python3

# ============================================================================
# This script allows you to play music using a chorizo (or whatever food you
# like) keyboard ! See README for more info and links.

# As all the other scripts in this repository, I release it under a very
# permissive license. To make a long story short : do whatever you want with
# this script (but try to have fun :), I don't mind. It would be cool to quote
# the origin of the script if you reuse it, but you don't have to. I'd like to
# be noticed of what you did cool with it (if you think it's worth). :)
# Ah, I almost forgot : If by chance we ever meet and you think this script is
# worth, you can buy me a soda :)
#
#                                                                   Phyks
# =============================================================================

# TODO

import wave
import math
import pyaudio
import sys


# Params
# ======
nChannels = 1  # Mono
sample_size = 2  # Size of a sample -> 1 = 8 bits
framerate = 44100  # Sampling frequency
length = 2  # Length in seconds
frequency = 440
level = 1
# =====

if level < 0.0 or level > 1.0:
    sys.exit(1)

filename = "temp"
w = wave.open(filename, 'w')

# Computed params
nFrames = int(length*framerate)
max_amplitude = int(2**(sample_size * 8 - 1) - 1)
amplitude = max_amplitude*level

w.setparams((nChannels, sample_size, framerate, nFrames,
             'NONE', 'not compressed'))

sine_wave = []
for i in range(min(framerate, nFrames)):
    sine_wave.append(int(max_amplitude +
                         amplitude*math.sin(2*math.pi*frequency*i/framerate)))

for i in range(nFrames):
    sine_wave = int(amplitude*math.sin(2*math.pi*frequency*i/framerate))
    data = wave.struct.pack('h', sine_wave)
    # ^ h is for "short" so each value can go from -2**15 to 2**15
    w.writeframesraw(data)

w.close()
