import cv2
import numpy as np
from threading import Thread
from pcCommunicate import connectPi

connector = connectPi('192.168.43.85')

rpi_name = ''
image = np.zeros((240, 320, 3))


def get_image():
    while True:
        global rpi_name
        global image
        rpi_name, image = connector.get_image()
        cv2.imshow(rpi_name, image)
        cv2.waitKey(1)


t = Thread(target=get_image)
t.start()

while True:
    #print(image[120, 160, 0])
    command = input('Enter your command: ')
    connector.send_message(command)
