#!/usr/bin/env python3

# ============================================================================
# This script allows you to play music using a chorizo (or whatever food you
# like) keyboard ! See README for more info and links.

# Specially designed for our demo for Christmas 2013. Designed to fully handle
# 5 notes and play jingle bells.

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


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

getch = _Getch()


def play_wave(frequency=440, nb_secs=1.):
    sine_wave = []
    for i in range(math.ceil(nb_secs*framerate)+1):
        sine_wave.append(int(16384*math.sin(2*math.pi*frequency*i/framerate)))
    sound(sine_wave)


def read_serial(ser):
    line = ser.readline()
    line = line.decode().strip("\r\n")
    line = line.split(" ")
    return [int(i or 0) for i in line]

framerate = 16000
processes = []
frequencies = {"FA": 698.5, "SOL": 784, "LA": 880, "SIb": 932, "DO": 1046.5}
notes = list(frequencies.keys())
thresholds = []
measures = []

serial_port = "/dev/ttyACM0"
serial_speed = 115200

try:
    opts, args = getopt.getopt(sys.argv[1:], "hs:S:", ["help", "serial=",
                                                       "speed="])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Play music with chorizos ! Only a limited set of notes " +
                  "is available to play jingle bells.")
            print("\nUsage : "+sys.argv[0]+" [OPTIONS]")
            print("\nOptions :")
            print("\t-h (--help) \t display this help message")
            print("\t-s (--serial=) \t change serial port (default is " +
                  "/dev/tty/ACM0")
            print("\t-S (--speed=) \t change serial speed (default is 115200)")
            sys.exit(0)
        elif opt in ("-s", "--serial"):
            serial_port = arg
        elif opt in ("-S", "--speed"):
            serial_speed = arg
except getopt.GetoptError:
    pass

# Handle serial opening
try:
    ser = serial.Serial(serial_port, serial_speed)
except Exception as e:
    sys.exit("Invalid serial port options : "+str(e))

try:
    if not ser.isOpen():
        ser.open()
except Exception as e:
    sys.exit("Error while opening serial port : "+str(e))

ser.flushInput()
ser.flushOutput()

# Handle calibration
for i in range(len(notes)):
    print("Calibrating note "+notes[i])
    print("Touch and release the key now... Will get 1k samples.")

    for sample in range(1000):
        measure = read_serial(ser)
        measures[sample] = measure[i]

    measures.sort()
    max_diff = 0
    max_diff_index = 0

    for sample in range(1000-1):
        if measures[sample+1]-measures[sample] > max_diff:
            max_diff = measures[sample+1]-measures[sample]
            max_diff_index = sample

    thresholds[i] = (measures[max_diff_index+1]+measures[max_diff_index])/2

# Main loop
print("Running... Press q to quit.")
running = True
while running:
    serial_input = read_serial(ser)
    frequency = 0

    for note in range(len(notes)):
        if serial_input[note] > thresholds[note]:
            frequency = frequencies[notes[note]]

    if frequency == 0:
        char = getch()
        if char == "q":
            print("Exiting...")
            running = False
            continue
        if char == "a":
            frequency = frequencies["LA"]
        elif char == "b":
            frequency = frequencies["SIb"]
        elif char == "c":
            frequency = frequencies["DO"]
        elif char == "e":
            frequency = frequencies["FA"]
        elif char == "g":
            frequency = frequencies["SOL"]
        else:
            continue

    print("Playing "+char.upper())
    processes.append(Process(target=play_wave,
                     args=(frequency,
                           math.floor(0.2 * frequency + 1) / frequency)))
    processes[-1].start()

for i in processes:
    i.join()
