import socket
import imagezmq


class connectPi():
    def __init__(self, pi_ip, port=12345):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((pi_ip, port))
        self.image_hub = imagezmq.ImageHub()

    def get_image(self):
        rpi_name, image = self.image_hub.recv_image()
        self.image_hub.send_reply(b'OK')
        return rpi_name, image

    def send_message(self, str):
        self.s.send(str.encode())
