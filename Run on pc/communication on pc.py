# run this program on the Mac to display image streams from multiple RPis
import socket
import cv2
import imagezmq
from threading import Thread

image_hub = imagezmq.ImageHub()

HOST = '192.168.43.85'  # Enter IP or Hostname of your server
# Pick an open Port (1000+ recommended), must match the server port
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def get_image():
    while True:  # show streamed images until Ctrl-C
        rpi_name, image = image_hub.recv_image()
        cv2.imshow(rpi_name, image)  # 1 window for each RPi
        cv2.waitKey(1)
        image_hub.send_reply(b'OK')


def send_message():
    while True:
        command = input('Enter your command: ')
        s.send(command.encode())


t1 = Thread(target=get_image)
t2 = Thread(target=send_message)

t1.start()
t2.start()
