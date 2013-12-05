#!/bin/env python3

# ============================================================================
# This script maps the 3D position of your hand, as detected by the electrodes
# in the RGB space, allowing you to pick a color for real.

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


def compute_value(line, minimum, maximum):
    if len(line) < 3:
        return False

    value = [0, 0, 0]
    for i in range(3):
        if maximum[i]-minimum[i] != 0:
            value[i] = int(255*(line[i]-minimum[i])/(maximum[i]-minimum[i]))
        else:
            value[i] = 0

        if value[i] > 255:
            value[i] = 255
        elif value[i] < 0:
            value[i] = 0

    return value


serial_port = "/dev/ttyACM0"

try:
    opts, args = getopt.getopt(sys.argv[1:], "hs:", ["help", "serial="])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Touchless 3D tracking with color mapping")
            print("\nUsage : "+sys.argv[0]+" [OPTIONS]")
            print("\nTrack the position of your hand in 3D and map it " +
                  "in RGB space")
            print("\nOptions :")
            print("\t-h (--help) \t display this help message")
            print("\t-s (--serial=) \t change serial port (default is " +
                  "/dev/tty/ACM0")
            sys.exit(0)
        elif opt in ("-s", "--serial"):
            serial_port = arg
except getopt.GetoptError:
    pass

ser = serial.Serial(serial_port, 115200)
pygame.init()

# Keep old value to determine a mean value
value = [[0, 0, 0], [0, 0, 0]]
font = pygame.font.Font(None, 36)

size = width, height = 640, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Touchless 3D tracking")
screen.fill((0, 0, 0))

try:
    ser.open()
except Exception as e:
    print("Error while opening serial port : "+str(e))

if ser.isOpen():
    try:
        ser.flushInput()
        ser.flushOutput()

        maximum = [-1, -1, -1]
        minimum = [-1, -1, -1]

        print("Calibration :")
        print("Press any key to launch the program when calibration is " +
              "finished.")
        # Display info in window
        label = font.render("Calibration...", 1, (255, 255, 255))
        label_pos = label.get_rect()
        label_pos.centerx = screen.get_rect().centerx
        label_pos.centery = 20
        screen.blit(label, label_pos)

        pygame.display.flip()

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
            # Quit if window is closed
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    pygame.quit()
                    running = False
                    continue

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

            if value is not False:
                screen.fill((value_bg[0], value_bg[1], value_bg[2]))

                # Display info in window
                label = font.render("Running...", 1, (value_text[0],
                                    value_text[1], value_text[2]))
                label_pos = label.get_rect()
                label_pos.centerx = screen.get_rect().centerx
                label_pos.centery = 20
                screen.blit(label, label_pos)

                pygame.display.flip()

        ser.close()
    except Exception as e:
        print("Error while fetching data from serial : "+str(e))
