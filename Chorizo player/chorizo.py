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

from sound4python import sound
from multiprocessing import Process
import math
import serial
import sys
import getopt


def play_wave(frequency=440, nb_secs=1):
    sine_wave = []
    for i in range(nb_secs*framerate):
        sine_wave.append(int(16384*math.sin(2*math.pi*frequency*i/framerate)))

    sound(sine_wave)

serial_port = "/dev/ttyACM0"

try:
    opts, args = getopt.getopt(sys.argv[1:], "hs:", ["help", "serial="])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Play music with chorizos !")
            print("\nUsage : "+sys.argv[0]+" [OPTIONS]")
            print("\nOptions :")
            print("\t-h (--help) \t display this help message")
            print("\t-s (--serial=) \t change serial port (default is " +
                  "/dev/tty/ACM0")
            sys.exit(0)
        elif opt in ("-s", "--serial"):
            serial_port = arg
except getopt.GetoptError:
    pass

try:
    ser = serial.Serial(serial_port, 115200)
except Exception as e:
    sys.exit("Error with serial port :"+str(e))

framerate = 16000
frequencies = [440, 600, 880]
gap_times = 10
p = []
for i in range(3):
    processes.append(Process(target=play_wave, args=(frequencies[i], 1)))
    processes[-1].start()

try:
    ser.open()
except Exception as e:
    sys.exit("Error while opening serial port : "+str(e))

if ser.isOpen():
    try:
        ser.flushInput()
        ser.flushOutput()

        measures = [[], [], []]

        print("Calibration :")
        print("Touch each chorizo electrodes before starting")

        for i in range(10000):
            line = ser.readline()
            line = line.decode().strip("\r\n")
            line = line.split(" ")
            line = [int(j or 0) for j in line]

            for j in range(3):
                measures[j][i] = line[j]


        # Get threshold
        threshold = [-1, -1, -1]
        for i in range(3):
            gap = -1
            for j in range(1, 10000):
                if measures[i][j] - measures[i][j-1] > gap:
                    gap = measures[i][j] - measures[i][j-1]
                    threshold[i] = (measures[i][j]+measures[i][j-1])/2

        print("Running...")
        running = True
        while running:
            # Read line from serial
            line = ser.readline()
            line = line.decode().strip("\r\n")
            line = line.split(" ")
            line = [int(j or 0) for j in line]

            for i in range(3):
                if line[i] > threshold[i]:
                    print("Playing")
                    p[i].start()

        p[i].join()
    except Exception as e:
        sys.exit("Error while handling data from serial : "+str(e))
