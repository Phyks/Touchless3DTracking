#!/bin/env python

# NOTE : This script is *not* working yet...

# ============================================================================
# I had to play "Petit papa Noël" in an original way for some events. So, why
# not using these cool electrodes to handle it ? Left hand would control the
# volume and right hand, the note which is played.
#
# Disclaimer : Even with a lot of practice, I'm not sure you will be able to
# play a nice with this script :)
#
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

import serial
import pygame
import sys
import getopt


serial_port = "/dev/ttyACM0"

try:
    opts, args = getopt.getopt(sys.argv[1:], "hs:", ["help", "serial="])

    for opt, arg in opts:
        if opt == "-h" or opt == "-help":
            print("Touchless 3D tracking with color mapping")
            print("\nUsage : "+sys.argv[0]+" [OPTIONS]")
            print("\nTrack the position of your hand in 3D and map it " +
                  "in RGB space")
            print("\nOptions :")
            print("\t-h (--help) \t display this help message")
            print("\t-s (--serial) \t change serial port (default is " +
                  "/dev/tty/ACM0")
            sys.exit(0)
        elif opt in ("-s", "--serial"):
            serial_port = arg
except getopt.GetoptError:
    pass

ser = serial.Serial(serial_port, 115200)

try:
    ser.open()
except Exception as e:
    print("Error while opening serial port : "+str(e))

if ser.isOpen():
    try:
        ser.flushInput()
        ser.flushOutput()

        print("Calibration :")
        print("Press any key to launch the program when calibration is " +
              "finished.")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    running = False
                    continue

            line = ser.readline()
            line = line.decode().strip("\r\n")
            line = line.split(" ")
            line = [int(j or 0) for j in line]

            for i in range(3):
                if line[i] < minimum[i] or minimum[i] < 0:
                    minimum[i] = line[i]
                if line[i] > maximum[i]:
                    maximum[i] = line[i]

            print(line)

        print("Running...")
        running = True
        while running:
            # Read line from serial
            line = ser.readline()
            line = line.decode().strip("\r\n")
            line = line.split(" ")
            line = [int(j or 0) for j in line]

            # Compute the value for red
            value[1] = value[0]
            value[0] = compute_value(line, minimum, maximum)
            value_bg = [(value[0][i] + value[1][i])/2 for i in range(3)]
            value_text = [255 - i for i in compute_value(line, minimum,
                                                         maximum)]

        ser.close()
    except Exception as e:
        print("Error while fetching data from serial : "+str(e))
