import cv2
import numpy as np
from threading import Thread
from pcCommunicate import connectPi
from time import sleep

connector = connectPi('192.168.43.195')

rpi_name = ''
image = np.zeros((240, 320, 3))
count = 0
path = 'turn.txt'
f = open(path, 'w')


def empty(v):
    pass


cv2.namedWindow('TrackBar')
cv2.resizeWindow('TrackBar', 640, 320)
cv2.createTrackbar('Threshold', 'TrackBar', 50, 100, empty)


def get_image():
    global rpi_name
    global image
    rpi_name, image = connector.get_image()
    cv2.imshow(rpi_name, image)
    cv2.waitKey(1)


def send_message():
    global count
    while True:
        turnAngle = (cv2.getTrackbarPos('Threshold', 'TrackBar')-50)/100
        command = 't '+str(turnAngle)+'\n'
        connector.send_message(command)
        if count%10==0:      
            cv2.imwrite('pictures/'+str(count)+'.jpg',image)
            f.write(str(str(count)+' '+str(turnAngle)+'\n'))
        count += 1


try:
    t = Thread(target=send_message)
    t.start()


    while True:
        get_image()
except KeyboardInterrupt:
    f.close()
    print('KeyboardInterrupt exception is caught')





