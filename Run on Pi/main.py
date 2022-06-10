from threading import Thread
from piCommunicate import ConnectPC
from drive import turn, ChangeSpeed

connector = ConnectPC('192.168.43.85', '192.168.43.93')


def send_image():
    while True:
        connector.send_image()


def get_message():
    while True:
        message = connector.get_message()
        print(message)
        if message.split()[0] == 't':
            turnAngle = float(message.split()[1])
            if -0.2 <= turnAngle <= 0.2:
                turn(turnAngle)
        elif message.split()[0] == 'd':
            speed = int(message.split()[1])
            if 0 <= speed <= 100:
                ChangeSpeed(speed)


t1 = Thread(target=send_image)
t2 = Thread(target=get_message)

t1.start()
t2.start()
