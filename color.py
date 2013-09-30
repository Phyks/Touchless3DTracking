#!/bin/env python

import serial
import pygame


def compute_value(line, minimum, maximum):
    line = line.split(" ")
    if len(line) < 3:
        return False

    for i in range(3):
        value[i] = int(255*(line[i]-minimum[i])/(maximum[i]-minimum[i]))
        if value[i] > 255:
            value[i] = 255
        elif value[i] < 0:
            value[i] = 0

    return value[0]


ser = serial.Serial("/dev/ttyACM0", 115200)
pygame.init()

# Keep old value to determine a mean value
value = [[0, 0, 0], [0, 0, 0]]
font = pygame.font.Font(None, 36)

size = width, height = 640, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Touchless 3D tracking")
screen.fill((0, 0, 0))(value[0]+value[1])

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
        print("Press any key to launch the program when calibration is" +
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
                if event.type == pygame.K_RETURN:
                    running = False

            line = float(ser.readline())

            if line < minimum or minimum < 0:
                minimumR = line
            if line > maximum:
                maximumR = line

        print("Running...")
        running = True
        while running:
            # Quit if window is closed
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    pygame.quit()
                    running = False

            # Read line from serial
            line = float(ser.readline())
            # Compute the value for red
            value[1] = value[0]
            value[0] = compute_value(line, minimum, maximum)
            value_bg = [value[0][i] + value[1][i] for i in range(3)]
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
