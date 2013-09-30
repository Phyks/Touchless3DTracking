#!/bin/env python

import serial
import pygame

ser = serial.Serial("/dev/ttyACM0", 115200)
pygame.init()

size = width, height = 640, 480
black = 0, 0, 0
screen = pygame.display.set_mode(size)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)

try:
    ser.open()
except Exception, e:
    print("Error while opening serial port : "+str(e))

if ser.isOpen():
    ser.flushInput()
    ser.flushOutput()

    maximum = -1.
    minimum = -1.
    print("Calibration")
    screen.blit(background, (0,0))
    pygame.display.flip()
    for i in range(50) :
        line = float(ser.readline())
	
	if line < minimum or minimum < 0:
		minimum = line
	if line > maximum:
		maximum = line

    print("Go")
    while True:
	line = float(ser.readline())
	background.fill((int(255.*(line-minimum)/(maximum-minimum)), 0, 0))
	screen.blit(background, (0,0))
	pygame.display.flip()

    ser.close()
