#!/bin/env python

import serial
import pygame

ser = serial.Serial("/dev/ttyACM0", 115200)
pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))

try:
    ser.open()
except Exception:
    print("Error while opening serial port.")

if ser.isOpen():
    try:
        ser.flushInput()
        ser.flushOutput()

        maximum = -1
        minimum = -1

        print("Calibration :")
        pygame.display.flip()

        for i in range(50) :
            line = float(ser.readline())

            if line < minimum or minimum < 0:
                minimum = line
                if line > maximum:
                    maximum = line

        print("Go :")
        while True:
            line = float(ser.readline())
            valueR = int(255*(line-minimum)/(maximum-minimum))
            if valueR < 0:
                valueR = 0
            if valueR > 255:
                valueR = 255

            screen.fill((valueR, 0, 0))
            pygame.display.flip()

        ser.close()
    except Exception:
        print("Error while fetching data from serial.")
