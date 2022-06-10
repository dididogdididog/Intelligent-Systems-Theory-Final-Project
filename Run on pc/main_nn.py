import cv2
import numpy as np
from threading import Thread
from pcCommunicate import connectPi
from time import sleep
from tensorflow import keras

connector = connectPi('192.168.43.195')

rpi_name = ''
image = np.zeros((240, 320, 3))
model=keras.models.load_model('models/ann.h5')



def get_image():
    global rpi_name
    global image
    rpi_name, image = connector.get_image()
    cv2.imshow(rpi_name, image)
    image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image_clip=image_gray[100:,:]
    image_flat=image_clip.reshape(1,image_clip.shape[0]*image_clip.shape[1])
    image_flat=image_flat/255
    #image_clip=image_clip.reshape(1,image_clip.shape[0],image_clip.shape[1])
    turnAngle = model.predict(image_flat)[0][0]
    command = 't '+str(turnAngle)+'\n'
    connector.send_message(command)    
    cv2.waitKey(100)



try:
    while True:
        get_image()
except KeyboardInterrupt:
    print('KeyboardInterrupt exception is caught')





