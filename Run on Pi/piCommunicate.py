# run this program on each RPi to send a labelled image stream
import socket
import time
from imutils.video import VideoStream
import imagezmq


class ConnectPC():
    def __init__(self, pi_ip, pc_ip, port1=12345, port2=5555):
        self.pi_ip = pi_ip
        self.pc_ip = pc_ip
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((pi_ip, port1))
        except socket.error:
            print('Bind failed ')
        self.s.listen(5)
        print('Socket awaiting messages')
        (self.conn, addr) = self.s.accept()
        print('Connected')

        connect_location = 'tcp://'+pc_ip+':'+str(port2)
        self.sender = imagezmq.ImageSender(connect_to=connect_location)
        # rpi_name = socket.gethostname()  # send RPi hostname with each image
        self.picam = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)  # allow camera sensor to warm up

    def send_image(self):
        image = self.picam.read()
        self.sender.send_image(self.pi_ip, image)

    def get_message(self):
        data = self.conn.recv(1024).decode()
        return data
