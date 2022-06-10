# run this program on each RPi to send a labelled image stream
import socket
import time
from imutils.video import VideoStream
import imagezmq
from threading import Thread

HOST = '192.168.43.85'  # Server IP or Hostname
# Pick an open Port (1000+ recommended), must match the client sport
PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# managing error exception
try:
    s.bind((HOST, PORT))
except socket.error:
    print('Bind failed ')

s.listen(5)
print('Socket awaiting messages')
(conn, addr) = s.accept()
print('Connected')


sender = imagezmq.ImageSender(connect_to='tcp://192.168.43.93:5555')
rpi_name = socket.gethostname()  # send RPi hostname with each image
picam = VideoStream(usePiCamera=True).start()
time.sleep(2.0)  # allow camera sensor to warm up


def send_image():
    while True:  # send images as stream until Ctrl-C
        image = picam.read()
        sender.send_image(rpi_name, image)


def get_message():
    while True:
        data = conn.recv(1024).decode()
        print('Client: ' + data)


t1 = Thread(target=send_image)
t2 = Thread(target=get_message)

t1.start()
t2.start()
